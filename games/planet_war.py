import visual
import math
import sys

### Game parameters
G                = 6.6e-8
M                = 2e30
time_step        = 1e-5
player_radius    = 1e6
player_mass      = 1e24
player_position  = visual.vector( 0, 0, 0 )
missile_radius   = 1e6
missile_length   = 3e6
missile_mass     = 1e5
missile_position = lambda x: (x.pos - player_position).norm() * player_radius
missile_momentum = 1e3
win              = False
level            = int(sys.argv[1]) if len(sys.argv) > 1 else 0


def Average( values ):
    return sum(values)/len(values)

def ComputeCenter( *elements ):
    return map(Average,zip(*[ element.pos for element in elements ]))

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
    return reduce( lambda x,y: x+y, map(Force,planets) )

def Game_over():
    global missile
    global scene
    global target
    global win
    if (missile.pos-target.pos).mag < missile.radius + target.radius:
        win = True
        return False
    
    VectorToCenter = missile.pos - visual.vector(scene.center)
    drscene    = [ abs(VectorToCenter[i]) > scene.range[i] for i in range(3) ]
    drplanets  = [ (missile.pos - planet.pos).mag < missile.radius + planet.radius for planet in planets ]
    drbarriers = [ (missile.pos - barrier.pos).mag < missile.radius + barrier.radius for barrier in barriers ]
    return any( drscene + drplanets + drbarriers )

def ConfigureLevel():
    global level
    global planets_properties
    global barriers_properties
    global target_position
    global target_radius
    global target_mass
    
    ### Other elements of the games. Information must be given as a dictionary
    planets_properties  = []
    barriers_properties = []
    
    if   level is 0:
        target_position = visual.vector( 1, 1, 0 ).norm() * 1e8
        target_radius = 2 * player_radius
        target_mass   = player_mass * 500000
        planets_properties.append( {    'pos' : visual.vector( 1, 1, 0 ).norm() * .5e8,
                                     'radius' : 8 * player_radius,
                                       'mass' : M,
                                      'color' : visual.color.orange} )

    elif level is 1:
        target_position = visual.vector( 1, 4, 0 ).norm() * 1e8
        target_radius = 1.5 * player_radius
        target_mass   = player_mass * 1000000
        planets_properties.append( {    'pos' : visual.vector( 0.3, 1, 0 ).norm() * .5e8,
                                     'radius' : 6 * player_radius,
                                       'mass' : M*2,
                                      'color' : visual.color.orange} )
        planets_properties.append( {    'pos' : visual.vector( 0.2, 0.8, 0 ).norm() * .8e8,
                                     'radius' : 6 * player_radius,
                                       'mass' : M,
                                      'color' : visual.color.orange} )

    elif level is 2:
        target_position = visual.vector( 1, 0, 0 ).norm() * 1e8
        target_radius = 1 * player_radius
        target_mass   = player_mass * 1000000
        planets_properties.append( {    'pos' : visual.vector( 1, 0, 0 ).norm() * .2e8,
                                     'radius' : 10 * player_radius,
                                       'mass' : M,
                                      'color' : visual.color.orange} )
        planets_properties.append( {    'pos' : visual.vector( 1, 0, 0 ).norm() * 1.5e8,
                                     'radius' : 6 * player_radius,
                                       'mass' : M,
                                      'color' : visual.color.orange} )

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


def game():
    global player
    global target
    global missile
    global planets
    global barriers
    global scene
    global arrow
    global win
    global wintext
    
    
    ConfigureLevel()

    ### Player planet
    player =  visual.sphere( pos = player_position,
                            radius = player_radius,
                            mass  = player_mass,
                            color = visual.color.green )

    target = visual.sphere( pos = target_position,
                            radius = target_radius,
                            mass = target_mass,
                            color = visual.color.red )

    planets  = [ visual.sphere(**planet ) for planet  in planets_properties ]
    barriers = [ visual.curve (**barrier) for barrier in barriers_properties]

    scene.center = tuple(ComputeCenter( player, target, *(planets + barriers) ) )
    scene.range  = ComputeRange( player, target, *(planets + barriers) )

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
                           p = missile_direction * missile_momentum,
                           color = visual.color.yellow,
                           make_trail = True)
    scene.unbind('mousemove',ChangeArrow)
    arrow.visible = False
    del arrow

    while not Game_over():
        visual.rate(100)
        missile.p   += ComputeForce( player, target, *planets ) * time_step
        missile.pos += missile.p * time_step
        missile.axis = missile.p.norm() * missile_length

        if win:
            wintext = visual.text( text='You win', pos = scene.center + visual.vector(0,0,1e8), height = 1e7, align='center', font = 'Times', color=visual.color.green)
#            wintext.up = True

            break
### Game window
scene = visual.display( title = 'Planet war',
                       x = 0, y = 0,
                       width = 1024, height = 700,
                       autoscale = False)

while not win:
    win  = False
    game()