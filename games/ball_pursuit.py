import visual
import math
import random
import copy

def compute_angle( Pa, Pb ):
    dir = Pb.pos - Pa.pos
    return math.acos( Pa.p.dot( dir ) / ( Pa.p.mag * dir.mag ) )

def GetXY( alpha, r = 1 ):
    return r * math.cos(alpha), r * math.sin(alpha)

def Compute_distances( particles ):
    indices = []
    for i in rangelen(particles):
        particle = particles[i]
        for j in rangelen(particles[i+1:]):
            if (particle.pos - particles[i+j+1].pos).mag <= particle.radius + particles[i+j+1].radius:
                indices.append( (i,i+j+1) )
    return indices

def GameOver( player, enemies ):
    for enemy in enemies:
        if (player.pos-enemy.pos).mag < player.radius + enemy.radius:
            return True
    return False

rangelen = lambda x: range(len(x))

### Instances
pi  = math.pi
R   = random.Random()
C   = R.choice
U   = lambda: R.uniform(-1,1)
T   = lambda: R.gauss( pi, pi**.5 )
is_at_max_speed = True
nstepsmax = 50
nsteps = nstepsmax
t = 0
t_total = 0

### Game parameters
time_step        = 1e-2
nenemies_max     = 5
enemy_appearance = 10
force_intensity  = 3e-2
ball_radius      = 3.e-1
enemies_distance = 10.
player_position  = visual.vector( 0, 0, 0 )
phantom_position = visual.vector( 1, 0, 0 )
player_direction = visual.vector( U(), U(), 0 ).norm()
player_direction = visual.vector( 0, 1, 0 ).norm()
player_momentum  = 1.
enemies_momenta  = 1.001 * player_momentum
speed            = 2

### Game window
scene = visual.display( title = 'Ball pursuit',
                        x = 0, y = 0,
                        width = 640, height = 400,
                        center = player_position,
                        autoscale = False)

### Player ball
player =  visual.sphere( pos = player_position,
                         radius = ball_radius,
                         p   = player_momentum * player_direction,
                         color = visual.color.red,
                         make_trail = True)
player.trail_object.radius = ball_radius * 0.2

### Phantom ball
phantom =  visual.sphere( pos = phantom_position,
                          radius = ball_radius,
                          visible = False )

### Enermies
enemies = []
colors  = [ visual.color.orange,
            visual.color.green,
            visual.color.blue,
            visual.color.yellow,
            visual.color.cyan,
            visual.color.magenta,
            visual.color.white,
            (1,0.7,0.2) ]

while not GameOver( player, enemies ):
    visual.rate( speed * 100)
    t_total += time_step
    t += time_step
    if len(enemies) <= nenemies_max and t // enemy_appearance > len( enemies ) :
        t = 0
        x,y = GetXY( T(), enemies_distance )
        enemy_position = visual.vector( player.x + x, player.y + y, 0 )
        enemies.append(  visual.sphere( pos = enemy_position,
                                        radius = ball_radius,
                                        p   = enemies_momenta * (player.pos-enemy_position).norm(),
                                        color = C( colors ),
                                        make_trail = True ) )
        enemies[-1].trail_object.radius = ball_radius * 0.2
    if scene.mouse.events:
        phantom.pos = scene.mouse.getevent().pos
        nsteps = 0
        is_at_max_speed = False
#    if scene.mouse.clicked:
#        phantom.pos = scene.mouse.getclick().pos
#        nsteps = 0
#        is_at_max_speed = False
    if nsteps<nstepsmax:
        nsteps += 1
        player.p += force_intensity * (phantom.pos - player.pos).norm()
        if player.p.mag >= player_momentum:
            player.p = player_momentum * player.p.norm()
            is_at_max_speed = True
    elif player.p.mag < player_momentum:
        player.p = player_momentum * player.p.norm()

    player.pos += player.p * time_step
    for enemy in enemies:
        enemy.p = enemies_momenta * (player.pos-enemy.pos).norm()
        enemy.pos += enemy.p * time_step

    enemies_touched = Compute_distances( enemies )
    for enemy in enemies_touched:
        enemies.pop(enemy[1]).visible = False
        enemies.pop(enemy[0]).visible = False


    scene.center = player.pos

t_total /= speed

game_over = visual.text( text='Game over', pos = player.pos + visual.vector(0,0,1), height = 3., align='center', font = 'Times', color=visual.color.red)

time_played = visual.text( text='total time = ' + str(t_total) + ' s', pos = player.pos + visual.vector(0,-2.5,1), height = 1.5, align='center', font = 'Times', color=visual.color.orange)