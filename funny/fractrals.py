from ROOT import TGraph, TH2D, TCanvas
from RandomNumbers import MersenneTwister as MT

def Sierpinski():
    R = MT()
    G = TGraph()
    G.SetMarkerColor(9)
    C = TCanvas()
    
    N = 1e6
    x = 0.5
    y = x * 3**0.5
    
    p1 = (0,0)
    p2 = (1,0)
    p3 = (x,y)
    
    P = ( p1, p2, p3 )
    
    while True:
        x0, y0 = R.List(2)
        if x0 < 0.5 and y0 < x0 * 3**0.5:
            break
        if x0 > 0.5 and y0 < (1-x0) * 3**0.5:
            break
    
    update = 10
    for n in xrange(int(N) + 1):
        p = P[R.Integer(0,3)]
        x, y = 0.5 * ( p[0] + x0 ), 0.5 * ( p[1] + y0 )
        x0, y0 = x, y
        G.SetPoint(n,x,y)
        if not n % update:
            if n == 10 * update:
                update *= 10
            G.Draw('AP')
            C.Update()
    
    return G, C

def Fern():
    R = MT()
    G = TGraph()
    G.SetMarkerColor(9)
    C = TCanvas()
    
    N = 1e6
    x = 0.5
    y = 1.0
    
    update = 10
    for n in xrange(int(N) + 1):
        p = R.Get()
        if   0.00 <= p < 0.02:
            x, y = 0.5, 0.27 * y
        elif 0.02 <= p < 0.17:
            x, y = -.139 * x + .263 * y + .57, .246 * x + .224 * y -.036
        elif 0.17 <= p < 0.3:
            x, y = .17 * x - .215 * y + .408, .222 * x + .176 * y + .0893
        else:
            x, y = .781 * x + .034 * y + .1075, -.032 * x + .739 * y + .27
        
        G.SetPoint(n,x,y)
        if not n % update:
            if n == 10 * update:
                update *= 10
            G.Draw('AP')
            C.Update()
    return G, C

def Tree():
    R = MT()
    G = TGraph()
    G.SetMarkerColor(9)
    C = TCanvas()
    
    N = 1e6
    x = 0.5
    y = 1.0
    
    update = 10
    for n in xrange(int(N) + 1):
        p = R.Get()
        if   0.0 <= p < 0.1:
            x, y = .05 * x, 0.6 * y
        elif 0.1 <= p < 0.2:
            x, y = .05 * x, -.5 * y + 1.
        elif 0.2 <= p < 0.4:
            x, y = .46 * x - .15 * y, .39 * x + .38 * y + 0.6
        elif 0.4 <= p < 0.6:
            x, y = .47 * x - .15 * y, .17 * x + .42 * y + 1.1
        elif 0.6 <= p < 0.8:
            x, y = .43 * x + .28 * y, -.25 * x + .45 * y + 1.0
        else:
            x, y = .42 * x + .26 * y, -.35 * x + .31 * y + 0.7
        
        G.SetPoint(n,x,y)
        if not n % update:
            if n == 10 * update:
                update *= 10
            G.Draw('AP')
            C.Update()
    
    return G, C

def Ballistic():
    R = MT()
    N = int(1e4)
    M = 200
    X = 6*N//M
    
    C = TCanvas()
    H = TH2D( 'BD', '', M, 0, M, X, 0, X )
    H.SetMarkerColor(9)
    H.SetMarkerStyle(20)
    H.SetMarkerSize(0.5)
    A = [ [float('inf')] + [0]*M + [float('inf')]  for i in range(X) ]

    def GetHeight(x):
        for i,row in enumerate(A):
            if row[x]:
                break
        return i

    update = 10
    for n in xrange(int(N)+1):
        x = R.Integer(1,M+1)
        y = min( GetHeight(x-1), GetHeight(x)-1, GetHeight(x+1) ) - 1
        A[y][x] = 1
        H.Fill(x-1,X-1-y)
        
        if not n % update:
            if n == 10 * update:
                update *= 10
            H.Draw()
            C.Update()

    return H, C

a = Sierpinski()
b = Fern()
c = Tree()
d = Ballistic()
