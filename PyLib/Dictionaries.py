#
# Module with some functions for dictionaries.
#
#
# Author: Gonzalo Martinez
#
# Last update: 08 / 04 / 2014
#

from General import SUM
from Sequences import Izip
from DataAnalysis import Mean

def StrDic( dictionary ):
    ''' Prints a dictionary sorted and in a fancy way.'''
    
    return reduce( SUM, map( lambda key:'{0} => {1}\n'.format( str(key), str(dictionary[key]) ), sorted( dictionary ) ) )

def Idic( dic ):
    ''' Inverts keys and values.'''

    return dict( Izip( dic.items() ) )

def MakeDic( keys, values ):
    if not len(keys) == len(values):
        raise ValueError('Both lists must have the same length.')
    
    return dict( zip( keys, values ) )

def DoubleDic( dic ):
    return dic.update( Idic( dic ) )

def Add( basedic, addeddic ):
    ''' Add entries to an existing dictionary of the form (key : [values])'''
    for key in addeddic:
        basedic[key].append( addeddic[key] )

def Average( dictionary, weights = None ):
    ''' Apply mean to the values of a dictionary of the form (key : [values] ) in order to get (key : meanvalue).'''

    for key in dictionary:
        dictionary[key] = Mean( dictionary[key], weights )

