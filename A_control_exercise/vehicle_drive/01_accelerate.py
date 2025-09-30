# Vehicle acceleration, slow down, and braking simulation along a straight path

""" 
controls
    W: accelerate
    S: brake and reverse
    space: hand brake
"""

import math
import numpy as np
import pygame

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Vehicle Acceleration Simulation")
clock = pygame.time.Clock()

# sprite
car_width = 40
car_height = 20
car_color = (255, 0, 0)  # Red

# Initial position (centered)
car_x = 100
car_y = 300
velocity = 0
acceleration = 0.15
max_velocity = 6
reverse_max_velocity = -2 # Lower top speed for reverse
friction = 0.99
reverse_friction = 0.96 # Stronger friction when reversing
handbrake_strength = 0.9 # Deceleration per frame when handbrake (space) is pressed

running = True
# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        velocity += acceleration
        if velocity > max_velocity:
            velocity = max_velocity
    elif keys[pygame.K_s]:
        velocity -= acceleration
        if velocity < reverse_max_velocity:
            velocity = reverse_max_velocity
    elif keys[pygame.K_SPACE]:
        # Hand brake: strong deceleration toward zero, no direction reversal
        if velocity != 0:
            velocity *= handbrake_strength
        elif abs(velocity) < 1e-4:
            velocity = 0
    else:
        # Use higher friction when in reverse
        if velocity < 0:
            velocity *= reverse_friction
        else:
            velocity *= friction
        if abs(velocity) < 1e-4:
            velocity = 0

    car_x += velocity

    window.fill((30, 30, 30))  # Clear screen with dark gray
    pygame.draw.rect(window, car_color, (int(car_x), int(car_y), car_width, car_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()