#! /usr/bin/env python

import pygame, sys, time

class unit:
    def __init__ (self, x, y, mass, vx=0, vy=0):
        self.pos = [x, y]
        self.mass = mass
        self.vel = vect (vx, vy)
        self.last_time = time.time ()

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

player = unit (50, 50, 1000)

diff = vect (0, 0)

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
            diff.x = float (pos[0] - CENTER[0])
            diff.y = float (pos[1] - CENTER[1])
            pygame.mouse.set_pos (CENTER)

def draw ():
    screen.fill (black)

    pygame.draw.circle (screen, green, (int (player.pos[0]),
                                        int (player.pos[1])), 20, 0)

    pygame.display.flip ()

def phys_step ():
    now = time.time ()
    dt = now - player.last_time

    player.vel.x += diff.x / player.mass
    player.vel.y += diff.y / player.mass

    if abs (player.vel.x) > MAXVEL:
        if player.vel.x > 0:
            player.vel.x = MAXVEL
        else:
            player.vel.x = -MAXVEL

    if abs (player.vel.y) > MAXVEL:
        if player.vel.y > 0:
            player.vel.y = MAXVEL
        else:
            player.vel.y = -MAXVEL

    player.pos[0] += dt * player.vel.x
    player.pos[1] += dt * player.vel.y

pygame.mouse.set_pos (CENTER)
pygame.mouse.set_visible (False)
while True:
    process_input ()
    phys_step ()
    draw ()

    clock.tick (60)

pygame.quit ()
