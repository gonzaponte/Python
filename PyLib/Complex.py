#
# Module with the Complex class.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from math import *
from Math import sign

class Complex:
    ''' Complex numbers instance.'''
    
    def __init__( self, arg1 = 0.0, arg2 = 0.0, mode = 'realimag' ):
        ''' Class constructor. It is constructed from its real and imaginary parts (default) or from the module and phase components. Its mode of initialization can be selected using the 3rd argument mode as follows:
            - realimag: real and imaginary components
            - modphase: module and phase components
            
            By default, the constructor uses floats.
            Default constructor:
            real  = 0.0
            imag  = 0.0
            mod   = 0.0
            phase = 0.0'''
        
        self.repr = 'realimag'
        
        if mode == 'realimag':
            self.real  = float( arg1 )
            self.imag  = float( arg2 )
            self.mod   = sqrt( self.real**2 + self.imag**2 )
            self.phase = atan( self.imag/self.real ) if self.real else sign( self.imag ) * 0.5 * pi if self.imag else 0.
        
        elif mode == 'modphase':
            self.mod   = float( arg1 )
            self.phase = float( arg2 )
            self.real  = self.mod * cos( self.phase )
            self.imag  = self.mod * sin( self.phase )
        
        else:
            raise TypeError('Could not initialize Complex: invalid mode of initialization')

    
    def __add__(self, other):
        ''' Sum operation with another number, complex or not.'''

        if not isinstance( other, Complex ):
            return Complex( self.real + other, self.imag )
        
        return Complex( self.real + other.real, self.imag + other.imag )
    
    def __radd__( self, number ):
        return self + number
    
    def __mul__( self, other ):
        ''' Product operation with another number, complex or not.'''

        if not isinstance( other, Complex ):
            return Complex( self.mod * other, self.phase, 'modphase' )
        return Complex( self.mod * other.mod, self.phase + other.phase, 'modphase' )
    
    def __rmul__( self, number ):
        return self * number
    
    def __sub__( self, other ):
        ''' Substraction operation with another number, complex or not.'''
        
        return self + ( - other )
    
    def __div__( self, other ):
        ''' Division operation with another number, complex or not.'''
        
        if not isinstance( other, Complex ):
            return Complex( self.mod/other, self.phase, 'modphase' )
        
        return self * other.Inverse()
    
    def __rdiv__( self, number ):
        ''' Right side division operation.'''
        
        return self.Inverse() * number

    def __neg__( self ):
        ''' Returns the complex number with the opposite sign.'''
        
        return Complex( self.mod, self.phase + pi, 'modphase' )
    
    def __abs__( self ):
        ''' Returns the module of the complex number.'''
    
        return self.mod
    
    def __round__( self, n ):
        ''' Performs rounding operation on the components.'''
    
        self.real  = round( self.real  , n )
        self.imag  = round( self.imag  , n )
        self.mod   = round( self.mod   , n )
        self.phase = round( self.phase , n )
    
    def __floor__( self, n ):
        ''' Performs rounding down on the components.'''
        
        self.real  = floor( self.real  , n )
        self.imag  = floor( self.imag  , n )
        self.mod   = floor( self.mod   , n )
        self.phase = floor( self.phase , n )
    
    def __ceil__( self, n ):
        ''' Performs rounding up on the components.'''
        
        self.real  = ceil( self.real  , n )
        self.imag  = ceil( self.imag  , n )
        self.mod   = ceil( self.mod   , n )
        self.phase = ceil( self.phase , n )

    def __complex__( self ):
        ''' Conversion to python complex class.'''
        
        return self.real + self.imag * 1.j
    
    def __repr__( self ):
        ''' Representation of the number. Returns a string with the Complex number in real-imaginary (default) or the module-phase representations. To change the type of the representation use the "SetRepresentation" method.'''
        
        if self.repr == 'realimag':
            return str(self.real) + ' + ' + str(self.imag) + 'i' if self.imag>=0 else str(self.real) + ' - ' + str(-self.imag) + 'i'
        
        if self.repr == 'modphase':
            return str(self.mod) + ' * exp ' + str(self.phase/pi) + ' pi i'
    
        if self.repr == 'all':
            self.repr = 'realimag'
            ri = self.__repr__()
            self.repr = 'modphase'
            mp = self.__repr__()
            self.repr = 'all'
            return ri + '  =  ' + mp
    
    def Re(self):
        ''' Returns the real part of the Complex number.'''
        return self.real
    
    def Im(self):
        ''' Returns the imaginary part of the Complex number.'''
        return self.imag
    
    def SetRepresentation( self, value ):
        ''' Sets the mode of representation. Options:
            - realimag: real-imaginary representation
            - modphase: module-phase representation
            - all: both representations at the same time.'''
        
        self.repr = str(value)

    def star( self ):
        ''' Changes the sign of the imaginary part without building a new object.'''
        
        self.imag  *= -1.
        self.phase *= -1.
    
    def Conj( self ):
        ''' Returns the Complex conjugate of the Complex number.'''
        
        return Complex( self.mod, 2*pi-self.phase, 'modphase' )
    
    def Inverse( self ):
        ''' Returns the inverse of the Complex number.'''
        return self.Conj()/self.mod**2



