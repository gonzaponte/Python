from visual import *
from visual.graph import *
from math import *
from forces import *

def dr(p1,p2):
    return p1.pos - p2.pos

def r(p1,p2):
    return mag(dr(p1,p2))

def force(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**3

UA = 149597870700. # m
km = 1e3 # m

G   = 6.67384e-11
dt = 3600*6.

Msun     = 1.9890 * 1e30
Mmercury = 3.3020 * 1e23
Mvenus   = 4.8670 * 1e24
Mearth   = 5.9720 * 1e24
Mmars    = 6.4185 * 1e23
Mjupiter = 1.8990 * 1e27
Msaturno = 5.6880 * 1e26
Murano   = 8.6860 * 1e25
Mneptuno = 1.0240 * 1e26

Rsun     = 0.000000 * UA
Rmercury = 0.387500 * UA
Rvenus   = 0.723332 * UA
Rearth   = 1.000000 * UA
Rmars    = 1.523662 * UA
Rjupiter = 5.203363 * UA
Rsaturno = 9.537070 * UA
Rurano   = 19.22941 * UA
Rneptuno = 30.10366 * UA

rsun     = 696342 * km * 40
rmercury = 2439.8 * km * 1
rvenus   = 6052   * km * 1
rearth   = 6371   * km * 1
rmars    = 3397.2 * km * 1
rjupiter = 71492. * km * 1
rsaturno = 60268. * km * 1
rurano   = 25559. * km * 1
rneptuno = 24786. * km * 1

Vsun     =  0.0000 * km
Vmercury = 47.8725 * km
Vvenus   = 35.0214 * km
Vearth   = 29.7800 * km
Vmars    = 24.0770 * km
Vjupiter = 13.0697 * km
Vsaturno = 9.67240 * km
Vurano   = 6.81000 * km
Vneptuno = 5.47780 * km


sun     = sphere( pos=( Rsun    , 0.0, 0.0 ), radius = rsun    , color = color.yellow       , make_trail = True )
mercury = sphere( pos=( Rmercury, 0.0, 0.0 ), radius = rmercury, color = ( 0.4, 0.4, 0.4 )  , make_trail = True )
venus   = sphere( pos=( Rvenus  , 0.0, 0.0 ), radius = rvenus  , color = color.green        , make_trail = True )
earth   = sphere( pos=( Rearth  , 0.0, 0.0 ), radius = rearth  , color = color.blue         , make_trail = True )
mars    = sphere( pos=( Rmars   , 0.0, 0.0 ), radius = rmars   , color = color.red          , make_trail = True )
jupiter = sphere( pos=( Rjupiter, 0.0, 0.0 ), radius = rjupiter, color = color.orange       , make_trail = True )
saturno = sphere( pos=( Rsaturno, 0.0, 0.0 ), radius = rsaturno, color = ( 1.0, 0.3, 0.0 )  , make_trail = True )
urano   = sphere( pos=( Rurano  , 0.0, 0.0 ), radius = rurano  , color = color.cyan         , make_trail = True )
neptuno = sphere( pos=( Rneptuno, 0.0, 0.0 ), radius = rneptuno, color = ( 0.0, 0.0, 0.5 )  , make_trail = True )

sun    .mass = Msun
mercury.mass = Mmercury
venus  .mass = Mvenus
earth  .mass = Mearth
mars   .mass = Mmars
jupiter.mass = Mjupiter
saturno.mass = Msaturno
urano  .mass = Murano
neptuno.mass = Mneptuno

sun    .p = Msun     * Vsun     * vector(  0.0, 1.0, 0.0 )
mercury.p = Mmercury * Vmercury * vector(  0.0, 1.0, 0.0 )
venus  .p = Mvenus   * Vvenus   * vector(  0.0, 1.0, 0.0 )
earth  .p = Mearth   * Vearth   * vector(  0.0, 1.0, 0.0 )
mars   .p = Mmars    * Vmars    * vector(  0.0, 1.0, 0.0 )
jupiter.p = Mjupiter * Vjupiter * vector(  0.0, 1.0, 0.0 )
saturno.p = Msaturno * Vsaturno * vector(  0.0, 1.0, 0.0 )
urano  .p = Murano   * Vurano   * vector(  0.0, 1.0, 0.0 )
neptuno.p = Mneptuno * Vneptuno * vector(  0.0, 1.0, 0.0 )


planets = [ mercury, venus, earth, mars, jupiter, saturno, urano, neptuno ]
F       = range(8)

#f1 = gcurve( color = color.orange )
#gdisplay()
#f2 = gcurve( color = color.magenta )
#t=0
#histo = ghistogram( bins = arange(0,8,1), color = color.white, accumulate = True )

while True:
    rate(200)
#    f1.plot( pos = ( t, (earth.pos - venus.pos).mag ) )
#    f2.plot( pos = ( earth.pos - venus.pos )/UA )
#    t += dt
    for i in range(8):
        planet     = planets[i]
        F[i]       = force( G * sun.mass * planet.mass, sun, planet )
        planet.p   = planet.p - F[i]*dt
        planet.pos = planet.pos + planet.p/planet.mass*dt

    for i in range(8):
        planet = planets[i]
        if planet.pos.x>0 and planet.pos.y<1:
            pass#histo.plot( data = [i] )
            







