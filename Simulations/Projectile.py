from math import *
from ROOT import TCanvas,TLegend
from Plots import Graph, Graph2

class ProjectileMotion:
    '''
        Compute motion of a projectile in 3D.
    '''
    def __init__( self, x0 = 0., y0 = 0., z0 = 0., v0 = 0., theta = 0., phi = 0., dt = 1e-3 ):
        self.x0  = x0
        self.y0  = y0
        self.z0  = z0
        self.v0  = v0
        self.th  = pi / 2 - theta * pi / 180.
        self.phi = phi * pi / 180.
        self.dt  = dt
        
        self.data = {'t':[],'x':[],'y':[],'z':[],'vx':[],'vy':[],'vz':[]}

    def Compute( self, condition = 'z>=0', drag = 0., density = False, gravity = False, coriolis = False ):
        g  = 9.807
        x  = self.x0
        y  = self.y0
        z  = self.z0
        vx = self.v0 * sin( self.th ) * cos( self.phi )
        vy = self.v0 * sin( self.th ) * sin( self.phi )
        vz = self.v0 * cos( self.th )
        
        t = 0.
        while eval(condition):
            self.data['t'] .append( t )
            self.data['x'] .append( x )
            self.data['y'] .append( y )
            self.data['z'] .append( z )
            self.data['vx'].append( vx )
            self.data['vy'].append( vy )
            self.data['vz'].append( vz )
            
            densityfactor = ( 1. - 6.5e-3 * z / 300. )**2.5 if density else 1.
            gravityfactor = ( 1 + z / 6378000. )**-2 if gravity else 1.
            coriolisfactor = 2 * 3.636e-5 if coriolis else 0.
            
            v   = sqrt( vx**2 + vy**2 + vz**2 )
            x  += vx * self.dt
            y  += vy * self.dt
            z  += vz * self.dt
            vx -= ( densityfactor * drag * v * vx - coriolisfactor * vy ) * self.dt
            vy -= ( densityfactor * drag * v * vy + coriolisfactor * vx ) * self.dt
            vz -= ( densityfactor * drag * v * vz + gravityfactor  * g  ) * self.dt
            
            t += self.dt
        
        return x

    def Graph( self, x, y, z = None, color = 1 ):
        return Graph( self.data[x], self.data[y], x, y, '', 20, 1, color ) if z is None else Graph2( self.data[x], self.data[y], self.data[z], x, y, z, '', 20, 1, color )

    def Clear( self ):
        for key in self.data:
            self.data[key] = []

'''
gvacuum = {}
gair = {}
colors = {45:1,35:2,25:3,15:4,55:6}
opt = 'AC'
for theta in [45,35,25,15,55]:
    proj = ProjectileMotion( v0 = 700., theta = theta, dt = 5e-2 )
    proj.Compute( drag = 0. )
    gvacuum[theta] = proj.Graph('x','z', color = colors[theta]); gvacuum[theta].SetLineWidth(2)
    gvacuum[theta].Draw(opt)
    opt = 'sameC'
    del proj

for theta in [45,35,25,15,55]:
    proj = ProjectileMotion( v0 = 700., theta = theta, dt = 5e-2 )
    proj.Compute( drag = 4e-5 )
    gair[theta] = proj.Graph('x','z', color = colors[theta]); gair[theta].SetLineWidth(2); gair[theta].SetLineStyle(3)
    gair[theta].Draw(opt)
    opt = 'sameC'
    del proj
'''


proj = ProjectileMotion( v0 = 700., theta = 45., dt = 5e-2 )

proj.Compute( drag = 0., density = False, gravity = False )
gideal = proj.Graph('x','z',color = 1); gideal.SetLineWidth(2)
proj.Clear()

proj.Compute( drag = 4e-5, density = False, gravity = False )
gdrag = proj.Graph('x','z',color = 2); gdrag.SetLineWidth(2)
proj.Clear()

proj.Compute( drag = 4e-5, density = True, gravity = False )
gdensity = proj.Graph('x','z',color = 3); gdensity.SetLineWidth(2)
proj.Clear()

proj.Compute( drag = 0., density = False, gravity = True )
ggrav = proj.Graph('x','z',color = 4); ggrav.SetLineWidth(2)
proj.Clear()

proj.Compute( drag = 0., density = False, gravity = False, coriolis = True )
gcor = proj.Graph('x','z',color = 9); gcor.SetLineWidth(2)
proj.Clear()

proj.Compute( drag = 4e-5, density = True, gravity = True, coriolis = True )
gall = proj.Graph('x','z',color = 5); gall.SetLineWidth(2)
proj.Clear()


gideal.Draw('AC')
gdrag.Draw('sameC')
gdensity.Draw('sameC')
ggrav.Draw('sameC')
gcor.Draw('sameC')
gall.Draw('sameC')

raw_input()



