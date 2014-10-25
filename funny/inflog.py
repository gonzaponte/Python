from math import log,exp
from ROOT import TH1I

def inflog(x):
  while x>0:
    x = log(x)
  return -x
  

h = TH1I('a','a',100000,0.,1)
for i in xrange(1,100000):
    k = h.Fill( inflog(i) )

h.Draw()
