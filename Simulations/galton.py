from ROOT import *

R = TRandom3(0)
U = lambda: R.Uniform(-.5,.5)

rows = 16

def galton( nrows = rows, limit = 9 ):
    p = 0
    for i in range(nrows):
        p += 1 if p is -limit else -1 if p is limit + 1 else 1 if U()>0 else -1
    return p

def galton( nrows = rows, limit = 9 ):
    p = 0
    for i in range(nrows):
#        p += 1 if p is -limit else -1 if p is limit + 1 else 1 if U()>0 else -1
        u = U()
        p += 1 if u>0.166666666666666 else 0 if u>-0.166666666666666 else -1
    return p


h = TH1F('','',2*rows+1,-rows,rows+1)

for i in xrange(10000):
    h.Fill( galton() )

h.Draw()