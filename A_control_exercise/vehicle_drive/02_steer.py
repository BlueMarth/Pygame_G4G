import math
import numpy as np
import pygame

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Steering direction Simulation")
clock = pygame.time.Clock()

# sprite
arrow_length = 60
arrow_width = 15
car_color = (255, 0, 0)  # Red

car_x = 400
car_y = 300
steer_angle = 0
steer_speed = 4  # degrees per frame
max_steer = 36  # max steering angle in degrees
centering_speed = 2      # degrees per frame to return to center

running = True
# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Steering control with A and D
    if keys[pygame.K_a]:
        steer_angle -= steer_speed
        if steer_angle < -max_steer:
            steer_angle = -max_steer
    elif keys[pygame.K_d]:
        steer_angle += steer_speed
        if steer_angle > max_steer:
            steer_angle = max_steer
    else:
        # Auto-centering
        if steer_angle > 0:
            steer_angle -= centering_speed
            if steer_angle < 0:
                steer_angle = 0
        elif steer_angle < 0:
            steer_angle += centering_speed
            if steer_angle > 0:
                steer_angle = 0

    window.fill((30, 30, 30))  # Clear screen with dark gray
    # Draw a long thin arrow (triangle) rotated by steer_angle
    # Arrow points up at 0 degrees
    angle_rad = math.radians(steer_angle)
    # Define arrow points relative to (0,0)
    tip = (0, -arrow_length)
    left = (-arrow_width//2, 0)
    right = (arrow_width//2, 0)
    # Rotate points
    def rotate_point(pt, angle):
        x, y = pt
        xr = x * math.cos(angle) - y * math.sin(angle)
        yr = x * math.sin(angle) + y * math.cos(angle)
        return (xr, yr)
    tip_r = rotate_point(tip, angle_rad)
    left_r = rotate_point(left, angle_rad)
    right_r = rotate_point(right, angle_rad)
    # Translate to car_x, car_y
    points = [
        (car_x + tip_r[0], car_y + tip_r[1]),
        (car_x + left_r[0], car_y + left_r[1]),
        (car_x + right_r[0], car_y + right_r[1])
    ]
    pygame.draw.polygon(window, car_color, points)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()