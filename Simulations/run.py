from __future__ import division
from functions import *
from Array import Vector,Vector3,Matrix
from RandomNumbers import MersenneTwister
from operator import add
import visual

R = MersenneTwister()
U = R.Uniform

class Particle:
    '''
        A particle.
    '''
    def __init__( self, id, pos, v, r = 0.1 ):
        self.id  = id
        self.pos = pos
        self.p   = v
        self.F   = Vector3(0.,0.,0.)
        self.sph = visual.sphere( pos = visual.vector(tuple(pos)),
                                  p   = visual.vector(tuple(v)),
                                  radius = r,
                                  color  = visual.color.red )

    def Update( self ):
        self.sph.pos = visual.vector( tuple(self.pos) )

class System:
    '''
        The whole system.
    '''
    def __init__( self, NCellsPerDimension, Length, E0 ):
        self.n   = NCellsPerDimension
        self.L   = Length
        self.V   = self.L**3
        self.N   = 4 * self.n**3
        self.a   = self.L / self.n
        self.E0  = E0
        self.E   = E0
        self.U   = 0
        self.dU  = 0
        self.ddU = 0
        self.particles = []
        self.index = 0
        self.dt    = 1e-2
        self.dt_2  = self.dt * 0.5
        self.dt2_2 = self.dt * self.dt_2
    
        self.scene = visual.display( title = 'System',
                                     x=800, y=0,
                                     width=800, height=800,
                                     center = visual.vector(0.5,0.5,0.5) * self.L,
                                     autoscale = False,
                                     range = 1.5 * self.L)
    
        self.box   = visual.box( pos     = visual.vector(0.5,0.5,0.5) * self.L,
                                 length  = self.L,
                                 height  = self.L,
                                 width   = self.L,
                                 color   = visual.color.green,
                                 opacity = 0.2 )
    
    def GenerateInitialState( self ):
        for k in range(self.n):
            k += .25
            for j in range(self.n):
                j += .25
                for i in range(self.n):
                    i += .25
                    self.SetParticle( Vector3( i     , j     , k      ) * self.a,  Vector3( U(-1,1), U(-1,1), U(-1,1) ) )
                    self.SetParticle( Vector3( i + .5, j     , k + .5 ) * self.a,  Vector3( U(-1,1), U(-1,1), U(-1,1) ) )
                    self.SetParticle( Vector3( i + .5, j + .5, k      ) * self.a,  Vector3( U(-1,1), U(-1,1), U(-1,1) ) )
                    self.SetParticle( Vector3( i     , j + .5, k + .5 ) * self.a,  Vector3( U(-1,1), U(-1,1), U(-1,1) ) )
        
        extraP = self.P() / self.N
        for i in range(self.N):
            self.particles[i].p -= extraP

        self.LJ()
        if self.E0>0 or self.E0 < self.U:
            raise ValueError('Wrong value for system energy. It must be in the range [pot. energy, 0) = [{0},0)'.format(self.U) )

        scalefactor = ( (self.E0 - self.U ) / self.K() )**0.5
        for particle in self.particles:
            particle.p *= scalefactor
        
    def SetParticle( self, position, velocity ):
        self.particles.append( Particle( self.index, position, velocity, 0.1 * self.a ) )
        self.index += 1

    def Rho( self ):
        return self.N / self.V

    def P( self ):
        return reduce( add, [ particle.p for particle in self.particles ] )

    def F( self ):
        return reduce( add, [ particle.F for particle in self.particles ] )

    def K( self ):
        return 0.5 * sum( map( lambda particle: particle.p ** particle.p, self.particles ) )

    def LJ( self ):
        self._Reset()
    
        for i,p_i in enumerate(self.particles):
            for j,p_j in enumerate(self.particles[i+1:]):
                dir   = p_i.pos - p_j.pos
                dr    = abs(dir)
                dir   = dir.Unitary()
                dr2   = dr ** dr
                idr2  = 1. / dr2
                idr6  = idr2**3
                idr12 = idr6**2
                F     = 24 * ( 2 * idr12 - idr6 ) * idr2 * dir

                self.U   += +1.0 * idr12 - 1.0 * idr6
                self.dU  += -2.0 * idr12 + 1.0 * idr6
                self.ddU += 26.0 * idr12 - 7.0 * idr6

                p_i.F += F
                p_j.F -= F

        self.U  *= 4
        self.dU *= 8 / self.V
        self.ddU *= 8./3. / self.V**2
    
    def Verlet( self ):
        for particle in self.particles:
            particle.pos += particle.p * self.dt + particle.F * self.dt2_2
            particle.p   += particle.F * self.dt_2
        
        self.LJ()
            
        for particle in self.particles:
            particle.p += particle.F * self.dt_2
    
    def Advance( self, Nsteps = 1 ):
        for step in range(Nsteps):
            self.Verlet()
        map( Particle.Update, self.particles )
    
    def _Reset( self ):
        self.U = self.dU = self.ddU = 0.0
        for particle in self.particles:
            particle.F *= 0.


system = System(2,5.,-2.20)
system.GenerateInitialState()

print system.N
print system.Rho()
print system.P()
print system.K()
print system.E
print system.U
while True:
    visual.rate(1000)
    system.Advance(1)