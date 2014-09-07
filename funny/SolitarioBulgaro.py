from ROOT import TRandom3,TH1I
from time import clock

seed = int(10000*clock())
random = TRandom3()
random.SetSeed(seed)

k = 8
N = sum(range(k))
r = lambda k: k*random.Uniform() + 0.5

npasos = []
print 'N = ',N
for i in range(1000000):
    print 'paso ',i
    mazos = []
    M = int(N)
    while M:
        a = int(round( r(M) ))
        mazos.append( a )
        M -= a

    pasos = 0
    while not mazos==range(1,k):
        pasos += 1
        mazos = map( lambda x: x-1, mazos )
        mazos.append( len(mazos) )
        mazos = filter(lambda x: x, mazos)
        mazos.sort()

    npasos.append( pasos )

nbins = max(npasos) + 1
h = TH1I('a','a',nbins,0,nbins)
for i in npasos:
    h.Fill(i)

h.SetLineWidth(2)
h.SetLineColor(1)
h.SetFillColor(5)
h.Draw()
raw_input()