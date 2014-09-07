from General import *
from ROOT import *
from math import *

R = TRandom3(0)
U = R.Uniform
V = lambda x: U( -x, x )
T = lambda: acos( U()**4 )
P = lambda: 2. * pi * U()

dim = 200
i   = 0
h   = 100.

h1 = TH2F( 'higher','higher', dim, -dim, dim, dim, -dim, dim )
h2 = TH2F(  'lower', 'lower', dim, -dim, dim, dim, -dim, dim )

h1.SetMinimum(0)
h2.SetMinimum(0)

gStyle.SetOptStat('')
c = TCanvas()
c.Divide(1,2)
c.cd(1)
h1.Draw('zcol')
c.cd(2)
h2.Draw('zcol')
c.Update()
raw_input()



while i<1e8:
    i += 1
    
    x0, y0 = V(dim),V(dim)
    theta = T()
    phi   = P()

    x = h * tan(theta) * cos(phi)
    y = x * tan(phi)

    x += x0
    y += y0

    h1.Fill( x , y  )
    h2.Fill( x0, y0 )

    if not i % 5000:
        c.cd(1)
        h1.Draw('zcol')
        c.cd(2)
        h2.Draw('zcol')
        c.Update()
