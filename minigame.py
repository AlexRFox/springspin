#! /usr/bin/env python

import pygame, ode, time, sys, math

SCALE = 800

WIDTH = SCALE
HEIGHT = SCALE
SIZE = (WIDTH, HEIGHT)

CENTER = (WIDTH / 2, HEIGHT / 2)

def ode_to_pygame (x, y):
    return x * SCALE, HEIGHT - y * SCALE

def pygame_to_ode (x, y):
    return float (x) / SCALE, float (800 - y) / SCALE

def rect_to_pol (x, y):
    r = math.hypot (x, y)
    t = math.atan2 (y, x)

    return (r, t)

def pol_to_rect (r, t):
    x = r * math.cos (t)
    y = r * math.sin (t)

    return (x, y)

def near_callback(args, geom1, geom2):
    global best_speed, flash

    contacts = ode.collide(geom1, geom2)

    if (geom1 == geoms[0] and geom2 == geoms[1]) \
            or (geom1 == geoms[1] and geom2 == geoms[0]):
        vel0 = bodies[0].getLinearVel ()
        speed0 = math.hypot (vel0[0], vel0[1])
        vel1 = bodies[1].getLinearVel ()
        speed1 = math.hypot (vel1[0], vel1[1])

        if speed0 + speed1 > best_speed:
            best_speed = speed0 + speed1
            flash = True
    

    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

def draw ():
    global flash

    screen.fill ((0, 0, 0))

    for b in bodies:
        x, y, z = b.getPosition ()
        coords = ode_to_pygame (x, y)
        p = [coords[0], coords[1]]
        for i in range (len (coords)):
            p[i] = int (p[i])
        pygame.draw.circle (screen, (55, 0, 200), p, int (b.rad * SCALE), 0)

    if pygame.mouse.get_pressed ()[0]:
        x0, y0, z0 = bodies[0].getPosition ()
        x1, y1, z1 = bodies[1].getPosition ()
        
        pygame.draw.line (screen, (0, 0, 255),
                          ode_to_pygame (x0, y0), ode_to_pygame (x1, y1))
        
    if flash:
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)
    flash = False
    text = font.render (str (best_speed), True, color)
    textpos = text.get_rect (centerx=background.get_width () / 2)
    textpos.top = 300
    screen.blit (text, textpos)

    pygame.display.flip ()

def process_input ():
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit ()
            sys.exit ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit ()
                sys.exit ()
def controls ():
    mpos = pygame.mouse.get_pos ()
    mpos = pygame_to_ode (mpos[0], mpos[1])
    rel = (mpos[0] - .5, mpos[1] - .5)
    pf = (50 * rel[0], 50 * rel[1], 0)
    bodies[0].addForce (pf)
    pygame.mouse.set_pos (CENTER)


    if pygame.mouse.get_pressed ()[0]:
        upos = bodies[1].getPosition ()
        ppos = bodies[0].getPosition ()
        
        dx = float (upos[0] - ppos[0])
        dy = float (upos[1] - ppos[1])

        r, t = rect_to_pol (dx, dy)
        r -= .1
        dx, dy = pol_to_rect (r, t)

        k = 20
        pf = (k * dx, k * dy, 0)
        bodies[0].addForce (pf)
        uf = (-k * dx, -k * dy, 0)
        bodies[1].addForce (uf)

pygame.init ()
screen = pygame.display.set_mode (SIZE)
pygame.display.set_caption ("Spring Spin")
pygame.mouse.set_pos (CENTER)
pygame.mouse.set_visible (False)

background = pygame.Surface (SIZE)
font = pygame.font.Font (None, 36)

world = ode.World ()
space = ode.Space ()
wall0 = ode.GeomPlane (space, (0, 1, 0), 0)
wall1 = ode.GeomPlane (space, (0, -1, 0), -1)
wall2 = ode.GeomPlane (space, (1, 0, 0), 0)
wall3 = ode.GeomPlane (space, (-1, 0, 0), -1)
bodies = []
geoms = []
contactgroup = ode.JointGroup ()

body0 = ode.Body (world)
m = ode.Mass ()
body0.rad = .025
m.setSphere (2500, body0.rad)
body0.setMass (m)
body0.setPosition ((.5, .5, 0))
bodies.append (body0)
geom = ode.GeomSphere (space, body0.rad)
geom.setBody (body0)
geoms.append (geom)

body1 = ode.Body (world)
m = ode.Mass ()
body1.rad = .01
m.setSphere (25000, body1.rad)
body1.setMass (m)
body1.setPosition ((.8, .8, 0))
bodies.append (body1)
geom = ode.GeomSphere (space, body1.rad)
geom.setBody (body1)
geoms.append (geom)

# j0 = ode.BallJoint (world)
# j0.attach (body0, body1)
# j0.setAnchor ((.5, .5, .5))

fps = 60
dt = 1.0 / fps
lasttime = time.time ()
best_speed = 0
flash = False

while True:
    t = dt - (time.time () - lasttime)
    if t > 0:
        time.sleep (t)

    process_input ()
    controls ()

    phys_steps = 10

    for i in range (phys_steps):
        space.collide ((world, contactgroup), near_callback)
        world.step (dt / phys_steps)
        contactgroup.empty ()

    draw ()
    lasttime = time.time ()
