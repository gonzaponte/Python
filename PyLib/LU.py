from Array import *

def BackSubstitution( A, B ):
    n = len(B)
    x = B.Copy()
    for i in reversed(range(n)):
	x[i] -= sum( A[i][j] * x[j] for j in range(i+1,n) )
	x[i] /= A[i][i]
    return x

def ForwardSubstitution( A, B ):
    n = len(B)
    x = B.Copy()
    for i in range(n):
	x[i] -= sum( A[i][j] * x[j] for j in range(i) )
	x[i] /= A[i][i]
    return x

def LU( A, eps = None ):
    A = A.Copy()
    Nrows, Ncols = A.Size()
    scales = [ 1.0/max( map(abs,row) ) for row in A ]
    eps = 1e-15 / min(scales) if eps is None else eps
    
    P = Identity(Nrows) # Parity matrix
    for j in range(Ncols):
        print 'IN', j
        print A
        print P
        for i in range(j):
            A[i][j] -= sum( A[i][k] * A[k][j] for k in range(i) )
        
        maximum = -1.0
        index   = None
        for i in range(j,Nrows):
            A[i][j] -= sum( A[i][k] * A[k][j] for k in range(j) )
            print i,j,A[i][j]
            test = scales[i]*abs(A[i][j]) 
            if test >= maximum:
                maximum = test
                index   = i
        
        if j != index: # interchange rows
            A[index], A[j] = A[j], A[index]
            scales[index], scales[j] = scales[j], scales[index]
        print 'permuting ',index, j
        P[index], P[j] = P[j], P[index]
        if not A[j][j]: A[j][j] = eps
        for i in range(j+1,Nrows):
            A[i][j] /= A[j][j]

    L = Identity(Nrows)
    U = Zeros(Nrows,Ncols)
    for i in range(Nrows):
        for j in range(Ncols):
            M = L if i<j else U
            M[i][j] = A[i][j]
    print 'A'
    print A  
    print 'P'
    print P  
    return L, U, P

def LUsolve( A, B ):
    L, U, P = LU(A)
    B = P ** B
    B = B.T()
    if isinstance(B,Matrix):
        return Matrix(*[ BackSubstitution( U, ForwardSubstitution( L, b ) ) for b in B ] )
    return BackSubstitution( U, ForwardSubstitution( L, B ) )

def LUinverse( A ):
    Nrows, Ncols = A.Size()
    assert Nrows == Ncols, 'Matrix must be square!'
    return LUsolve(A,Identity(Nrows)).T()


A0 = Matrix([1.,2.,-1.],[2.,4.,5.],[3.,-1.,-2.])
B0 = Vector(2.,25.,-5.)

print A0.Inverse('GJ')
print A0.Inverse('LU')
