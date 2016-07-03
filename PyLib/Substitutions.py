def BackSubstitution( matrix, coeffs ):
    n = len(coeffs)
    x = [0.] * n
    for i in reversed(range(n)):
	x[i] = coeffs[i] - sum( matrix[i][j] * x[j] for j in range(i+1,n) )
	x[i] /= matrix[i][i]
    return x

def ForwardSubstitution( matrix, coeffs ):
    n = len(coeffs)
    x = [0.] * n
    for i in range(n):
	x[i] = coeffs[i] - sum( matrix[i][j] * x[j] for j in range(i) )
	x[i] /= matrix[i][i]
    return x

def LU( matrix, eps = None ):
    A = map( list, matrix )
    Nrows = len(A)
    Ncols = len(A[0])
    scales = [ 1.0/max( map(abs,row) ) for row in A ]
    eps = 1e-15 / min(scales) if eps is None else eps
    
    P = Identity(Nrows) # Parity matrix
    for j in range(Ncols):
        for i in range(j):
            A[i][j] -= sum( A[i][k] * A[k][j] for k in range(i-1) )
        
        maximum = -1.0
        index   = None
        for i in range(j,Nrows):
            A[i][j] -= sum( A[i][k] * A[k][j] for k in range(j-1) )
            
            test = scales[i]*abs(A[i][j]) 
            if test >= maximum:
                maximum = test
                index   = i
        
        if j != index: # interchange rows
            A[index], A[j] = A[j], A[index]
            scales[inedex] = scales[j]
        
        P[index], P[j] = P[j], P[index]
        if not A[j][j]: A[j][j] = eps
        if j+1 < Nrows:
            for i in range(j+1,Nrows):
                A[i][j] /= A[j][j]

    L = Identity(Nrows)
    U = Zeros(Nrows,Ncols)
    for i in range(Nrows):
        for j in range(Ncols):
            M = L if i<j else U
            M[i][j] = A[i][j]
    
    return L,U,P

def LUsolve( A, B ):
    L, U, P = LU(A)
    Y = ForwardSubstitution( L, B )
    X = BackSubstitution( U, Y )
    return X

