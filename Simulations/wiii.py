from visual import *
from math import *

q0  = 1.602e-19
eps = 8.854e-12
c   = 299792458.
m0  = 1e6*q0/c**2
em  = q0**2./(4.*3.14159265*eps)
r0  = 5e-11
G   = 6.67e-11
g   = 9.81

def dr(p1,p2):
    return p1.pos - p2.pos
        
def r(p1,p2):
    return mag(dr(p1,p2))

def force(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**3

def H():
    dt  = 1e-17
    p0  = 2.7e2

    p   = sphere( pos=(0.0,0.0,0.0), radius = r0, color = color.red, make_trail=True, interval=10)
    e   = sphere( pos=(0.0,1e-9,0.0), radius = r0, color = color.blue, make_trail=True, interval=10)
    p.mass = 938.3*m0
    e.mass = 0.511*m0
    p.p = vector(0.0,0.0,+p0)*p.mass
    e.p = -p.p
    
    while True:
        rate(200)
        F = force(em,p,e)
        p.p = p.p + F*dt
        e.p = e.p - F*dt
        p.pos = p.pos + p.p/p.mass*dt
        e.pos = e.pos + e.p/e.mass*dt

def triangle():
    polygon(3)

def square():
    polygon(4)

def polygon(n):
    p   = []
    arc = 2*pi/n
    r   = 1e-9
    dt  = 2e-18
    for i in range(n):
        p.append( sphere( pos=( r*cos(i*arc), r*sin(i*arc), 0.0),
                         radius=r0/5,
                         color = color.red,
                         interval = 10 ) )
        p[i].mass=938.1*m0
        p[i].p = vector(0.0,0.0,0.0)
    e = sphere( pos=(0.0,0.0,r), radius = r0, color = color.blue, make_trail=True, interval=10)
    e.mass = 0.511*m0
    e.p = vector(0.0,0.0,0.0)
    while True:
        rate(200)
        F = vector(0.0,0.0,0.0)
        for P in p:
            F = F + force(em,P,e)
        e.p = e.p - F*dt
        e.pos = e.pos + e.p/e.mass*dt

def atom(n):
    p     = []
    dt    = 1e-17
    r     = 1e-9
    p0    = 5e5*0.511*m0*sqrt(n)
    angle = 2*math.pi/n
    for i in range(n):
        rx = r0*math.cos(i*angle)/5.
        ry = r0*math.sin(i*angle)/5.
        p.append( sphere( pos=( rx,ry,0.0), radius=r0/5, color = color.red) )
    e = sphere( pos=(r,0.0,0.0), radius = r0, color = color.blue, make_trail = True)
    e.mass = 0.511*m0
    e.p = vector(0.0,p0,0.0)

    while True:
        rate(200)
        F = n*force(em,p[0],e)
        e.p = e.p - F*dt
        e.pos = e.pos + e.p/e.mass*dt

def threebody():
    p    = []
    m    = 5e32
    p0   = 3.e6*m
    d0   = 2e9
    rbig = 1e8
    rx   = 0.5*d0
    ry   = 0.5*d0*sin(math.pi/3)
    dt   = 1

    p.append( sphere( pos=(-rx,-ry,0.0), radius = rbig, color = color.red, make_trail = True, p=vector(+p0,0.0,0.0), mass = m) )
    p.append( sphere( pos=(+rx,-ry,0.0), radius = rbig, color = color.red, make_trail = True, p=vector(0.0,+p0,0.0), mass = m) )
    p.append( sphere( pos=(0.0,+ry,0.0), radius = rbig, color = color.red, make_trail = True, p=vector(0.0,-3*p0,0.0), mass = m))
    while True:
        rate(200)
        F = [vector(0.0,0.0,0.0)]*3
        for i in range(3):
            for j in range(3):
                if i==j:
                    continue
                F[i] = F[i] + force(G*m**2,p[i],p[j])
        for i in range(3):
            p[i].p   = p[i].p + F[i]*dt
            p[i].pos = p[i].pos + p[i].p/m*dt

##def pendulum():
##    m = 1
##    l = 1
##    theta0 = math.pi/3
##    x0 = l*math.sin(theta0)
##    y0 = -l*math.cos(theta0)
##    dt = 1e-2
##    cero = sphere( pos=(0,0,0.0), radius = l/5., color = color.blue )
##    p = sphere( pos=(x0,y0,0.0), radius = l/5., color = color.red, make_trail = True, p=vector(0.0,0.0,0.0), mass = m)
##    while True:
##        rate(200)
##        theta = math.asin( p.pos[0]/l )
##        F = -g*m*math.sin(theta)*vector(math.cos(theta),math.sin(theta),0)
##        p.p = p.p + F*dt
##        p.pos = p.pos + p.p*dt/m

def pendulum():
    m = 1
    l = 1
    theta0 = math.pi/9
    x0 = l*math.sin(theta0)
    y0 = -l*math.cos(theta0)
    dt = 1e-2
    omega=0
    cero = sphere( pos=(0,0,0.0), radius = l/5., color = color.blue )
    p = sphere( pos=(x0,y0,0.0), radius = l/5., color = color.red, make_trail = True, p=vector(0.0,0.0,0.0), mass = m)
    while True:
        rate(200)
        theta = theta0 + omega*dt
        p.pos = l*vector(math.sin(theta),math.cos(theta),0)
        omega = math.sqrt(abs(2*g/l*math.cos(theta)))
        theta0 = theta

#def electrons(d):
#    p0= 10
#    e1 = sphere( pos=(-100,-d/2.,0.0), radius = d/4.., color = color.blue, make_trail = True, p=vector(+p0,0.0,0.0), mass = 0.511*m0)
#    e2 = sphere( pos=(+100,+d/2.,0.0), radius = d/4.., color = color.blue, make_trail = True, p=vector(-p0,0.0,0.0), mass = 0.511*m0)
#    while True:
#        rate(200)
#        F = force(em,e1,e2) + q0*vectorial( e1.p/e1.mass, )

def vectorial(v1,v2):
    return vector( v1[1]*v2[2] - v1[1]*v2[2], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0] )

#H()
#triangle()
#square()
#polygon(120)
#atom(10)
threebody()
#pendulum()
