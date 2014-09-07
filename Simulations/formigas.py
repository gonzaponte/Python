from visual import *
from math import *

def GetDirection( p1, p2 ):
    return vector( p2.x - p1.x, p2.y - p1.y, p2.z - p1.z )

# Some constants
l0 = 0.05
dt = 1e-2
c60 = cos(60*pi/180)
s60 = sin(60*pi/180)

def square():
    # Viewing
    scene = display( title = 'Ants simulation', x=0, y=0,center=(0.5,0.5,0) )
    
    # Initial state:

    f1 = pyramid( pos = ( 0, 0, 0 ), size = ( l0, l0, l0), color = color.red   , make_trail = True )
    f2 = pyramid( pos = ( 1, 0, 0 ), size = ( l0, l0, l0), color = color.blue  , make_trail = True )
    f3 = pyramid( pos = ( 0, 1, 0 ), size = ( l0, l0, l0), color = color.green , make_trail = True )
    f4 = pyramid( pos = ( 1, 1, 0 ), size = ( l0, l0, l0), color = color.yellow, make_trail = True )

    while True:
        rate(200)
        p1 = GetDirection( f1, f2 )
        p2 = GetDirection( f2, f3 )
        p3 = GetDirection( f3, f4 )
        p4 = GetDirection( f4, f1 )
        f1.pos += p1*dt
        f2.pos += p2*dt
        f3.pos += p3*dt
        f4.pos += p4*dt


def hexagon():
    scene = display( title = 'Ants simulation', x=0, y=0,center=(0.,0.,0. ) )
                    
    # Initial state:
    f1 = pyramid( pos = ( 1, 0, 0 ), size = ( l0, l0, l0), color = color.red   , make_trail = True )
    f2 = pyramid( pos = ( c60, s60, 0 ), size = ( l0, l0, l0), color = color.blue  , make_trail = True )
    f3 = pyramid( pos = ( -c60, s60, 0 ), size = ( l0, l0, l0), color = color.green , make_trail = True )
    f4 = pyramid( pos = ( -1, 0, 0 ), size = ( l0, l0, l0), color = color.yellow, make_trail = True )
    f5 = pyramid( pos = ( -c60, -s60, 0 ), size = ( l0, l0, l0), color = color.orange, make_trail = True )
    f6 = pyramid( pos = ( c60, -s60, 0 ), size = ( l0, l0, l0), color = color.magenta, make_trail = True )

    t = 0
    while t<10:
        t += dt
        rate(200)
        p1 = GetDirection( f1, f2 )
        p2 = GetDirection( f2, f3 )
        p3 = GetDirection( f3, f4 )
        p4 = GetDirection( f4, f5 )
        p5 = GetDirection( f5, f6 )
        p6 = GetDirection( f6, f1 )
        
        f1.pos += p1*dt
        f2.pos += p2*dt
        f3.pos += p3*dt
        f4.pos += p4*dt
        f5.pos += p5*dt
        f6.pos += p6*dt

    f1.visible = False
    f2.visible = False
    f3.visible = False
    f4.visible = False
    f5.visible = False
    f6.visible = False
    rate(200)
    raw_input()

def Nants( N ):
    scene = display( title = 'Ants simulation', x=0, y=0,center=(0.,0.,0. ) )
    colors = [color.red, color.blue, color.green, color.orange, color.magenta, color.cyan, color.yellow]*int(ceil(N/7.))
    # Initial state:
    fs = []
    arc = 2. * pi / N
    for i in range(N):
        fs += [ pyramid( pos = ( cos(i*arc), sin(i*arc), 0 ), size = ( l0, l0, l0), color = colors[i], make_trail = True ) ]
    
    t = 0
    N2 = N * N
    while t<N2:
        t += dt
        rate(200)
        ps = map( GetDirection, fs, fs[1:] + [fs[0]] )
        for i in range(len(fs)):
            fs[i].pos += ps[i]*dt
    for f in fs:
        f.visible = False

    rate(200)
    raw_input()

Nants(11)
