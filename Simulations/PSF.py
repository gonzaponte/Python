from visual import *
from math import *
from RandomNumbers import LCG
from ROOT import TH1F,TH2F,TProfile,TCanvas,gStyle

R = LCG()

theta = pi/2.5
phi   = -pi/7
dir = ( sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta) )

r0 = .5
z0 = -5
Nphotons = int(1e4)
delta = 1.01


scene = display( title = 'PSF',
                 x = 0, y = 0,
                 width = 800, height = 600,
                 autoscale = False,
                 forward = dir,
                 range   = 40)

electron = sphere( pos = (0,0,z0),
                   radius = 1,
                   color = color.yellow )

tracking = box( pos = (0.,0.,0.),
                height = 50, width = 0.05, length = 50,
                color = color.white,
                opacity = 0.8)

photons = []
for i in range(Nphotons):
    ctheta = R.Uniform(-1,1)
    stheta = sqrt( 1 - ctheta**2 )
    phi = 2 * pi * R.Get()
    cphi = cos(phi)
    sphi = sin(phi)
    x = r0 * stheta * cphi
    y = r0 * stheta * sphi
    z = r0 * ctheta + z0
    newph  = sphere( pos = (x,y,z), radius = 0.1, color = color.blue )
    photons.append( newph )

gStyle.SetOptStat('')
c = TCanvas()
c.Divide(2)
h2 = TH2F('2','2',50,-25,25,50,-25,25)
h1 = TH1F('p','p',50,  0,25)
c.cd(1);h2.Draw('lego2');c.cd(2);h1.Draw()
def Fill( particle ):
    if particle.visible and particle.z > 0:
        h2.Fill( particle.x, particle.y )
        h1.Fill( (particle.x**2 + particle.y**2)**.5 )
        particle.visible = False
        c.cd(1);h2.Draw('lego2');c.cd(2);h1.Draw()
        c.Update()

while True:
    rate(2000)
    for photon in photons:
        photon.x *= delta
        photon.y *= delta
        photon.z  = ( photon.z - z0 ) * delta + z0
        Fill( photon )