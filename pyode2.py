#! /usr/bin/env python

import pygame, sys, time, math, ode, random

def coord (x, y):
    return int (320+170*x), int (400-170*y)

def near_callback(args, geom1, geom2):
    contacts = ode.collide(geom1, geom2)

    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

def create_circle (world, space, density, radius):
    body = ode.Body (world)
    m = ode.Mass ()
    m.setSphere (density, radius)
    body.setMass (m)

    geom = ode.GeomSphere (space, .1)
    geom.setBody (body)

    return body, geom

def drop_object ():
    global bodies, geom, counter, objcount

    body, geom = create_circle (world, space, 2500, .1)
    body.setPosition ((random.gauss (0, 0.1), 3.0, 0))
    bodies.append (body)
    geoms.append (geom)
    counter = 0
    objcount += 1

def vscal (v, s):
    for i in range (len (v)):
        v[i] *= s

def explosion():
    global bodies

    print "boom"

    for b in bodies:
        x, y, z = b.getPosition ()
        d = math.hypot (x, y)
        a = max(0, 40000*(1.0-0.2*d*d))
        l = [x / 4, y, 0]
        vscal (l, a / math.hypot (l[0], l[1]))
        b.addForce(l)

def pull():
    global bodies, counter

    print "ssssllluuuurrrppp"

    for b in bodies:
        l=list (b.getPosition ())
        vscal (l, -1000 / math.hypot (l[0], l[1]))
        b.addForce(l)
        if counter%60==0:
            b.addForce((0,10000,0))

def draw ():
    screen.fill ((0, 0, 0))

    for b in bodies:
        x, y, z = b.getPosition ()
        pygame.draw.circle (screen, (55, 0, 200), coord (x, y), 20, 0)

    pygame.draw.line (screen, (255, 0, 0), (0, coord(0, 0)[1]),
                      (WIDTH, coord(0, 0)[1]))

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

x = 0
y = 0

WIDTH = 640
HEIGHT = 480

pygame.init ()

screen = pygame.display.set_mode ((WIDTH, HEIGHT))

pygame.display.set_caption ("PyODE Learning")

clock = pygame.time.Clock ()

world = ode.World ()
world.setGravity ((0, -10, 0))

space = ode.Space ()

floor = ode.GeomPlane (space, (0, 1, 0), 0)

bodies = []

geoms = []

contactgroup = ode.JointGroup ()

fps = 60
dt = 1.0 / fps
running = True
state = 0
counter = 0
objcount = 0
lasttime = time.time ()

while True:
    t = dt - (time.time () - lasttime)
    if (t > 0):
        time.sleep (t)

    process_input ()

    counter += 1

    if state == 0:
        if counter == 20:
            drop_object ()
        if objcount == 30:
            state = 1
            counter = 0
    elif state == 1:
        if counter == 100:
            explosion ()
        elif counter > 300:
            pull ()
        elif counter == 500:
            counter = 20
    
    n = 2

    for i in range (n):
        space.collide ((world, contactgroup), near_callback)

        world.step (dt / n)

        contactgroup.empty ()

    draw ()

    lasttime = time.time ()
