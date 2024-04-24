import math
import random
import pygame
from pygame.locals import *

# color dictionary
colours = {
    "white":    (255, 255, 255),
    "gray":     (127, 127, 127),
    "black":    (255, 255, 255),
    "red":      (255, 87, 51),
    "yellow":   (255, 87, 51),
    "green":    (80, 200, 120),
    "blue":     (0, 127, 255),
    "purple":   (200, 162, 200)
}

def rad(theta) :
    return theta*math.pi/180

def rotatePoint(p,q,theta) :
    p1 = p * math.cos(rad(theta)) - q * math.sin(rad(theta))
    q1 = p * math.sin(rad(theta)) + q * math.cos(rad(theta))
    return p1, q1

def drawTriangle (c1, c2, l, tilt, colour, border) :
    # reset points
    x = [0, 0, 0]
    y = [0, 0, 0]
    # compute first set of points
    x[0] = int(l * math.cos(rad(tilt)))
    y[0] = int(l * math.sin(rad(tilt)))
    # compute subsequent sets of points
    for i in range(1,3):
            x[i], y[i] = rotatePoint(x[i-1], y[i-1], 120)
            x[i] = int(x[i])
            y[i] = int(y[i])
    # translate all points by centre distance
    for i in range(3):
         x[i] = x[i] + c1
         y[i] = y[i] + c2
    # draw the hexagon
    if border > 0:
        pygame.draw.polygon(window, colour, [[x[0],y[0]], [x[1],y[1]], [x[2],y[2]]], border)
    else:
        pygame.draw.polygon(window, colour, [[x[0],y[0]], [x[1],y[1]], [x[2],y[2]]])

# initiate pygame
pygame.init()
# create display window
window = pygame.display.set_mode((600,600))
window.fill(('gray'))

draw_positions = []
brush_size = 20

count = 0
run = True

while run:
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            run = False
        # draw small triangle when LMB pressed
        elif event.type == MOUSEBUTTONDOWN:
            position = event.pos
            draw_positions.append(position)
            brush_size = int(random.uniform(5,25))
            tilt = int(random.uniform(0,120))
            thisColour = random.choice(list(colours.keys()))
            drawTriangle(position[0], position[1], brush_size, tilt, thisColour, 0)
        # draw outline triangle when LMB released
        elif event.type == MOUSEBUTTONUP:
            brush_size = int(brush_size * 1.5)
            border = int(brush_size / 5)
            drawTriangle(position[0], position[1], brush_size, tilt, thisColour, border)

    pygame.display.update()