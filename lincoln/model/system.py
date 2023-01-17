'''
System of nodes.
'''

from dataclasses import dataclass, field
from typing import List, Dict, Any

from lincoln.model import node
from lincoln.model.node import Node

def SystemValidationError(Exception):
    pass
    
@dataclass
class Network:
    '''Describes direction of flow between system nodes.'''
    names: List[str]
    '''Node names in order their data appears as row or columns in matrix.'''
    matrix: List[List[str]]
    '''A square mxm matrix that describes the connection between system nodes. Entry is 1 if matrix row node is connected to matrix column node, 0 otherwise.'''

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        #l = [len(self.matrix)] + [len(self.matrix[i]) for i in range(0, len(self.matrix))] + [len(self.names)]
        if len(set([len(self.matrix)] + [len(self.matrix[i]) for i in range(0, len(self.matrix))] + [len(self.names)])) != 1:
            raise ValueError('The system network matrix is not mxm (i.e. square) or the number of node names, does not match the number row and column entries in the matrix.')
 
@dataclass
class System:
    network: Network
    nodes: Dict[str, Node] = field(default_factory=lambda: {})

    # def diagram(self):
    #     layers = []
    #     is_top_layer: bool = True
    #     is_not_finished: bool = False
    #     while is_not_finished:
    #         current_layer = []
    #         if is_top_layer:
    #             current_layer = [k for k, v in self.nodes.items() if v.tag == node.Tag.inflow]
    #         else:
    #             last_layer = layers[-1]
    #             for k, v in self.nodes.items():
    #                 for i in v.#senders.
    #                     if i in last_layer
    #             current_layer = [k for k, v in self.nodes.items() if ]

def factory(data: Dict[str, Any]):
    # a recursive solution would be better here.  
    senders = {}
    system = System(Network(data['system']['order'], data['system']['matrix']))
    while len(system.nodes) != len(system.network.names):
        new_layer = _add_layer(system, senders, data)
        system.nodes.update(new_layer)
        senders = new_layer
    return system

def _add_layer(system: System, senders: Dict[str, Node], data: Dict[str, Any]) -> Dict[str, Node]:
    return _add_receiver_nodes(system, senders, data) if senders else _add_inflow_nodes(system, data)

def _add_inflow_nodes(system: System, data: Dict[str, Any]) -> Dict[str, Node]:
    recievers = [sum([system.network.matrix[row][col] for row in range(0, len(system.network.matrix))]) for col in range(0, len(system.network.matrix[0]))]
    return {system.network.names[i]: node.factory(**data['node'][system.network.names[i]]) for i in range(0, len(recievers)) if recievers[i] == 0}

def _add_receiver_nodes(system: System, senders: Dict[str, Node], data: Dict[str, Any]):
    new_nodes = {}
    for k, v in senders.items():                                    # iterate through last layer
        row = system.network.matrix[system.network.names.index(k)]  # row of sender node name
        for col in range(0, len(row)):      
            if row[col] == 1:               # sender-receiver entry
                node_name = system.network.names[col]              # receiver node name
                if node_name in system.nodes:                      # node already added
                    # this is ugly.
                    system.nodes[node_name].add_sender({k: v})
                else:                                              # new node
                    if node_name not in new_nodes:
                        new_nodes[node_name] = node.factory(**data['node'][node_name])
                    new_nodes[node_name].add_sender({k: v})
                    # if node_name in new_nodes:                     # existing new node
                    #     new_nodes[node_name].add_sender({k: v})
                    # else:                                          # add node to new list
                    #     #data['node'][node_name]['senders'] = [k]
                    #     new_nodes[node_name] = node.factory(**data['node'][node_name])                     
    return new_nodes

        
# def identify_inflows(node_names: List[str], matrix: List[List[int]]) -> List[str]:
#     '''
#     Identifies columns in matrix, that receive no inflows (and therefore are inflow nodes).
    
#     Parameters
#     ----------
#     node_names: List[str]
#         a list of node's names represented in the matrix, in the same order they appear in the matrix's rows and columns.
#     matrix: [List[List[int]]]
#         a square (mxm) matrix of 0's and 1's, with a 1 if the column node recieves flow from the row node, and 0 otherwise.
    
#     Returns
#         containing the names of inflow nodes (those were the sum of the matrix colum = 0).
        
#     Raises
#     ----------
#     ValueError
#         if the matrix is not square (mxm), or the number of entries in the node_names list does not match the number of rows and columns in the matrix.
#     '''
#     check_matrix(node_names, matrix)
#     recievers = [sum([matrix[    ----------
#     List[strow][col] for row in range(0, len(matrix))]) for col in range(0, len(matrix[0]))]
#     return {node_names[i]:  for i in range(0, len(recievers)) if recievers[i] == 0}

# def identify_recievers(node_names: List[str], matrix: List[List[int]], senders: List[str] = []) -> List[str]:
#     check_matrix(node_names, matrix)
#     if len(senders) == 0:
#         return identify_inflows(node_names, matrix)
#     else:
#         sender_rows = [i for sender_name in senders for i in range(0, len(node_names)) if sender_name == node_names[i]]
#         return [node_names[col] for row in sender_rows for col in range(0, len(matrix[row])) if matrix[row][col] == 1]        

# # centralize errors in system validator


         
# def check_matrix(node_order: List[str], matrix: List[List[int]]) -> None:
#     nodes, rows = len(node_order), len(matrix)
#     if nodes != rows:
#         raise SystemValidationError(f'The system matrix contains {rows} rows but a list of {nodes} node names were provided causing an error.')
#     for row in range(0, len(matrix)):
#         if nodes != len(matrix[row]):
#             raise SystemValidationError(f'Row {row} of the system matrix contains {len(matrix[row])} entries (i.e. columns), but a list of {nodes} node names were provided causing an error.')