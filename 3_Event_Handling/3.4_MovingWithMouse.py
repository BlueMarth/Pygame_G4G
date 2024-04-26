import pygame
from pygame.locals import *
from sys import exit

pygame.init()

size = screen_width, screen_height = 768, 432
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Moving Objects")
icon = pygame.image.load("visual/github_icon.png")
pygame.display.set_icon(icon)
img = pygame.image.load("visual/mouse_hover.png")

clicking = False
right_clicking = False
middle_click = False

while True:
    mx, my = pygame.mouse.get_pos()
    x = mx - img.get_width()/2
    y = my - img.get_height()/2
    location = [x, y]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    # mouse interrupts
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1: # left button
            clicking = True
            img = pygame.image.load("visual/mouse_hover.png")
            pygame.display.update()
        if event.button == 3: # middle button
            right_clicking = True
            img = pygame.image.load("visual/mouse_click.png")
            # flip the cursor about both axis
            img = pygame.transform.flip(img, True, True)
            pygame.display.update()
        if event.button == 2:
            middle_click = middle_click
            # scale the image smaller
            img = pygame.transform.scale(img, (60, 60))
            pygame.display.update()
    
    if event.type == MOUSEBUTTONUP:
        if event.button == 1:
            clicking = False

    screen.fill((255, 255, 255))
    screen.blit(img, (location[0], location[1]))
    
    pygame.display.update()
