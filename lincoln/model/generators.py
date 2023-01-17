'''
Inflow generator functions.
'''

from random import randint

def uniform_generator(min=2, max=12):
    '''Generates random integer on range: [min, max] (inclusive).'''
    return randint(a=min, b=max)