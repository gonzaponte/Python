#
# Module with the Vector class.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from math import *


class Vector:
    ''' Vector instance.'''
    
    def __init__( self, values, dim = 0 ):
        ''' Class constructor. It takes the components in a list and copy them to the data members. It also can be constructed giving a number and the dimension of the vector.'''
        
        # By - size constructor
        if dim:
            self.v = [ values for i in xrange( dim ) ]
        
        # Copy constructor
        elif isinstance( values, Vector ):
            self.v = list( values.v )
        
        # Normal constructor
        else:
            self.v = list( values )
    
        self.l = len( self.v )
    
    def __add__( self, other ):
        ''' Sum operator with a number or another vector.'''
        
        if not isinstance( other, vector ):
            other = Vector( other, self.l )
        
        return Vector( map(lambda x,y: x+y, self.v, other.v) )
    
    def __radd__( self, number ):
        return self + number
    
    def __iadd__( self, other):
        return self + other
    
    def __mul__( self, other ):
        ''' Product operator with a number or another vector (component by component).'''
        
        if not isinstance(other,vector):
            other = Vector( other, self.l )
        
        return Vector( map( lambda x,y: x*y, self.v, other.v) )
    
    def __rmul__( self, number ):
        return self * number
    
    def __pow__( self, other ):
        ''' Returns scalar product of the vector with another vector.'''
        
        return sum( ( self * other ).v )
    
    def __neg__( self ):
        ''' Sign inversion on the vector.'''
        
        return Vector( map( lambda x: -x, self.v ) )
    
    def __sub__( self, other ):
        ''' Substraction operation with a number or another vector.'''
        
        return self + (-other)
    
    def __div__( self, other):
        ''' Division operation with a number or another vector (component by component).'''
        
        if not isinstance(other,vector):
            other = Vector( other, self.l )
        
        return self * ( 1. / other )
    
    def __rdiv__( self, number ):
        ''' Operation defined for other classes when dividing by a vector.'''
        
        return Vector( map( lambda x: number/x, self.v ) )
    
    def __getitem__(self,index):
        ''' Returns the index-th component of the vector starting from 0.'''
        
        return self.v[index]
    
    def __setitem__(self,index,value):
        ''' Assign value to the index-th component of the vector.'''
        
        self.v[index] = value
    
    def __len__(self):
        ''' Number of elements.'''
        
        return self.l
    
    def __reversed__( self ):
        ''' Reverse the list of values.'''
    
        return self.v[::-1]
    
    def __repr__(self):
        ''' Returns a string representation of the vector.'''
        
        return reduce( lambda x,y: x + ' ' + y, map( lambda z: str(z), self.v) )
    
    def Zero( self ):
        ''' Sets all the coordinates to 0.'''
        
        self.v = [ 0. for i in xrange( self.l ) ]

