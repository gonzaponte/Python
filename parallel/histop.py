from ROOT import *
import pp,time,math


e = 2.718281828
h = TH1F('a','a',100,0,1)
total=100000
random = TRandom3()
r = random.Uniform

def F(n):
    h.Fill(n)

def convert(n):
    n *= 2.718281828-1
    n += 1
    return math.log(n)

#J = pp.Server()
#jobs=[]
#t0 = time.time()
#
#for i in xrange(total):
#    jobs += [J.submit( convert,(r(),),(), ("math",) )]
#
#map( lambda x: F(x()), jobs)
#t1 = time.time()
#
#h.Draw()
#h.SetMinimum(0)
#print t1-t0
#raw_input()

t0 = time.time()
jobs=[]
for i in xrange(total):
    jobs += [convert(r())]

map( F, jobs )
t1 = time.time()

h.Draw()
h.SetMinimum(0)
print t1-t0
raw_input()

