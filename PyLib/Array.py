'''
    Contains definitions of array-like objects and some related functions.
'''
from __future__ import division
from copy import copy as _copy, deepcopy as _deepcopy
from operator import add as _addition, mul as _multiplication, truediv as _division
from math import ceil, floor, trunc, sqrt, acos as _acos

class Vector:
    
    def __init__( self, *values ):
        '''
            Constructor. Takes as many arguments as desired. Copy constructor is also implemented. The arithmetic operators are defined to be applied element by element. Special operations have special syntax:
            - Dot product is the __pow__ method (** operator).
            - Appending values is performed using the Add method.
            ...
        '''
        
        self.values = _deepcopy(list(values))
        self.length = len(self.values)
    
    def __add__( self, other ):
        '''
            Addition operation.
        '''
        if isinstance( other, self.__class__ ):
            return self.__class__( *map( _addition, self.values, other.values) )
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
            return self.__class__( *map( _multiplication, self.values, other.values) )
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
            return self.__class__( *map( _division, self.values, other.values) )
        return self.__class__( *[ v / other for v in self.values ])

    def __truediv__( self, other ):
        '''
            True division operation. Same as __div__.
        '''
        return self.__div__( other )

    def __rdiv__( self, number ):
        '''
            Division operation. Same as __div__.
        '''
        return self.__class__( *[ other / v for v in self.values ] )
    
    def __getitem__( self, index ):
        '''
            Returns the specified element "index".
        '''
        if isinstance( index, (list,tuple,Vector) ):
            return self.__class__( *[ self.__getitem__(i) for i in index ] )
        if isinstance( index, slice ):
            return self.__class__( *self.values[index] )
        return self.values[index]
    
    def __setitem__( self, index, value ):
        '''
            Assign "value" to item in "index".
        '''
        self.values[index] = value
    
    def __delitem__( self, index ):
        '''
            Remove item in index.
        '''
        del self.values[index]
        self.length -= 1
    
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

    def __floor__( self ):
        '''
            Floor-round operation to each element.
        '''
        return self.__class__( *map( floor, self.values ) )

    def __ceil__( self ):
        '''
            Ceil-round operation to each element.
        '''
        return self.__class__( *map( ceil, self.values ) )

    def __trunc__( self ):
        '''
            Truncation operation to each element.
        '''
        return self.__class__( *map( trunc, self.values ) )

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
        '''
            Append the argument to the vector.
        '''
        self.values.append( element )
        self.length += 1
    
    def Maxpos( self, Abs = None ):
        '''
            Return the index and value of the greatest value in the vector. If the argument "Abs" is not None, absolute values are applied.
        '''
        Abs = abs if Abs else (lambda x: x)
        maximum = Abs(self[0])
        maxpos  = 0
        for i in range(1,self.length):
            if Abs(self[i]) > maximum:
                maximum = Abs(self[i])
                maxpos = i
        return maxpos, maximum
    
    def Minpos( self, Abs = None ):
        '''
            Return the index and value of the smallest value in the vector. If the argument "Abs" is not None, absolute values are applied.
        '''
        Abs = abs if Abs else (lambda x: x)
        minimum = Abs(self[0])
        minpos  = 0
        for i in range(1,self.length):
            if Abs(self[i]) < minimum:
                minimum = Abs(self[i])
                minpos = i
        return minpos, minimum
    
    def Clear( self ):
        '''
            Sets all the values to 0.0 .
        '''
        self.values = _deepcopy(Zeros(self.length))

    def Copy( self ):
        '''
            Return a copy of the instance.
        '''
        return self.__class__( *self.values )

    def ToList( self ):
        '''
            Return the object as list representation.
        '''
        return list( self )

    def Insert( self, index, element ):
        '''
            Insert element in index.
        '''
        element = _deepcopy(element)
        self.values.insert(index,element)
        if isinstance(self,Matrix):
            self.rows += 1
        elif isinstance(self,Vector):
            self.length += 1

    insert = Insert

    def Pop(self,index=-1):
        '''
            Return index-th element and remove it from list.
        '''
        element = self[index]
        del self[index]
        return element

    

class Matrix( Vector ):
    
    def __init__( self, *values ):
        ''' 
            Constructor. Takes as many arguments as desired. Copy constructor is also implemented. The arithmetic operators are defined to be applied element by element. Special operations have special syntax:
            - Actual matrix product is the __pow__ method (** operator).
            - Appending rows/cols is performed with the AddRow / AddCol method.
            - Transposition is both T and Transpose methods.
            - Inverse matrix is the Inverse method.
            - Matrix dimensions is given with the Size method.
            - Diagonalization is performed with the Diagonalize method.
            ...
        '''
        self.values = Vector( *[Vector(*v) for v in values ])
        self.rows   = len( self.values    ) if self.values else 0
        self.cols   = len( self.values[0] ) if self.values else 0
    
    def __pow__( self, other ):
        '''
            Product operation with another matrix or vector.
        '''
        if isinstance( other, self.__class__ ):
            return self.__class__( *[ [ row ** col for col in other.T().values ] for row in self.values ] )
        elif isinstance( other, Vector ):
            return Vector( *[ row ** other for row in self.values ] )
    
    def __contains__( self, x ):
        '''
            Containment aasertion.
        '''
        return any( [ x in row for row in self.values ] )
    
    def __delitem__( self, index ):
        '''
            Remove index-th row.
        '''
        del self.values[index]
        self.rows -= 1

    def __str__( self ):
        '''
            User-friendly string representation of the matrix.
        '''
        return '\n|' + '|\n|'.join( map( str, self.values ) ) + '|'

    def IsSquare( self ):
        '''
            Square matrix assertion.
        '''
        return self.rows == self.cols
    
    def Diag( self ):
        '''
            Return the diagonal of the matrix.
        '''
        return Vector( *[ self[i][i] for i in range(self.rows) ] )
    
    def T(self):
        '''
            Matrix transposition.
        '''
        return self.__class__( *[ [ self[j][i] for j in range(self.rows) ] for i in range(self.cols) ] )
    
    def Transpose(self):
        '''
            Matrix transposition. Same as Matrix.T .
        '''
        return self.T()
    
    def Tr(self):
        '''
            Trace operation.
        '''
        return sum( self.Diag() )
    
    def Trace(self):
        '''
            Trace operation. Same as Matrix.Tr .
        '''
        return self.Tr()
    
    def AddRow( self, row ):
        '''
            Add a row to the matrix.
        '''
        assert isinstance( row, (list,tuple,Vector) ), TypeError('The added row must be a list/tuple/Vector instance')
        self.values.Add( Vector(*row) )
        self.rows += 1

    def AddCol( self, element ):
        '''
            Add a column to the matrix.
        '''
        assert isinstance( element, (list,tuple,Vector) ), TypeError( 'The added column must be a list/tuple/Vector instance' )
        for i in range( self.rows ):
            self.values[i].Add( element[i] )
        self.cols += 1

    def Maxpos( self, Abs = None ):
        '''
            Find the indices and value of the largest element in the matrix. Set optional value Abs to true to disregard signs.
        '''
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
        '''
            Find the indices and value of the smallest element in the matrix. Set optional value Abs to true to disregard signs.
        '''
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
        '''
            Sets all the values to 0.
        '''
        map( Vector.Clear, self.values )
    
    def Size( self ):
        '''
            Dimensions of the matrix.
        '''
        return self.rows, self.cols

    def Diagonalize( self, p=1e-4 ):
        '''
            Perform the matrix diagonalization. Returns the diagonalized matrix (D) and a matrix of eigenvectors (V), been each row a eigenvector, i.e. A = VT ** D ** V.
        '''
        assert self.IsSquare(), ValueError('Only square matrices can be diagonalized')

        def findmax():
            maximum = 0.
            maxpos  = [ 0, 0 ]
            for i in range( self.rows ):
                for j in range( self.cols ):
                    if i==j:
                        continue
                    if abs( D[i][j] ) > maximum:
                        maximum = abs( D[i][j] )
                        maxpos  = [i,j]
            return maxpos
        
        def check():
            for i in range( self.rows ):
                for j in range( self.cols ):
                    if i==j:
                        continue
                    if abs( D[i][j] ) > p :
                        return True
            return False
        
        D  = self.Copy()
        V  = Identity( self.rows )
        
        while check():
            row, col = findmax()
            
            t = ( D[col][col] - D[row][row] ) / ( 2. * D[row][col] )
            s = -1. if t<0 else 1.
            t = s / ( abs(t) + sqrt( t**2 + 1. ) )
            c = 1. / sqrt( t**2 + 1. )
            s = c * t
            print D
            print t,c,s, row,col
            R = Identity( self.rows )
            R[row][row] =  c
            R[col][col] =  c
            R[row][col] =  s
            R[col][row] = -s
            
            D = R.T() ** ( D ** R )
            V = V ** R
        
        return D, V.T()

    def Inverse( self, method = 'GJ' ):
        '''
            Return the inverse of the matrix using the specified method. The available possibilities are:
            - GaussJordan      ==> GJ
            - LU decomposition ==> LU
        '''
        if method == 'GJ':
            return self._GaussJordan()
        elif method == 'LU':
            return self._LUInverse()
        else:
            return None

    def Det( self, method = 'Adj', **kwargs ):
        '''
            Compute the determinant of the matrix using the specified method. Moreover, keyword arguments may be given. The available possibilities are (with arguments):
            - Adjugate         ==> Adj ( row, col )
            - LU decomposition ==> LU  ()
        '''
        if method == 'Adj':
            return self._AdjugateDeterminant()
        elif method == 'LU':
            return self._LUDeterminant()
        else:
            return None

    def _GaussJordan(self):
        '''
            Performs matrix inversion using Gauss-Jordan elimination.
        '''
        new = self.Copy()
        sol = Vector( *range(self.rows) )
        for i in range( self.rows ):
            for j in range( self.cols ):
                new[i].Add( 1.0 if i == j else 0.0 )
    
        def findmax(x):
            max = abs(new[x][x])
            row = col = x
            for i in range( x, self.cols ):
                for j in range( x, self.cols ):
                    if abs( new[i][j] ) > max:
                        max = abs( new[i][j] )
                        row, col = i, j
            return row, col
    
        for i in range(self.cols):
            row, col = findmax(i)
            
            if not row == i: #interchange rows
                new[i], new[row] = new[row], new[i]
            
            if not col == i: #interchange cols
                sol[i], sol[col] = sol[col], sol[i]
                for k in range( self.cols ):
                    new[k][i], new[k][col] = new[k][col], new[k][i]
            
            for j in range( i+1, self.cols ):
                factor = new[j][i]/new[i][i]
                new[j] -= factor * new[i]
        
        for i in reversed(range(self.cols)):
            new[i] /= new[i][i]
            for j in range(i):
                new[j] -= new[j][i] * new[i]

        M = Zeros( self.cols, self.cols )
        for i in range( self.cols ):
            for j in range( self.cols ):
                M[sol[i]][j] = new[i][j+self.cols]

        return M
    
    def Pick( self, rows = [], cols = [] ):
        '''
            Return the selected rows and cols.
        '''
        M = self.Copy()
        
        if rows:
            for i in reversed(range(self.rows)):
                if not i in rows:
                    del M[i]
        M = M.T()
        
        if cols:
            for i in reversed(range(self.cols)):
                if not i in cols:
                    del M[i]
        M = M.T()
        
        return M
    
    def SubMatrix( self, row, col ):
        '''
            Return the submatrix correspondent to remove the row-th row and the col-th column.
        '''
        sub = self.Copy()
        del sub[row]
        sub = sub.T()
        del sub[col]
        return sub.T()
#    
#    def SwapRows( self, i, j ):
#        '''
#            Swap i-th and j-th rows.
#        '''
#        if j<i: i, j = j, i
#        self.Insert( i, self.Pop(j) )
#
#    def SwapCols( self, i, j ):
#        '''
#            Swap i-th and j-th rows.
#        '''
#        if j<i: i, j = j, i
#        self = self.T().Insert( i, self.Pop(j) )
#        self = self.T()

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
        '''
            Matrix with the cofactors.
        '''
        return Matrix( *[ [ self.Cofactor(i,j)  for j in range(self.cols)] for i in range(self.rows) ] )
    
    def Break( self, i, j = None ):
        '''
            Break the matrix into 4 blocks. Cuts just before i,j (not including them. Returns them in "z" order.
        '''
        j = i if j is None else j
        
        M1 = Zeros(             i,             j )
        M2 = Zeros(             i, self.cols - j )
        M3 = Zeros( self.rows - i,             j )
        M4 = Zeros( self.rows - i, self.cols - j )
        for row in range(self.rows):
            for col in range(self.cols):
                if   row<i and col<j:
                    M1[row][col] = self[row][col]
                elif row<i and col>=j:
                    M2[row][col-j] = self[row][col]
                elif row>=i and col<j:
                    M3[row-i][col] = self[row][col]
                elif row>=i and col>=j:
                    M4[row-i][col-j] = self[row][col]
        return M1, M2, M3, M4

    def _AdjugateDeterminant( self, row = None, col = None ):
        '''
            Return the determinant of the matrix. For ranges >= 4 a hint for adjugate decomposition may be used.
        '''
        assert self.IsSquare(), ValueError('The determinant can only be computed for a square matrix')
        
        # More efficient methods for ranges < 4.
        if   self.rows is 1:
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

    def Determinant( self, row = None, col = None ):
        '''
            Returns the determinant of the matrix. Same as Matrix.Det .
        '''
        return self.Det(row,col)

    def Symmetric( self ):
        '''
            Returns the simetric part.
        '''
        return 0.5 * ( self + self.T() )

    def AntiSymmetric( self ):
        '''
            Returns the antisimetric part.
        '''
        return 0.5 * ( self - self.T() )

    def Cholesky( self ):
        '''
            Cholesky decomposition.
        '''
        L = Zeros(self.rows,self.rows)
        for j in range(self.cols):
            for i in range(j,self.rows):
                L[i][j] = self[i][j] - sum( L[i][k] * L[j][k] for k in range(j) )
                if i == j:
                    L[i][j] **= 0.5
                else:
                    L[i][j] /= L[j][j]
        return L

    def LU( self ):
        '''
            Perform LU decomposition. Returns L-, U- and P-matrices.
        '''
        assert self.IsSquare(), ValueError('Matrix must be square.')
        
        P = Identity(self.rows)
        L = Identity(self.rows)
        U = self.Copy()

        for i in range(self.rows-1):
            max_index = U.T()[i][i:].Maxpos( Abs = abs )[0] + i
            if not i == max_index:
                U[i],U[max_index] = U[max_index], U[i]
                P[i],P[max_index] = P[max_index], P[i]
            for j in range(i+1,self.rows):
                factor = U[j][i] / U[i][i]
                U[j] -= U[i] * factor
                L[j][i] = factor

        return L,U,P

    def QR( self ):
        '''
            Compute QR decomposition. Returns Q- and R-matrices.
        '''
        Q = self.T()
        for i in range(self.cols):
            Qi = Q[i].Copy()
            for j in range(i):
                Q[i] -= ( Q[j] ** Qi ) * Q[j]
            Q[i] /= ( Q[i] ** Q[i] ) ** 0.5
            
        R = Q ** self
        return Q.T(), R

    def _LUInverse(self):
        '''
            Invert matrix using LU decomposition.
        '''
        L, U, P = self.LU()
        return U.Inverse('GJ') ** L.Inverse('GJ') ** P

    def _LUDeterminant(self):
        '''
            Compute determinant using LU decomposition.
        '''
        L, U, P = self.LU()
        return reduce( _multiplication, U.Diag() ) / P.Det('Adj')

    def ToList( self ):
        '''
            Return the object as list representation.
        '''
        return map( Vector.ToList, self.values )


class Vector3(Vector):
    '''
        Class dedicated for operatios in 3 or less dimensions.
    '''
    def __init__( self, x = 0., y = 0., z = 0. ):
        '''
            Initialize with a sequence or directly the components. Also works for 1 and 2 dimmensions.
        '''
        if isinstance( x, (list,tuple,Vector) ):
            x, y, z = x
        Vector.__init__( self, x, y, z )

    def __xor__( self, other ):
        '''
            Vector (i.e. inner) product.
        '''
        assert isinstance( other, Vector3 ), TypeError('The cross product must be performed with another 3-Vector')
        
        return Vector3( *[ +( self[1]*other[2] - self[2]*other[1] ),
                           -( self[0]*other[2] - self[2]*other[0] ),
                           +( self[0]*other[1] - self[1]*other[0] )] )

    def __abs__( self ):
        '''
            Magnitude.
        '''
        return sqrt( self ** self )

    def Unitary( self ):
        '''
            Unitary vector.
        '''
        return Vector3( self/abs(self) )
    
    def Unit( self ):
        '''
            Unitary vector. Same as Unitary().
        '''
        return self.Unitary()
    
    def Angle( self, other ):
        '''
            Angle between two 3 vectors.
        '''
        return _acos( self.Unit() ** other.Unit() )

    def RotationMatrix( self, axis = 'x' ):
        '''
            Returns the rotation matrix for transforming coordinates in the vector basis to the general basis.
        '''
        axis = axis.lower()
        u = self.Unit()
        v = Vector3( -u[1], u[0], 0 ).Unit()
        w = (u ^ v).Unit()
        M = Matrix( u, v, w ) if axis == 'x' else Matrix( v, u, w ) if axis == 'y' else Matrix( v, w, u ) if axis == 'z' else None
        return M.T()

class Vector4(Vector):
    '''
        Class dedicated for operatios in Minskowsky space.
    '''
    def __init__( self, E = 0., x = 0., y = 0., z = 0. ):
        '''
            Initialize with a sequence or directly the components. Also works for 1 and 2 dimmensions.
        '''
        if isinstance( E, (list,tuple,Vector) ):
            E, x, y, z = E
        Vector.__init__( self, E, Vector3( x, y, z ) )
        self.E = self.values[0]
        self.v = self.values[1]

    def __abs__( self ):
        '''
            Magnitude.
        '''
        return sqrt( self.E**2 - self.v ** self.v )

    def __str__( self ):
        '''
            String representation.
        '''
        return '( ' +  str(self.E) + ', ' + str(self.v) + ' )'

def Zeros( rows, cols = None ):
    '''
        Vector/Matrix filled with zeros.
    '''
    if cols:
        return Matrix( *( [ [0.] * cols ] * rows ) )
    return Vector( *([0.] * rows) )

def Ones( rows, cols = None ):
    '''
        Vector/Matrix filled with ones.
    '''
    return Zeros( rows, cols ) + 1.

def Identity( rows ):
    '''
        Rows x rows identity matrix.
    '''
    return Matrix( *[ [ 1. if j==i else 0. for j in range(rows) ] for i in range(rows) ])

def Diagonal( items ):
    '''
        Creates a diagonal matrix with elements in items.
    '''
    n = len(items)
    return Matrix( *[ [ items[i] if j==i else 0. for j in range(n) ] for i in range(n) ])

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

'''
from math import pi,cos,sin
from ROOT import *

#g = TGraph2D()
#g.SetMarkerStyle(20)
#g.SetMarkerSize(2)
theta = 45 * pi / 180
phi   = 45 * pi / 180

o  = Vector3(0,0,0)
x  = Vector3(1,0,0)
y  = Vector3(0,1,0)
z  = Vector3(0,0,1)
u0 = Vector3( sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta) )
v0 = Vector3(-sin(theta) * sin(phi), sin(theta) * cos(phi), 0          ).Unit()
w0 = ( u0 ^ v0 ).Unit()

M = u0.RotationMatrix('z')


h = TH3I('a','',*([100,-1,1]*3) ); h.SetMarkerStyle(20)
h.Fill( *(M**x) );h.Fill( *(M**y) );h.Fill( *(M**z) )
u = TPolyLine3D();u.SetPoint(0,*o);u.SetPoint(1,*u0);u.SetLineColor(kRed)
v = TPolyLine3D();v.SetPoint(0,*o);v.SetPoint(1,*v0);v.SetLineColor(kBlue)
w = TPolyLine3D();w.SetPoint(0,*o);w.SetPoint(1,*w0);w.SetLineColor(kGreen)

h.Draw()
u.Draw('same')
v.Draw('same')
w.Draw('same')

'''
