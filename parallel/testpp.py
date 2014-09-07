import ROOT,pp,time

t0 = time.time()

R = ROOT.TRandom3()
r = R.Gaus
H = ROOT.TH1F('a','a',1000,-1,1)

total = 10000000

def f(X):
    for x in X:
        H.Fill(x)

J = pp.Server()
job =[]
for i in range(4):
    d = [r(0,0.2) for i in xrange(total/4)]
    job += [J.submit(f,(d,)),(ROOT.TH1.Fill,),('ROOT',)]

#map( lambda x: x(), job)
#for i in [r(0,0.2) for i in xrange(total)]:
#    f(i)

H.SetLineWidth(2)
H.SetLineColor(1)
H.SetFillColor(9)
H.Draw()

t1 = time.time()

print t1 - t0
raw_input()
