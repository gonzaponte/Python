from visual import *
from math import pi

green = color.green
red = color.red
white = color.white
### Game parameters
vmax = 2.
theta0 = 15 * pi / 180.
vx0 = vmax * cos(theta0)
vy0 = vmax * sin(theta0)
v0 = vector( vx0, vy0, 0)
player   = cylinder( pos = (-1.,0.,0.), axis = (0.,1.,0.), radius = 0.02, color = green )
computer = cylinder( pos = (+1.,0.,0.), axis = (0.,1.,0.), radius = 0.02, color = red   )
ball     = sphere  ( pos = ( 0.,0.,0.), v    = v0        , radius = 0.02, color = white )

xlimit = 1- 0.02
ylimit = 1
dt = 1e-3

def Move( mouse ):
    dy = mouse.y - player.y
    sign = dy/abs(dy) if dy else 1.
    v  = min( vmax, abs(dy) )
    player.v.y = v * sign

def XBoing( ):
    ball.v.x *= -1

def YBoing():
    ball.v.y *= -1


scene = display( title = 'Ping',
                 x = 0, y = 0,
                 width = 1024, height = 700,
                 autoscale = True)

#scene.bind('mousemove',Move)
xin = yin = True
while True:
    rate(200)
    if abs(ball.x) > xlimit and xin:
        xin = False
        XBoing()
    if abs(ball.y) > ylimit and yin:
        yin = False
        YBoing()
    if not xin and abs(ball.x) < xlimit:
        xin = True
    if not yin and abs(ball.y) < ylimit:
        yin = True

    ball.pos += ball.v * dt
#    print ball.x, ball.y, xin, yin


