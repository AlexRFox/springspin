#! /usr/bin/env python

import pygame, ode, time, sys

WIDTH = 640
HEIGHT = 480

#scales coords from pixels to ode's
def coord_ode (x, y, z=None):
    c = [int (x * 170 + 320), int (400 - y * 170)]
    try:
        z
        c.append (z * 170)
    except:
        pass
    return c

#scales coords from ode's to pixels
def coord_pygame (x, y, z=None):
    c = [int ((x - 320) / 170), int ((y + 400) / 170)]
    try:
        z
        c.append (z * 170)
    except:
        pass
    return c

def near_callback(args, geom1, geom2):
    contacts = ode.collide(geom1, geom2)

    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

def draw ():
    screen.fill ((0, 0, 0))

    for b in bodies:
        x, y, z = b.getPosition ()
        print x, y, z
        pygame.draw.circle (screen, (55, 0, 200), coord_ode (x, y), 20, 0)

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

pygame.init ()

screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Spring Spin")

world = ode.World ()
space = ode.Space ()
# wall0 = ode.GeomPlane (space, (0, -1, 0), 0)
# wall1 = ode.GeomPlane (space, (-1, 0, 0), WIDTH / 170)
# wall2 = ode.GeomPlane (space, (1, 0, 0), 0)
# wall3 = ode.GeomPlane (space, (0, 1, 0), HEIGHT / 170)
bodies = []
geoms = []
contactgroup = ode.JointGroup ()

body = ode.Body (world)
m = ode.Mass ()
m.setSphere (2500, .1)
body.setMass (m)
body.setPosition ((0, 0, 0))
bodies.append (body)
geom = ode.GeomSphere (space, .1)
geom.setBody (body)
geoms.append (geom)

fps = 60
dt = 1.0 / fps
lasttime = time.time ()

while True:
    t = dt - (time.time () - lasttime)
    if t > 0:
        time.sleep (t)

    process_input ()

    phys_steps = 2
    
    for i in range (phys_steps):
        space.collide ((world, contactgroup), near_callback)
        world.step (dt / phys_steps)
        contactgroup.empty ()

    draw ()
    lasttime = time.time ()
