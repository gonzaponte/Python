from math import *
from ROOT import *
from time import clock
import os

initialtime = clock()
print '\n'
print 'Defining variables...\n'

# Constants
N     = int(round(1e-8 * 1e23))
t12   = 3600 * 24 * 365.25 * 30.23
l     = log(2) / t12
tau   = 1. / l
A     = l * N
dt    = 1e-7
steps = int(round(1e9))
P     = 1 - exp( - N * l * dt )
binw  = 300
f     = TFile('desintegracion.root','RECREATE')
p     = TH1I('poisson','poisson',binw/6,0,binw/6)
e     = TH1F('exponential','exponential',25,0,0.00001)

r = TRandom3()

print 'Number of nuclei     = ', N
print 'Half life (years)    = ', t12 / ( 3600 * 24 * 365.25 )
print 'Decay constant (s-1) = ', l
print 'Activity (Bq)        = ', A
print 'Emission probability = ', P
print 'Delta t (ns)         = ', dt * 1e9
print 'Number of steps      = ', steps
print ''
print 'Creating events...'

i = 1
n = 0
t = 0

while i<=steps:
    if not i % binw:
        p.Fill( n )
        n=0
    if r.Rndm() < P:
        e.Fill( i * dt - t )
        n += 1
        t = i * dt
    i += 1

print 'Ready! Saving histograms...'

c = TCanvas()
gStyle.SetOptStat(1111111)
p.Draw()
c.SaveAs('poisson.pdf')
e.Draw()
c.SaveAs('exponential.pdf')
f.Write()

print 'Total time of execution (s): ',clock() - initialtime

os.system('open poisson.pdf')
os.system('open exponential.pdf')