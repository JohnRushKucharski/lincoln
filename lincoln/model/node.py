'''Contains game elements'''

import typer

from enum import Enum
from functools import partial
from dataclasses import dataclass, field
from typing import List, Set, Dict, Any, Callable, Protocol

from lincoln.model import generators
from lincoln.utilities import exception_handler

class Tag(str, Enum):
    '''Describes the type of node.'''
    inflow = 'inflow'
    '''Upstream most node, creates new inflows.'''
    storage = 'storage'
    '''Accept upstream inflow, sends flow downstream, can store water.'''
    transfer = 'transfer'
    '''Accept upstream inflow, sends flow downsteam, used for aggregation or rescaling flows.'''
    outflow = 'outflow'
    '''Accept upstream inflow that can be diverted out of the system.'''
    outlet = 'outlet'
    '''Downstream most node.'''

def factory(**kwargs):
    constructors = {
        'inflow': InflowNode.deserialize,
        'storage': StorageNode.deserialize,
        'outlet' : OutletNode.deserialize
    }
    return constructors[kwargs['tag']](kwargs)

class NodeValidationError(Exception):
    pass

class Node(Protocol):
    @property
    def tag(self) -> Tag:
        '''Enum describing node type.'''
    @property
    def senders(self) -> Dict[str, 'Node']:
        '''Set of node names that send inflow to node.'''

    def send(self) -> int:
        '''Sends flow downstream.'''
    def request_inflow(self) -> int:
        '''Requests inflows from sender nodes, if any. Initializes a chain reaction that sends flows to node.'''
    
    def serialize(self) -> Dict[str, Any]:
        '''Convert object into dictionary for storage.'''
    @staticmethod
    def deserialize(data: Dict[str, Any]):
        '''Parse dictionary containing object data.'''

# class Sender(Protocol):
#     def send(self, season='') -> int:
#         '''Sends flow downstream.'''
    
class Reciever(Protocol):
    def add_sender(self, sender_name: str) -> None:
        '''Adds connection to upstream sender.'''
    def remove_sender(self, sender_name: str) -> None:
        '''Removes connection to upstream sender.'''

@dataclass
class InflowNode:
    '''Sender only node.'''
    _data: Dict[str, Any]
    _generators: Dict[str, Callable[..., int]]

    @property
    def tag(self) -> Tag:
        return Tag.inflow
    @property
    def senders(self) -> Dict[str, Node]:
        '''This node generates its own inflows and has not senders.'''
        return {}
    
    def serialize(self) -> Dict[str, Any]:
        return self._data.update(self.senders) 
    @staticmethod
    @exception_handler(NodeValidationError, 9)
    def deserialize(data: Dict[str, Any]) -> 'InflowNode':
        '''Builds object from dictionary of object data.'''
        InflowNode.validate_keys(data)
        InflowNode.validate_data(data)
        genies: Dict[str, Callable[..., int]] = {}
        for i in range(0, len(data['generators'])):
            # TODO: #2 add plugin architecture for generators.
            match data['generators'][i]:
                case 'uniform':
                    genies[data['seasons'][i]] = partial(generators.uniform_generator, min=data['parameters'][i][0], max=data['parameters'][i][1])
                case other:
                    raise NodeValidationError(f'\"{data["generators"][i]}\" is not an implemented inflow node generator.')
        return InflowNode(data, genies)
    
    @staticmethod
    @exception_handler(KeyError, 10)
    def validate_keys(data: Dict[str, Any]):
        keys = ['tag', 'generators', 'seasons', 'parameters']
        for key in keys:
            if key not in data.keys():
                raise KeyError(f'{key} data is missing from the input node data.')
            
    @staticmethod
    @exception_handler(NodeValidationError, 9)
    def validate_data(data: Dict[str, Any]):
        if len(set([len(data['seasons']), len(data['generators']), len(data['parameters'])])) != 1:
            raise NodeValidationError('There is not a one-to-one mapping between the provided inflow node generators, seasons, and generator parameters.')
    
    def request_inflow(self, season: str = '') -> int:
        return self.send(season)          
    def send(self, season: str = '') -> int:  
        '''Generates an inflow that is sent to downstream connections.'''
        return self.generators[season]()
    
@dataclass
class StorageNode:
    '''Node with storage'''
    storage: int
    capacity: int
    _initial: int
    _senders: Set[str] = field(default_factory=lambda: {})
    
    @property
    def tag(self) -> Tag:
        return Tag.storage
    @property
    def senders(self) -> Dict[str, Node]:
        return self._senders
    
    def serialize(self):
        return {
            'tag': 'storage',
            'storage': self._initial,
            'capacity': self.capacity,
            'senders': [k for k in self.senders.keys()]
        }
    @staticmethod
    def deserialize(data: Dict[str, Any]):
        StorageNode.validate_keys(data)
        StorageNode.validate_data(data)
        return StorageNode(storage=data['initial'], capacity=data['capacity'], _initial=data['initial'])
    
    @staticmethod
    @exception_handler(KeyError, 10)
    def validate_keys(data: Dict[str, Any]):
        keys = ['tag', 'initial', 'capacity']
        for key in keys:
            if key not in data.keys():
                raise KeyError(f'{key} data is missing from the storage node data.')
            
    @staticmethod
    @exception_handler(NodeValidationError, 9)
    def validate_data(data: Dict[str, Any]):
        if data['initial'] < 0 or data['capacity'] < 0:
            raise NodeValidationError(f'The initial: {data["initial"]}, and capacity: {data["capacity"]} storage parameters must be set to positive integer values, with initial \u2264 capacity storage.')
        
    def add_sender(self, kvpair: Dict[str, Node]) -> None:
        self._senders.update(kvpair)
    def remove_sender(self, kvpair: Dict[str, Node]) -> None:
        self._senders.remove(kvpair)

    def request_inflow(self, season: str = ''):
        return sum([node.send(season) for node in self.senders.values()])
    def send(self, season: str = '') -> int:
        inflows = self.request_inflow(season)
        spill = max(0, self.storage + inflows - self.capacity)
        # put in some sort of decision object, that provides table and deals with prompt.
        if spill:
            release = typer.prompt(f'{spill} units have spilled. How much more would you like to release? [0, {self.storage}]')
        else:
            release = typer.prompt(f'How much would you like to release? [0, {self.storage}]')
        self.storage = self.storage + inflows - spill - release
        return release

@dataclass
class OutletNode:
    '''Node at outlet of system with no operations (i.e., inflow = outflow).'''
    _senders: Dict[str, Node] = field(default_factory=lambda: {})
    
    @property
    def tag(self) -> Tag:
        return Tag.outlet
    @property
    def senders(self) -> Dict[str, Node]:
        return self._senders
    
    def serialize(self):
        return {
            'tag': 'outlet',
            'senders': [k for k in self.senders.keys()]
        }
    @staticmethod
    def deserialize(data: Dict[str, Any]):
        return OutletNode()
    
    def add_sender(self, kvpair: Dict[str, Node]) -> None:
        self._senders.update(kvpair)
    def remove_sender(self, kvpair: Dict[str, Node]) -> None:
        self._senders.remove(kvpair)
        
    def request_inflow(self, season: str = ''):
        return sum([node.send(season) for node in self.senders.values()])
    def send(self, season: str = ''):
        return self.request_inflow(season)