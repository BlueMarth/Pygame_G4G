import pygame
from pygame.locals import *
from sys import exit

pygame.init()

size = screen_width, screen_height = 768, 432
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Moving Objects")
icon = pygame.image.load("github_icon.png")
pygame.display.set_icon(icon)

# create a copy of image on surface
img_fb = pygame.image.load("facebook_icon.png").convert()
display_img = img_fb
x, y = 0, 0
move_x, move_y = 0, 0

while True:
    
    img_width = display_img.get_width()
    img_height = display_img.get_height()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    # keyboard interrupts
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            move_x = +0.5
            print("RIGHT")
        elif event.key == pygame.K_LEFT:
            move_x = -0.5
            print("LEFT")
        elif event.key == pygame.K_UP:
            move_y = -0.5
            print("UP")
        elif event.key == pygame.K_DOWN:
            move_y = +0.5
            print("DOWN")
        elif event.key == pygame.K_LCTRL:
            display_img = pygame.image.load("instagram_icon.png")
            pygame.display.update()
        # elif event.key == pygame.K_BACKSPACE:
        #     display_img = pygame.image.load("facebook_icon.png")
        #     pygame.display.update()
            
    # stop moving when key released
    if event.type == KEYUP:
        if event.key == pygame.K_RIGHT:
            move_x = 0
        elif event.key == pygame.K_LEFT:
            move_x = 0
        elif event.key == pygame.K_UP:
            move_y = 0
        elif event.key == pygame.K_DOWN:
            move_y = 0
        elif event.key == pygame.K_LCTRL:
            display_img = pygame.image.load("facebook_icon.png")
            pygame.display.update()
    

    x += move_x
    y += move_y

    if x < 0:
        x = 0
    elif x > (screen_width - img_width):
        x = screen_width - img_width
    elif y < 0:
        y = 0
    elif y > (screen_height - img_height):
        y = screen_height - img_height

    screen.fill((255, 255, 255))
    screen.blit(display_img, (x,y))
    pygame.display.update()
