#! /usr/bin/env python

import pygame, sys, time

class unit:
    def __init__ (self, x, y, mass, player=False, vx=0, vy=0):
        self.player = player
        self.pos = [x, y]
        self.mass = mass
        self.vel = vect (vx, vy)
        self.last_time = time.time ()
        self.force = vect (0, 0)

class vect:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    def __str__ (self):
        return "x: " + str (self.x) + ", y: " + str (self.y)

WIDTH = 640
HEIGHT = 480
CENTER = (WIDTH / 2, HEIGHT / 2)
MAXVEL = 50

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

pygame.init ()

size = [640, 480]
screen = pygame.display.set_mode (size)

pygame.display.set_caption ("Spring Spin")

clock = pygame.time.Clock ()

units = []

player = unit (CENTER[0], CENTER[1], 500, True)
units.append (player)

obj = unit (CENTER[0] + 100, CENTER[1] + 100, 1000)
units.append (obj)

def process_input ():
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit ()
            sys.exit ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit ()
                sys.exit ()
            elif event.key == pygame.K_r:
                player.pos[0] = CENTER[0]
                player.pos[1] = CENTER[1]
                player.vel.x = 0
                player.vel.y = 0
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos ()
            player.force.x = float (pos[0] - CENTER[0])
            player.force.y = float (pos[1] - CENTER[1])
            pygame.mouse.set_pos (CENTER)

def draw ():
    screen.fill (black)

    for u in units:
        pygame.draw.circle (screen, green, (int (u.pos[0]),
                                            int (u.pos[1])), 20, 0)

    pygame.display.flip ()

def phys_step ():
#add friction (toggable)
#simulate spring correctly (right now only the non-players are effected)

    for u in units:
        now = time.time ()
        dt = now - u.last_time

        if u.player == False and pygame.mouse.get_pressed ()[0]:
            u.force.x = float (player.pos[0] - u.pos[0])
            u.force.y = float (player.pos[1] - u.pos[1])

        u.vel.x += u.force.x / u.mass
        u.vel.y += u.force.y / u.mass

        if abs (u.vel.x) > MAXVEL:
            if u.vel.x > 0:
                u.vel.x = MAXVEL
            else:
                u.vel.x = -MAXVEL

        if abs (u.vel.y) > MAXVEL:
            if u.vel.y > 0:
                u.vel.y = MAXVEL
            else:
                u.vel.y = -MAXVEL

        u.pos[0] += dt * u.vel.x
        u.pos[1] += dt * u.vel.y

pygame.mouse.set_pos (CENTER)
pygame.mouse.set_visible (False)

while True:
    process_input ()
    phys_step ()
    draw ()

    clock.tick (60)

pygame.quit ()
