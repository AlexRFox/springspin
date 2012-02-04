#! /usr/bin/env python

import pygame, ode, time, sys, math

SCALE = 800

WIDTH = SCALE
HEIGHT = SCALE

CENTER = (WIDTH / 2, HEIGHT / 2)

class unit ():
    def __init__ (self, body, geom, rad, player):
        self.body = body
        self.geom = geoms
        self.rad = rad
        self.player = player

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
    contacts = ode.collide(geom1, geom2)

    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.4)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

def closest (u0):
    x0, y0, z0 = u0.body.getPosition ()

    best_u = None
    best_dist = sys.maxint

    for u1 in units:
        if u1 != u0:
            x1, y1, z1 = u1.body.getPosition ()
            dist = math.hypot (x0 - x1, y0 - y1)
            if dist < best_dist:
                best_u = u1
                best_dist = dist

    return best_u

def draw ():
    screen.fill ((0, 0, 0))

    for u in units:
        x, y, z = u.body.getPosition ()
        coords = ode_to_pygame (x, y)
        p = [coords[0], coords[1]]
        for i in range (len (coords)):
            p[i] = int (p[i])
        pygame.draw.circle (screen, (55, 0, 200), p, int (u.rad * SCALE), 0)

    if pygame.mouse.get_pressed ()[0]:
        other = closest (player)

        px, py, pz = player.body.getPosition ()
        ux, uy, uz = other.body.getPosition ()

        pygame.draw.line (screen, (0, 0, 255),
                          ode_to_pygame (px, py),
                          ode_to_pygame (ux, uy))
        
    pygame.display.flip ()

def process_input ():
    global paused

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit ()
            sys.exit ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit ()
                sys.exit ()
            elif event.key == pygame.K_p:
                paused = (paused + 1) % 2

def controls ():
    mpos = pygame.mouse.get_pos ()
    mpos = pygame_to_ode (mpos[0], mpos[1])
    rel = (mpos[0] - .5, mpos[1] - .5)
    pf = (50 * rel[0], 50 * rel[1], 0)
    player.body.addForce (pf)
    pygame.mouse.set_pos (CENTER)


    if pygame.mouse.get_pressed ()[0]:
        other = closest (player)

        ppos = player.body.getPosition ()
        opos = other.body.getPosition ()
        
        dx = float (opos[0] - ppos[0])
        dy = float (opos[1] - ppos[1])

        r, t = rect_to_pol (dx, dy)
        r -= .1
        dx, dy = pol_to_rect (r, t)

        k = 20
        pf = (k * dx, k * dy, 0)
        player.body.addForce (pf)
        of = (-k * dx, -k * dy, 0)
        other.body.addForce (of)

pygame.init ()
screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Spring Spin")
pygame.mouse.set_pos (CENTER)
pygame.mouse.set_visible (False)

world = ode.World ()
space = ode.Space ()
wall0 = ode.GeomPlane (space, (0, 1, 0), 0)
wall1 = ode.GeomPlane (space, (0, -1, 0), -1)
wall2 = ode.GeomPlane (space, (1, 0, 0), 0)
wall3 = ode.GeomPlane (space, (-1, 0, 0), -1)
bodies = []
geoms = []
units = []
contactgroup = ode.JointGroup ()

body = ode.Body (world)
m = ode.Mass ()
rad = .025
m.setSphere (2500, rad)
body.setMass (m)
body.setPosition ((.5, .5, 0))
bodies.append (body)
geom = ode.GeomSphere (space, rad)
geom.setBody (body)
geoms.append (geom)
player = unit (body, geom, rad, True)
units.append (player)

body = ode.Body (world)
m = ode.Mass ()
rad = .01
m.setSphere (25000, rad)
body.setMass (m)
body.setPosition ((.8, .8, 0))
bodies.append (body)
geom = ode.GeomSphere (space, rad)
geom.setBody (body)
geoms.append (geom)
units.append (unit (body, geom, rad, False))

body = ode.Body (world)
m = ode.Mass ()
rad = .01
m.setSphere (25000, rad)
body.setMass (m)
body.setPosition ((.3, .3, 0))
bodies.append (body)
geom = ode.GeomSphere (space, rad)
geom.setBody (body)
geoms.append (geom)
units.append (unit (body, geom, rad, False))

fps = 60
dt = 1.0 / fps
lasttime = time.time ()

paused = False

while True:
    t = dt - (time.time () - lasttime)
    if t > 0:
        time.sleep (t)

    process_input ()

    if not paused:
        controls ()

        phys_steps = 10

        for i in range (phys_steps):
            space.collide ((world, contactgroup), near_callback)
            world.step (dt / phys_steps)
            contactgroup.empty ()

    draw ()
    lasttime = time.time ()
