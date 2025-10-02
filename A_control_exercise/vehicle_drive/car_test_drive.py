import os
import math
import numpy as np
import pygame
import kinematic_bicycle_model as kbm

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Car Drive Simulation")
fps = 60
clock = pygame.time.Clock()

# sprite
CAR_LENGTH = 100
CAR_WIDTH = 40

# Car image loading and scaling
car_img_path = os.path.join('visual', 'red_car_top.png')
car_img_raw = pygame.image.load(car_img_path).convert_alpha()
car_img = pygame.transform.smoothscale(car_img_raw, (CAR_LENGTH, CAR_WIDTH))
CAR_COLOR = (255, 0, 0)  # Red

# Initial position (centered)
car_x = 100
car_y = 300
velocity = 0
acceleration = 0.2
max_velocity = 6
reverse_max_velocity = -2  # Lower top speed for reverse
friction = 0.99
reverse_friction = 0.97 # Stronger friction when reversing
handbrake_strength = 0.9 # Deceleration per frame when handbrake (space) is pressed

# Kinematic Bicycle Model parameters
# Define distance from front bumper to front axle
front_axle_offset = 0.1 * CAR_LENGTH
# Center of rotation offset (20% from rear)
rear_axle_offset = 0.2 * CAR_LENGTH
# Calculate wheelbase as distance between axles
WHEELBASE = CAR_LENGTH - front_axle_offset - rear_axle_offset
car_angle = 0   # radians, heading
steering_angle = 0  # radians
max_steering_deg = 35
steering_speed_deg = 2.5
max_steering = math.radians(max_steering_deg)
steering_speed = math.radians(steering_speed_deg)

# Arrow geometry for steering visualization
arrow_length = 80
arrow_head_size = 16
arrow_head_angle = math.pi / 8
running = True
dt = 1
# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((30, 30, 30))  # Clear screen with dark gray

    keys = pygame.key.get_pressed()
    # --- Acceleration ---
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        velocity += acceleration
        if velocity > max_velocity:
            velocity = max_velocity
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        velocity -= acceleration
        if velocity < reverse_max_velocity:
            velocity = reverse_max_velocity
    elif keys[pygame.K_SPACE]:
        if velocity != 0:
            velocity *= handbrake_strength
        elif abs(velocity) < 1e-4:
            velocity = 0
    else:
        velocity *= friction
        if abs(velocity) < 1e-4:
            velocity = 0

    # --- Steering ---
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        steering_angle -= steering_speed
        if steering_angle < -max_steering:
            steering_angle = -max_steering
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        steering_angle += steering_speed
        if steering_angle > max_steering:
            steering_angle = max_steering
    else:
        # Auto-centering
        if steering_angle > 0:
            steering_angle -= steering_speed
            if steering_angle < 0:
                steering_angle = 0
        elif steering_angle < 0:
            steering_angle += steering_speed
            if steering_angle > 0:
                steering_angle = 0

    # --- Kinematic Bicycle Model update ---
    # Use imported kbm function
    car_x, car_y, car_angle = kbm.kinematic_bicycle_model(
        car_x, car_y, car_angle, velocity, steering_angle, WHEELBASE, dt
    )

    # Calculate turn radius (for display or debug)
    if abs(steering_angle) > 1e-4:
        turn_radius = WHEELBASE / math.tan(steering_angle)
    else:
        turn_radius = float('inf')

    # Draw car as a rotated image, with rotation center 20% from rear
    # Compute the center of rotation in local car coordinates (relative to image topleft)
    local_center = (rear_axle_offset, CAR_WIDTH/2)
    car_center = (int(car_x), int(car_y))
    # Rotate the car image
    rotated_car = pygame.transform.rotate(car_img, -math.degrees(car_angle))
    # After rotation, the center of rotation moves; get the new offset
    # Get the rect of the original image, and the rect of the rotated image
    orig_rect = car_img.get_rect()
    rot_rect = rotated_car.get_rect()
    # The vector from the image center to the rotation center (in original image)
    center_to_rot = (local_center[0] - orig_rect.width/2, local_center[1] - orig_rect.height/2)
    # Rotate this vector
    cos_a = math.cos(car_angle)
    sin_a = math.sin(car_angle)
    rot_x = cos_a * center_to_rot[0] - sin_a * center_to_rot[1]
    rot_y = sin_a * center_to_rot[0] + cos_a * center_to_rot[1]
    # The blit position is car_center minus the offset from rotated image center to rotation center
    blit_x = car_center[0] - rot_rect.width//2 - int(rot_x)
    blit_y = car_center[1] - rot_rect.height//2 - int(rot_y)
    window.blit(rotated_car, (blit_x, blit_y))

    # Draw steering state as a thin arrow from car center in the direction of the front wheel
    arrow_angle = car_angle + steering_angle
    start_pos = car_center
    end_pos = (
        int(car_center[0] + arrow_length * math.cos(arrow_angle)),
        int(car_center[1] + arrow_length * math.sin(arrow_angle))
    )
    pygame.draw.line(window, (0, 255, 0), start_pos, end_pos, 3)
    # Draw arrowhead
    left_head = (
        int(end_pos[0] - arrow_head_size * math.cos(arrow_angle - arrow_head_angle)),
        int(end_pos[1] - arrow_head_size * math.sin(arrow_angle - arrow_head_angle))
    )
    right_head = (
        int(end_pos[0] - arrow_head_size * math.cos(arrow_angle + arrow_head_angle)),
        int(end_pos[1] - arrow_head_size * math.sin(arrow_angle + arrow_head_angle))
    )
    pygame.draw.polygon(window, (0, 255, 0), [end_pos, left_head, right_head])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()