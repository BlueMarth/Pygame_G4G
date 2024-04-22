import pygame
from pygame.locals import *

# color dictionary
colors ={
    "white":(255, 255, 255),
    "gray":(127, 127, 127),
    "black":(255, 255, 255),
    "red":(255, 87, 51),
    "yellow":(255, 87, 51),
    "green":(80, 200, 120),
    "blue":(0, 127, 255),
    "purple":(200, 162, 200)
}

pygame.init()

window = pygame.display.set_mode((600,600))
gray = (127,127,127)
window.fill(('gray'))

# hollow rectangle with 2 pixels border
pygame.draw.rect(window, ('red'), [100, 100, 400, 100], 2)
# solid rectangle
pygame.draw.rect(window,('yellow'),[100, 300, 400, 100], 0)

# hollow circle 150 radius
pygame.draw.circle(window, ('green'), [300, 300], 150, 4)
# solid circle
pygame.draw.circle(window, ('blue'), [300, 300], 100, 0)

# solid polygon
x1,y1 = 200, 200
x2,y2 = 450, 300
x3,y3 = 325, 325
x4,y4 = 300, 450
pygame.draw.polygon(window, ('purple'), [[x1,y1], [x2,y2], [x3,y3], [x4,y4]])
# hollow polygon
x1,y1 = 600-x1, 600-y1
x2,y2 = 600-x2, 600-y2
x3,y3 = 600-x3, 600-y3
x4,y4 = 600-x4, 600-y4
pygame.draw.polygon(window, ('black'), [[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 6)

# line
pygame.draw.line(window, ('white'), [100,150],[500,450])

while True:
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()