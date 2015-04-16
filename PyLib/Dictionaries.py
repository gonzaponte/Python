#
# Module with some functions for dictionaries.
#
#
# Author: Gonzalo Martinez
#
# Last update: 08 / 04 / 2014
#

from Sequences import Izip

def Str( dictionary ):
    '''
        Prints a dictionary in a sorted and fancy way.
    '''
    return '\n'.join( [ str(key) + ' => ' +  str(dictionary[key]) for key in sorted( dictionary ) ] )

def Idict( dictionary ):
    '''
        Inverts keys and values.
    '''
    return dict( Izip( dictionary.items() ) )

def DoubleDict( dictionary ):
    '''
        Return a dictionary made of input + inverse of input.
    '''
    return dict( dicionary ).update( Idict( dicionary ) )
