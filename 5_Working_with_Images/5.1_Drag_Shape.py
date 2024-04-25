import pygame
from pygame.locals import *
import math
pygame.init()
clock = pygame.time.Clock()

w, h = 640, 360
screen = pygame.display.set_mode((w,h))

img = pygame.image.load("visual/droplet.png").convert()

rect = img.get_rect()
rect.center = w//2, h//2

moving = False

fps = 30
while True:
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()

        elif event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True
        elif event.type == MOUSEBUTTONUP:
            moving = False
        elif event.type == MOUSEMOTION and moving:
            rect.move_ip(event.rel)

    screen.fill("gray2")
    screen.blit(img, rect)
    
    pygame.display.update()
    clock.tick(fps)