import visual
import math
import sys

#c = shapes.circle(pos=(0,1.5), radius=0.001)
#
#a = 2.
#b = 4
#
#t = [-(1 - 0.002*i)*pi for i in range(1000)]
#x = [ cos(a*ti)-sin(b*ti) for ti in t]
#y = [ cos(b*ti)-sin(a*ti) for ti in t]
#z = [0. for i in x]
#p = zip(x,y,z)
#
#e = extrusion( pos = p, shape = c, color = color.orange )

def average( values ):
    return sum(values)/len(values)

def ComputeCenter( *elements ):
    return map(average,zip(*[ element.pos for element in elements ]))

def ComputeRange( *elements ):
    center = visual.vector(ComputeCenter( *elements ))
    return 2*max([ (element.pos - center).mag for element in elements ])

def ChangeArrow( click ):
    global arrow
    global player
    arrow.axis = click.pos - player.pos

def Force( planet ):
    global missile
    direction = planet.pos - missile.pos
    return G * planet.mass * missile.mass * direction.norm()/direction.mag2

def ComputeForce( *planets ):
#    print reduce( lambda x,y: x+y, map(Force,planets) )
    return reduce( lambda x,y: x+y, map(Force,planets) )

### Game parameters
G                = 6.6e-8
M                = 2e30
time_step        = .1e-4
player_radius    = 1e6
player_mass      = 1e24
player_position  = visual.vector( 0, 0, 0 )
missile_radius   = 1e6
missile_length   = 3e6
missile_mass     = 1e3
missile_position = lambda x: (x.pos - player_position).norm() * player_radius

### Game window
scene = visual.display( title = 'Planet war',
                        x = 0, y = 0,
                        width = 1024, height = 700,
                        autoscale = False)

### Player planet
player =  visual.sphere( pos = player_position,
                         radius = player_radius,
                         mass  = player_mass,
                         color = visual.color.green )


### Other elements of the games. Information must be given as a dictionary
planets_properties  = []
barriers_properties = []

try:
    level = sys.argv[1]
except:
    level = 0
    
if   level is 0:
    target_position = visual.vector( 1, 1, 0 ).norm() * 1e8
    target_radius = 2 * player_radius
    target_mass   = M
    planets_properties.append( {    'pos' : visual.vector( 1, 1, 0 ).norm() * .5e8,
                                 'radius' : 8 * player_radius,
                                   'mass' : M,
                                  'color' : visual.color.orange} )

elif level is 1:
    pass
elif level is 2:
    pass
elif level is 3:
    pass
elif level is 4:
    pass
elif level is 5:
    pass
elif level is 6:
    pass
elif level is 7:
    pass
elif level is 8:
    pass
elif level is 9:
    pass
elif level is 10:
    pass
elif level is 11:
    pass
elif level is 12:
    pass
else:
    raise ValueError( 'The level {0} does not exist'.format(level) )


target = visual.sphere( pos = target_position,
                        radius = target_radius,
                        mass = target_mass,
                        color = visual.color.red )

planets  = [ visual.sphere(**planet ) for planet  in planets_properties ]
barriers = [ visual.curve (**barrier) for barrier in barriers_properties]

scene.center = tuple(ComputeCenter( player, target, *(planets + barriers) ) )
scene.range = ComputeRange( player, target, *(planets + barriers) )

arrow = visual.arrow( pos = player_position,
                      axis = (target.pos-player.pos).norm() * player_radius * 10,
                      shaftwidth = player_radius * 0.5,
                      headwidth  = player_radius,
                      headlength = player_radius,
                      color = visual.color.cyan)

scene.bind('mousemove',ChangeArrow)
click = scene.waitfor('click')
missile_direction = click.pos - player.pos
missile = visual.cone( pos = missile_position(target),
                       axis = missile_direction.norm() * missile_length,
                       radius = missile_radius,
                       mass = missile_mass,
                       p = missile_direction * missile_mass,
                       color = visual.color.yellow,
                       make_trail = True)
scene.unbind('mousemove',ChangeArrow)
arrow.visible = False
del arrow
while True:
    visual.rate(100)
#    print 'p = ',missile.p
#    print 'f = ',ComputeForce( player, target, *planets )
    missile.p   += ComputeForce( player, target, *planets ) * time_step
    missile.pos += missile.p * time_step
    missile.axis = missile.p.norm() * missile_length
#    print missile.axis

