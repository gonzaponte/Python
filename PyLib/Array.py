'''
    Contains definitions of array-like objects and some related functions.
'''

import copy
import operator
import math

class Vector:
    
    def __init__( self, *values ):
        '''
            Constructor. Takes as many arguments as desired. Copy constructor is also implemented. The arithmetic operators are defined to be applied element by element. Special operations have special syntax:
            - Dot product is the __pow__ method (** operator).
            - Appending values is performed with the Add method.
            ...
        '''
        
        # If only one value in "values" take it: avoid list( list( stuff ) )
        data = list(values[0]) if len(values) is 1 and isinstance( values[0], (list,tuple,Vector) ) else list(values)
        self.values = copy.deepcopy(data)
        self.length = len(self.values)
    
    def __add__( self, other ):
        '''
            Addition operation.
        '''
        if isinstance( other, self.__class__ ):
            return self.__class__( *map( operator.add, self.values, other.values) )
        return self.__class__( *[ v + other for v in self.values ])
    
    def __radd__( self, other ):
        '''
            Right-addition operation. Same as __add__.
        '''
        return self.__add__(other)
    
    def __sub__( self, other ):
        '''
            Substraction operation.
        '''
        return self.__add__( -other )
    
    def __rsub__( self, other ):
        '''
            Right-substraction operation. Same as __sub__.
        '''
        return other + self.__neg__()
    
    def __neg__( self ):
        '''
            Sign inversion.
        '''
        return self * -1
    
    def __mul__( self, other ):
        '''
            Multiplication operation.
        '''
        if isinstance( other, self.__class__ ):
            return self.__class__( *map( operator.mul, self.values, other.values) )
        return self.__class__( *[ v * other for v in self.values ])
    
    def __rmul__( self, number ):
        '''
            Right-multiplication operation. Same as __mul__.
        '''
        return self.__mul__( number )
    
    def __pow__( self, other ):
        '''
            Dot product operation.
        '''
        if isinstance( other, Matrix ):
            return Vector( *[self.__pow__( col ) for col in other.T()] )
        return sum( self.__mul__( other ).values )
    
    def __div__( self, other ):
        '''
            Division operation.
        '''
        if isinstance( other, self.__class__ ):
            return self.__class__( *map( operator.div, self.values, other.values) )
        return self.__class__( *[ v / other for v in self.values ])
    
    def __rdiv__( self, number ):
        '''
            Division operation. Same as __div__.
        '''
        return self.__class__( *[ other / v for v in self.values ] )
    
    def __getitem__(self,index):
        '''
            Returns the specified element "index".
        '''
        return self.values[index]
    
    def __setitem__(self,index,value):
        '''
            Assign "value" to item in "index".
        '''
        self.values[index] = value
    
    def __len__(self):
        '''
            Length of the vector.
        '''
        return self.length
    
    def __reversed__( self ):
        '''
            Reversed components.
        '''
        return self.__class__( *self.values[::-1])
    
    def __str__( self ):
        '''
            User-friendly string representation of the vector.
        '''
        return '< ' + ', '.join( ['{0:<+8.4e}'.format(v) for v in self.values] ) + ' >'
    
#    def __format__( self ):
#        '''
#            User-friendly string representation of the vector for new style string format.
#        '''
#        return self.__str__()
#
#    def __repr__( self ):
#        '''
#            More explicit string representation of the vector.
#        '''
#        return 'Vector ' + self.__str__()

    def __eq__( self, other ):
        '''
            Equality comparison of each value.
        '''
        return self.values == other.values if isinstance( other, self.__class__ ) else False
    
    def __gt__( self, other ):
        '''
            Greater than operator. Lengths comparison.
        '''
        return self.length > other.length if isinstance( other, self.__class__ ) else False

    def __lt__( self, other ):
        '''
            Lower than operator. Lengths comparison.
        '''
        return self.length < other.length if isinstance( other, self.__class__ ) else False

    def __ge__( self, other ):
        '''
            Greater of equal length.
        '''
        return self > other or self == other

    def __le__( self, other ):
        '''
            Lower or equal length.
        '''
        return self < other or self == other

#    def __float__( self ):
#        '''
#            Float conversion for each element.
#        '''
#        return self.__class__( *map( float, self.values ) )
#
#    def __round__( self ):
#        '''
#            Round operation to each element.
#        '''
#        return self.__class__( *map( round, self.values ) )

    def __floor__( self ):
        '''
            Floor-round operation to each element.
        '''
        return self.__class__( *map( math.floor, self.values ) )

    def __ceil__( self ):
        '''
            Ceil-round operation to each element.
        '''
        return self.__class__( *map( math.ceil, self.values ) )

    def __trunc__( self ):
        '''
            Truncation operation to each element.
        '''
        return self.__class__( *map( math.trunc, self.values ) )

    def __nonzero__( self ):
        '''
            Bool conversion.
        '''
        return True if self.length else False

    def Apply( self, function ):
        '''
            Apply "function" to each element.
        '''
        return self.__class__( *map( function, self.values ) )

    def append( self, *elements):
        '''
            Elements addition.
        '''
        if len(elements) is 1 and isinstance( elements[0], Vector ):
            map( self.Add, elements )

    def Add( self, element ):
        ''' Append the argument to the vector.'''
        self.values.append( element )
        self.length += 1
    
    def Maxpos( self, Abs = None ):
        ''' Return the index and value of the greatest value in the vector. If the argument "Abs" is not None, absolute values are applied.'''
        Abs = (lambda x: x) if Abs is None else abs
        maximum = Abs(self[0])
        maxpos  = 0
        for i in range(1,self.length):
            if Abs(self[i]) > maximum:
                maximum = Abs(self[i])
                maxpos = i
        return maxpos, maximum
    
    def Minpos( self, Abs = None ):
        ''' Return the index and value of the smallest value in the vector. If the argument "Abs" is not None, absolute values are applied.'''
        Abs = (lambda x: x) if Abs is None else abs
        minimum = Abs(self[0])
        minpos  = 0
        for i in range(1,self.length):
            if Abs(self[i]) < minimum:
                minimum = Abs(self[i])
                minpos = i
        return minpos, minimum
    
    def Clear( self ):
        ''' Sets all the values to 0.0 .'''
        
        self.values = copy.deepcopy(Zeros(self.length))

    def Copy( self ):
        return self.__class__( self.values )



class Matrix( Vector ):
    
    def __init__( self, *values ):
        ''' Constructor. Takes as many arguments as desired. Copy constructor is also implemented. The arithmetic operators are defined to be applied element by element. Special operations have special syntax:
            - Actual matrix product is the __pow__ method (** operator).
            - Appending rows/cols is performed with the AddRow / AddCol method.
            - Transposition is both T and Transpose methods.
            - Inverse matrix is the Inverse method.
            - Matrix dimensions is given with the Size method.
            - Diagonalization is performed with the Diagonalize method.
            ...'''

        data = list(values[0]) if len(values) is 1 and isinstance( values[0], (list,tuple,Vector,Matrix) ) else list(values)
        self.values = Vector( *map( Vector, data ) )
        self.rows = len( self.values    ) if self.values else 0
        self.cols = len( self.values[0] ) if self.values else 0
    
    def __pow__( self, other ):
        ''' Product operation with another matrix or vector.'''
        if isinstance( other, self.__class__ ):
            return self.__class__( *[ [ row ** col for col in other.T().values ] for row in self.values ] )
        elif isinstance( other, Vector ):
            return Vector( [ row ** other for row in self.values ] )
    
    def __contains__( self, x ):
        return any( [ x in row for row in self.values ] )

    def __str__( self ):
        ''' User-friendly string representation of the matrix.'''
        return '\n|' + '|\n|'.join( map( str, self.values ) ) + '|'
    
    def __repr__( self ):
        ''' More explicit string representation of the vector.'''
        
        return 'Matrix \n' + self.__str__()

    def IsSquare( self ):
        return self.rows is self.cols
    
    def T(self):
        ''' Matrix transposition.'''
        
        return self.__class__( *[ [ self[j][i] for j in range(self.cols) ] for i in range(self.rows) ] )
    
    def Transpose(self):
        return self.T()
    
    def Tr(self):
        return sum( [ self.values[i][i] for i in range(min(self.rows,self.cols)) ] )
    
    def Trace(self):
        return self.Tr()
    
    def AddRow( self, row ):
        if not isinstance( row, (list,tuple,Vector) ):
            raise TypeError( 'The added row must be a list/tuple/Vector instance' )
        self.values.Add( Vector(row) )
        self.rows += 1

    def AddCol( self, element ):
        if not isinstance( element, (list,tuple,Vector) ):
            raise TypeError( 'The added column must be a list/tuple/Vector instance' )
        for i in range( self.rows ):
            self.values[i].Add( element[i] )
        self.cols += 1

    def Maxpos( self, Abs = None ):
        maxrow, maxcol = 0, 0
        maximum = self[0][0]
        for i in range(self.rows):
            col, value = self.values[i].Maxpos( Abs )
            if value > maximum:
                maxrow = i
                maxcol = col
                maximum = value
        return maxrow, maxcol, maximum

    def Minpos( self, Abs = None ):
        minrow, mincol = 0, 0
        minimum = self[0][0]
        for i in range(self.rows):
            col, value = self.values[i].Minpos( Abs )
            if value < minimum:
                minrow = i
                mincol = col
                minimum = value
        return minrow, mincol, minimum

    def Clear( self ):
        ''' Sets all the coordinates to 0.'''
        map( Vector.Clear, self.values )
    
    def Size( self ):
        ''' Size of the matrix.'''
        return self.rows, self.cols

    def Diagonalize( self, p=1e-4 ):
        if not self.IsSquare():
            raise ValueError('Only square matrices can be diagonalized')

        def findmax():
            maximum = 0.
            maxpos  = [ 0, 0 ]
            for i in range( self.rows ):
                for j in range( self.cols ):
                    if i==j:
                        continue
                    if abs( self[i][j] ) > maximum:
                        maximum = abs( self[i][j] )
                        maxpos  = [i,j]
            return maxpos
        
        def check():
            for i in range( self.rows ):
                for j in range( i+1, self.cols ):
                    if abs( self[i][j] ) > p :
                        return False
            return True
        
        D  = Matrix( self )
        V  = Identity( self.rows )
        
        while not check():
            row, col = findmax( D )
            
            t = ( D[col][col] - D[row][row] ) / ( 2. * D[row][col] )
            t = Sign(t) / ( abs(t) + sqrt( t**2 + 1 ) )
            c = 1. / sqrt( t**2 + 1 )
            s = c * t
            
            R = Identity( self.rows )
            R[row][row] =  c
            R[col][col] =  c
            R[row][col] =  s
            R[col][row] = -s
            
            D = R.T() ** ( D ** R )
            V = V ** R
        
        return D, V

    def Inverse(self):
        
        new = Matrix(self)
        sol = Vector( range(self.rows) )

        for i in range( self.cols ):
            for j in range( self.cols ):
                if i==j:
                    new[i].Add(1.0)
                else:
                    new[i].Add(0.0)

        def findmax(x):
            max=abs(new[x][x])
            row=x
            col=x
            for i in range(x,self.cols):
                for j in range(x,self.cols):
                    if abs(new[i][j])>max:
                        max=abs(new[i][j])
                        row=i
                        col=j
            return row,col

        def interchangerows(a,b):
            for k in range(2*self.cols):
                new[a][k], new[b][k] = new[b][k], new[a][k]

        def interchangecols(a,b):
            sol[a], sol[b] = sol[b], sol[a]
            for k in range(self.cols):
                new[k][a], new[k][b] = new[k][b], new[k][a]
    
        for i in range(self.cols):
            row,col = findmax(i)
            interchangerows(i,row)
            interchangecols(i,col)
            
            for j in range(i+1,self.cols):
                factor = new[j][i]/new[i][i]
                for k in range(i,2*self.cols):
                    new[j][k] -= factor*new[i][k]

        for i in range(self.cols-1,-1,-1):
            
            factor = new[i][i]
            for j in range( i, 2*self.cols ):
                new[i][j] /= factor
            
            for j in range(i):
                factor = new[j][i]
                for k in range( i, 2*self.cols ):
                    new[j][k] -= factor * new[i][k]
        M = Zeros( self.cols, self.cols )

        for i in range( self.cols ):
            for j in range( self.cols ):
                M[sol[i]][j] = new[i][j+self.cols]

        return M

    def SubMatrix( self, row, col ):
        '''
            Return the submatrix correspondent to remove the row-th row and the col-th column.
        '''
        
        sub = Zeros(self.rows-1,self.cols-1)
        for i in range(self.rows):
            for j in range(self.cols):
                if   i < row and j < col:
                    sub[i][j] = self[i][j]
                elif i > row and j < col:
                    sub[i-1][j] = self[i][j]
                elif i < row and j > col:
                    sub[i][j-1] = self[i][j]
                elif i > row and j > col:
                    sub[i-1][j-1] = self[i][j]
        
        return sub

    def Minor( self, row, col ):
        '''
            Return the (row,col)-minor.
        '''
        return self.SubMatrix( row, col ).Det()

    def Cofactor( self, row, col ):
        '''
            Return the (row,col)-cofactor.
        '''
        return self.Minor( row, col ) * (-1)**(row+col)
    
    def CofactorsMatrix( self ):
        return Matrix( [ [ self.Cofactor(i,j)  for j in range(self.cols)] for i in range(self.rows) ] )

    def Det( self, row = None, col = None ):
        '''
            Return the determinant of the matrix. row and col parameters
        '''
        if not self.IsSquare():
            raise ValueError('The determinant can only be computed for a square matrix')
        
        # More efficient methods for ranges < 4.
        if self.rows is 1:
            return self[0][0]
        elif self.rows is 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
        elif self.rows is 3:
            det  = 0
            det += self[0][0] * self[1][1] * self[2][2]
            det += self[0][1] * self[1][2] * self[2][0]
            det += self[0][2] * self[1][0] * self[2][1]
            det -= self[0][2] * self[1][1] * self[2][0]
            det -= self[0][1] * self[1][0] * self[2][2]
            det -= self[0][0] * self[1][2] * self[2][1]
            return det
        else:
            if row is None:
                if col is None:
                    return sum([ self[i][0] * self.Cofactor(i,0) for i in range(self.rows) ])
                else:
                    return sum([ self[i][col] * self.Cofactor(i,col) for i in range(self.rows) ])
            else:
                return sum([ self[row][i] * self.Cofactor(row,i) for i in range(self.cols) ])

    def Determinant( self, row = None, col = None):
        return self.Det(row,col)

    def Simetric( self ):
        return 0.5 * ( self + self.T() )

    def AntiSimetric( self ):
        return 0.5 * ( self - self.T() )


class Vector3(Vector):

    def __init__( self, x = 0., y = 0., z = 0. ):
        if isinstance( x, (list,tuple,Vector) ):
            x, y, z = x
        Vector.__init__( self, x, y, z )

    def __xor__( self, other ):
        if not isinstance( other, Vector3 ):
            raise TypeError('The cross product must be performed with another 3-Vector')
        return Vector3( *[ +( self[1]*other[2] - self[2]*other[1] ),
                           -( self[0]*other[2] - self[2]*other[0] ),
                           +( self[0]*other[1] - self[1]*other[0] )] )

    def __abs__( self ):
        return math.sqrt( self ** self )

    def Unitary( self ):
        return Vector3( self/abs(self) )

    def Angle( self, other ):
        ''' Angle between two 3 vectors. Is 0 if one of them is 0.'''
        if not abs(self) or not abs(other):
            return 0.
        return math.acos( self.Unit() ** other.Unit() )


class Vector4(Vector):

    def __init__( self, E = 0., x = 0., y = 0., z = 0. ):
        Vector.__init__( self, E, Vector3( x, y, z ) )
        self.E = self.values[0]
        self.v = self.values[1]

    def __abs__( self ):
        return math.sqrt( self.E**2 - self.v ** self.v )

    def __str__( self ):
        return '( ' +  str(self.E) + ', ' + str(self.v) + ' )'


def Zeros( rows, cols = None ):
    '''
        Matrix filled with zeros.
    '''
    if cols:
        return Matrix( [ [0.] * cols ] * rows )
    return Vector( [0.] * rows )

def Ones( rows, cols = None ):
    '''
        Matrix filled with ones.
    '''
    return Zeros( rows, cols ) + 1.

def Identity( rows ):
    '''
        Identity matrix. Must be square.
    '''
    return Matrix( [ [ 1. if j==i else 0. for j in range(rows) ] for i in range(rows) ])

# examples and debug
if __name__ == '__main__':
    A = Vector( 1., 2., 3. )
    B = Vector( 6., 5., 4. )
    C = Matrix( ( 1., 2., 3.),
                ( 4., 5., 6.),
                ( 7., 8., 9.) )
    D = Matrix( ( 9., 8., 7.),
                ( 2., 1., 6.),
                ( 3., 4., 5.) )

    print 'A         =  ', A
    print 'B         =  ', B
    print 'A +  B    =  ', A +  B
    print 'A +  5    =  ', A +  5
    print '3 +  B    =  ', 3 +  B
    print 'A -  B    =  ', A -  B
    print 'A -  9    =  ', A -  9
    print '7 -  B    =  ', 7 -  B
    print 'A *  B    =  ', A *  B
    print 'A *  4    =  ', A *  4
    print '2 *  B    =  ', 2 *  B
    print 'A ** B    =  ', A ** B
    print 'A[1]      =  ', A[1];    A[1] = 0
    print 'A[1]=0    => ', A
    print 'len(A)    =  ', len(A)

    print 'C         =  ', C
    print 'D         =  ', D
    print 'C +  D    =  ', C +  D
    print 'C +  5    =  ', C +  5
    print '3 +  D    =  ', 3 +  D
    print 'C -  D    =  ', C -  D
    print 'C -  9    =  ', C -  9
    print '7 -  D    =  ', 7 -  D
    print 'C *  D    =  ', C *  D
    print 'C *  4    =  ', C *  4
    print '2 *  D    =  ', 2 *  D
    print 'C ** D    =  ', C ** D
    print 'C ** B    =  ', C ** B
    print 'A ** D    =  ', A ** D
    print 'C[1][0]   =  ', C[1][0];    C[1][0] = 0
    print 'C[1][0]=0 => ', C
    print 'C.Size()   =  ', C.Size()


