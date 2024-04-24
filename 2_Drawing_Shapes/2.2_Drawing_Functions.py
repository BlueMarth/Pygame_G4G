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

def rad(theta):
    return theta*math.pi/180

def rotatePoint(p,q,theta) :
    p1 = p*math.cos(rad(theta)) - q*math.sin(rad(theta))
    q1 = p*math.sin(rad(theta)) + q*math.cos(rad(theta))
    return p1, q1

def drawHexagon (c1, c2, radius, tilt, colour) :
    # reset points
    x = [0,0,0,0,0,0]
    y = [0,0,0,0,0,0]
    # compute first set of points
    x[0] = int(radius*math.cos(rad(tilt)))
    y[0] = int(radius*math.sin(rad(tilt)))
    # compute subsequent sets of points
    for i in range(1,6):
            x[i], y[i] = rotatePoint(x[i-1],y[i-1],60)
            x[i] = int(x[i])
            y[i] = int(y[i])
    # translate all points by centre distance
    for i in range(6):
         x[i] = x[i]+c1
         y[i] = y[i]+c2
    # draw the hexagon
    pygame.draw.polygon(window, colour, [
         [x[0],y[0]], [x[1],y[1]], [x[2],y[2]],
         [x[3],y[3]], [x[4],y[4]], [x[5],y[5]]
    ])
# initiate pygame
pygame.init()
# create display window
window = pygame.display.set_mode((600,600))
window.fill(('gray'))
# set initial drawing conditions
angle = 0
radius = 150
c1, c2 = 450, 300

while True:
    # some real cool shit why not
    while radius > 0:
        pygame.time.delay(1)
        # choose random colour to paint
        thisColour = random.choice(list(colours.keys()))
        drawHexagon(c1, c2 ,radius,angle,thisColour)
        # update drawing conditions
        angle = angle - 15
        radius = radius - 4
        # offset the center of window
        c1 = c1 - 300
        c2 = c2 - 300
        # move center point of hexagon
        c1, c2 = rotatePoint(c1,c2,15)
        # offset to center of window
        c1 = c1 + 300
        c2 = c2 + 300
        # update display
        pygame.display.flip()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()