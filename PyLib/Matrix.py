#
# Module with the matrix class.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from Vector import Vector
from Math import Transpose


class Matrix( Vector ):
    ''' Matrix instance.'''
    
    def __init__( self, values = [ [] ], nrows = 0, ncols = 0):
        ''' Class constructor. It takes the components in a list of lists and copy them to the data members. It also can be constructed giving a number and both dimensions.'''
        
        # By-size constructor
        if nrows and ncols:
            self.v = Vector( Vector( values, ncols ), nrows )
        
        # Copy constructor
        elif isinstance( values, Matrix ):
            self.v = Vector( map( Vector, values.v ) )
                
        # Normal constructor
        else:
            self.v = Vector( map( lambda x: Vector(x), values ) )
        
        self.rows = len( self.v )
        self.cols = len( self.v[0] )

    def __add__( self, other ):
        ''' Sum operation with another matrix or number.'''
        
        if not isinstance( other, Matrix ):
            other = Matrix( other, self.rows, self.cols)
        
        return Matrix( self.v + other.v )
    
    def __mul__( self, other ):
        ''' Product operation with another matrix (element by element) or with another number.'''
        
        if not isinstance( other, Matrix ):
            other = Matrix( other, self.rows, self.rows )

        return Matrix( self.v * other.v )
    
    def __pow__( self, other ):
        ''' Product operation with another matrix or vector.'''
        
        # Operation with a vector.
        if isinstance( other, vector):
            return Vector( map( lambda x: x ** other, self.v ) )
        
        otherT = other.T()
        return Matrix( [ map( lambda O: S ** O, otherT.v ) for S in self.v ] )
    
    def __rpow__( self, other ):
        ''' Vector product on a matrix.'''
        
        return self.T() ** other
        
    def __neg__( self ):
        ''' Sign inversion.'''
        
        return Matrix( -self.v )
    
    def __rdiv__( self, number ):
        ''' Right division (component by component).'''
        
        return number * Matrix( 1. / self.v )
    
    def __repr__( self ):
        ''' Representacion da Matrix.'''
        
        return reduce( lambda x,y: str(x) + '\n' + str(y), self.v )
    
    def T(self):
        ''' Matrix transposition.'''
        
        return Transpose( self.v )
#        return Matrix( [ [ self[j][i] for j in range(self.rows) ] for i in range(self.cols)])
    
    def Zero( self ):
        ''' Sets all the coordinates to 0.'''
        
        map( lambda x: x.Zero(), self.v )
    
    def Size( self ):
        ''' Size of the matrix.'''
        
        return self.rows, self.cols
