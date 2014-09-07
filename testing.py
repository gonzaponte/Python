from Random import *
from ROOT import *
from time import clock

fr = FastRandom(11)
u = fr.Uniform
gr = GoodRandom(11)
u = gr.Uniform
#R = TRandom3()
#u = R.Uniform

h = TH1F('a','a',1000,0,1)

t0 = clock()

for i in xrange(10000000):
    h.Fill( u() )

print clock() - t0

h.SetMinimum(0)
h.SetLineWidth(2)
h.SetLineColor(1)
h.SetFillColor(2)
h.Draw()

raw_input()
