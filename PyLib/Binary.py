'''
    A binary operation toolbox. Contains the usual binary operations.
'''

import operator

def Bit( boolean ):
    '''
        Return the bit corresponding to boolean.
    '''
    return str( int( boolean ) )

def Bool( bit ):
    '''
        Return the boolean corresponding to bit.
    '''
    return bool( int( bit ) )

def Padding( number, nbits, side = 'left' ):
    '''
        Pad with zeros to complete nbits. Add those zeros to the input side.
    '''
    zeros = '0' * ( nbits - len(number) )
    return zeros + number if side == 'left' else number + zeros

def MakeCompatible( *args ):
    '''
        Return the arguments with sharing format.
    '''
    nbits = max( map( len, args ) )
    return [ Padding( arg, nbits ) for arg in args ]

def AND( b1, b2 ):
    '''
        And operation, i.e., for each bit position: 1 if both bits are 1, 0 otherwise.
    '''
    b1, b2 = MakeCompatible( b1, b2 )
    return ''.join( map( Bit, map( operator.and_, map( Bool, b1 ), map( Bool, b2 ) ) ) )

def OR( b1, b2 ):
    '''
        Or operation, i.e., for each bit position: 0 if both bits are 0, 1 otherwise.
    '''
    b1, b2 = MakeCompatible( b1, b2 )
    return ''.join( map( Bit, map( operator.or_, map( Bool, b1 ), map( Bool, b2 ) ) ) )

def XOR( b1, b2 ):
    '''
        Xor operation, i.e., for each bit position: 0 if both bits are the same, 1 otherwise.
    '''
    b1, b2 = MakeCompatible( b1, b2 )
    return ''.join( map( Bit, map( operator.xor, map( Bool, b1 ), map( Bool, b2 ) ) ) )

def NOT( b1 ):
    '''
        Not operation, i.e., for each bit: 1 if bit is 0, 0 if bit is 1.
    '''
    return ''.join( map( Bit, map( operator.not_, map( Bool, b1 ) ) ) )


a = '001010'
b = '011010'
print 'a   = ', a
print 'b   = ', b
print 'and = ', AND(a,b)
print 'or  = ', OR(a,b)
print 'xor = ', XOR(a,b)
print 'not = ', NOT( a )
print int(a)
print hex(int(a))

