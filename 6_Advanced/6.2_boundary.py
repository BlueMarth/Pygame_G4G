import pygame
from pygame.locals import *
from sys import exit
pygame.init()

def checkCollision(x, ball_size, L, R):
    if (x - ball_size//2) <= (L + 0):
        return 1
    elif (x + ball_size//2) >= (600 - R):
        return 2
    else:
        return 0

screen_width, screen_height = 600, 240
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("gray2")

left_wall_size = [100, 150]
right_wall_size = [150, 150]
ball_size = 25

normal_color = "lightskyblue4"
collide_color = "lightskyblue"

x, y = screen_width//2, screen_height//2
move_x = 0
move_y = 0
ball_color = normal_color

# 0:not collide 1:left_wall 2:right_wall
collide_case = 0

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    screen.fill((0,0,0))
    ball = pygame.draw.circle(screen, ball_color, [x, y], ball_size)
    left_wall = pygame.draw.rect(screen, "firebrick3", [0,90,left_wall_size[0],left_wall_size[1]])
    right_wall = pygame.draw.rect(screen, "firebrick4", [450,90,right_wall_size[0],right_wall_size[1]])
    
    if event.type == KEYDOWN:
        if event.key == pygame.K_RIGHT:
            move_x = +0.01
        elif event.key == pygame.K_LEFT:
            move_x = -0.01
    
    if event.type == KEYUP:
        if event.key == pygame.K_RIGHT:
            move_x = 0
        if event.key == pygame.K_LEFT:
            move_x = 0

    # collision detection and clamping
    x += move_x
    left_limit = left_wall_size[0] + ball_size//2
    right_limit = 600 - right_wall_size[0] - ball_size//2
    if x < left_limit:
        x = left_limit
        ball_color = collide_color
    elif x > right_limit:
        x = right_limit
        ball_color = collide_color
    else:
        ball_color = normal_color

    pygame.display.update()