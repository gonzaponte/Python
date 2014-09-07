#
# Module with the Coordinates class.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from math import *

class Coordinates:
    ''' Coordinates translator.'''
    
    def __init__( self, arg1 = 0.0, arg2 = 0.0, arg3 = 0.0, mode = 'cartesian' ):
        ''' Class constructor. It takes 3 arguments which are the 3 components of the reference frame. The system of reference can be chosen with the mode argument. The options are:
            - cartesian
            - cylindric
            - spheric'''
        
        self.repr = 'cartesian'
        
        if   mode == 'cartesian':
            self.cartesian  = [ arg1, arg2, arg3 ]
            
            self.__ComputeCylindric()
            self.__ComputeSpheric()
        
        elif mode == 'cylindric':
            self.cylindric = [ arg1, arg2, arg3 ]
            
            self.__ComputeCartesian('cylindric')
            self.__ComputeSpheric()

        elif mode == 'spheric':
            self.spheric    = [ arg1, arg2, arg3 ]
            
            self.__ComputeCartesian('spheric')
            self.__ComputeCylindric()
    
    
    def __add__( self, other ):
        ''' Sum operator with a number or another vector.'''
        
        if not isinstance( other, Coordinates ):
            new = map( lambda x: x + other, self.cartesian)
        else:
            new = map( lambda x,y: x + y, self.cartesian, other.cartesian)
        
        return Coordinates( *new )
    
    def __radd__( self, number ):
        return self + number
        
    def __mul__( self, other ):
        ''' Product operator with a number'''
        
        new     = list(self.spheric)
        new[0] *= other
        new.append( 'spheric' )
        
        return Coordinates( *new )

    def __rmul__( self, number ):
        return self * number
        
    def __neg__( self ):
        ''' Parity operation on the vector.'''
        
        return Coordinates( *map( lambda x: -x, self.cartesian ) )
    
    def __sub__( self, other ):
        ''' Substraction operation with a number or another vector.'''
        
        return self + (-other)
        
    def __div__( self, number ):
        ''' Division operation by a number.'''
        
        return self * (1./number)
    
    def __eq__( self, other ):
        ''' Checks wheter the vector has the same components as another one.'''

        return self.cartesian == other.cartesian
    
    def __ne__( self, other ):
        ''' Checks whether the vector has not the same module as another one.'''
        return not self==other
    
    def __gt__( self, other ):
        ''' Checks whether the vector has greater module than another one.'''
    
        return self.spheric[0] > other.spheric[0]
    
    def __lt__( self, other ):
        ''' Checks whether the vector has lower module than another one.'''
        
        return self.spheric[0] < other.spheric[0]
    
    def __ge__( self, other ):
        ''' Checks whether the vector has greater or equal module than another one.'''

        return not self < other
    
    def __le__( self, other ):
        ''' Checks whether the vector has lower or equal module than another one.'''
        
        return not self > other
        
    def __repr__(self):
        ''' Returns a string representation of the vector.'''
        
        if self.repr == 'cartesian':
            return str( self.GetX() )   +   ' x + ' + str( self.GetY() )        +        ' y + ' + str( self.GetZ() )      + ' z'
        
        if self.repr == 'cylindric':
            return str( self.GetRho() ) + ' rho + ' + str( self.GetPhi()/pi )   +   ' pi phi + ' + str( self.GetZ() )      + ' z'
            
        if self.repr == 'spheric':
            return str( self.GetR() )   +   ' r + ' + str( self.GetTheta()/pi ) + ' pi theta + ' + str( self.GetPhi()/pi ) + ' pi phi'

        if self.repr == 'all':
            self.repr = 'cartesian'
            Cartesian = self.__repr__()
            self.repr = 'cylindric'
            Cylindric = self.__repr__()
            self.repr = 'spheric'
            Spherical = self.__repr__()
            self.repr = 'all'
            
            return Cartesian + '\n' + Cylindric + '\n' + Spherical + '\n'

    def GetX( self ):
        ''' Returns the x component of the vector.'''
        
        return self.cartesian[0]
    
    def GetY( self ):
        ''' Returns the y component of the vector.'''
        
        return self.cartesian[1]
    
    def GetZ( self ):
        ''' Returns the z component of the vector.'''
        
        return self.cartesian[2]
    
    def GetR( self ):
        ''' Returns the r component of the vector.'''
        
        return self.spheric[0]
    
    def GetRho( self ):
        ''' Returns the rho component of the vector.'''
        
        return self.cylindric[0]
    
    def GetTheta( self ):
        ''' Returns the theta component of the vector.'''
        
        return self.spheric[1]
    
    def GetPhi( self ):
        ''' Returns the phi component of the vector.'''
        
        return self.cylindric[1]
    
    def Zero( self ):
        ''' Sets all the coordinates to 0.'''
        
        self.cartesian = [ 0., 0., 0. ]
        self.cylindric = [ 0., 0., 0. ]
        self.spheric   = [ 0., 0., 0. ]
    
    def SetRepresentation( self, value = 'cartesian' ):
        ''' Sets the mode of representation. Options:
            - cartesian: cartesian components
            - cylindric: cylindric components
            - spheric:   spherical components
            - all:       all representations at the same time.'''
        
        self.repr = value

    def __ComputeCartesian( self, FROM ):
        
        if FROM == 'cylindric':
            self.cartesian    = range(3)
            self.cartesian[0] = self.GetRho() * cos( self.GetPhi() )
            self.cartesian[1] = self.GetRho() * sin( self.GetPhi() )
            self.cartesian[2] = self.cylindric[2]
        
        elif FROM == 'spheric':
            self.cartesian    = range(3)
            self.cartesian[0] = self.GetR() * sin( self.GetTheta() ) * cos( self.spheric[2] )
            self.cartesian[1] = self.GetR() * sin( self.GetTheta() ) * sin( self.spheric[2] )
            self.cartesian[2] = self.GetR() * cos( self.GetTheta() ) *           1

    def __ComputeCylindric( self ):
        
        self.cylindric    = range(3)
        self.cylindric[0] = sqrt( self.GetX()**2 + self.GetY()**2 )
        self.cylindric[1] = atan( self.GetY()/self.GetX() ) if self.GetX() else sign(self.GetY()) * 0.5 * pi if self.GetY() else 0.
        self.cylindric[2] = self.GetZ()

    def __ComputeSpheric( self ):
        
        self.spheric    = range(3)
        self.spheric[0] = sqrt( self.GetX()**2 + self.GetY()**2  + self.GetZ()**2 )
        self.spheric[1] = acos( self.GetZ()/ self.GetR() ) if self.GetR() else 0.
        self.spheric[2] = self.GetPhi()


