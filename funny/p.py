from ROOT import *
from math import pi
c = TCanvas()

#expos = [ str(2*i + 1) for i in range(100) ]
#cosstring = map( lambda expo: "cos(x)^" + expo, expos )
#coses = [ TF1( cos, cos, -pi, pi ) for cos in cosstring ]
#map( lambda x: coses[x].SetLineColor(x+2), range(len(coses)))
#coses[0].Draw()
#map( lambda x: x.Draw('same'), coses[1:] )
#
#finalstr = str(1./len(coses)) + '* (' + reduce( lambda x,y: x + ' + ' + y, cosstring ) + ')'
#print finalstr
#
#cos = TF1( 'final', finalstr, -pi, pi )
#cos.SetLineColor(1)
#cos.SetLineWidth(4)
#cos.Draw('same')
#raw_input()

def factorial(n):
    return n*factorial(n-1) if n else 1.

N = 100
div  = [ '(' + str( (-1)**i/factorial(i) ) + ')' for i in range(N)]
expo = [ str(i) for i in range(N) ]
strs = map( lambda d,e: d + "*x^" + e, div, expo )
funs = [ TF1( cadea, cadea, 0, 4 ) for cadea in strs ]
map( lambda x: funs[x].SetLineColor(x+2), range(len(funs)))
funs[0].Draw()
map( lambda x: x.Draw('same'), funs[1:] )

final = reduce( lambda x,y: x + ' + ' + y, strs )

exp = TF1( 'final', final, 0, 4 )
exp.SetLineColor(1)
exp.SetLineWidth(4)
exp.Draw('same')
raw_input()
