import pygame
import sys
pygame.init()
size = w,h = 640, 360
screen = pygame.display.set_mode((w,h))

buttonFrames = []

def makeFrame(cx,cy,side):
    x1 = cx-side//2
    y1 = cy-side//2
    x2 = cx+side//2
    y2 = cy+side//2
    pygame.Rect((x1,y1,x2,y2))

home_btn = makeFrame(80, 180, 100)
play_btn = makeFrame(240, 180, 100)
exit_btn = makeFrame(480, 180, 100)
options_btn = makeFrame(560, 180, 100)

buttonFrames = [(0, 0, 0, 0),
                (0, 0, 0, 0),
                (0, 0, 0, 0),
                (0, 0, 0, 0)
                ]
for frame in buttonFrames:
    buttonFrames[frame] = 

""" while True:
    
    for event in pygame.event.get():
        if event == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if  """

    

    # pygame.draw.rect(screen, "red", home_btn)
    # pygame.draw.rect(screen, "blue", play_btn)
    # pygame.draw.rect(screen, "yellow", exit_btn)
    # pygame.draw.rect(screen, "green", options_btn)
