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
CAR_COLOR = (255, 0, 0)  # Red

# Initial position (centered)
car_x = 100
car_y = 300
velocity = 0
acceleration = 0.2
max_velocity = 8
reverse_max_velocity = -2  # Lower top speed for reverse
friction = 0.97

# Kinematic Bicycle Model parameters
WHEELBASE = 40  # pixels (distance between axles)
car_angle = 0   # radians, heading
steering_angle = 0  # radians
max_steering_deg = 30
steering_speed_deg = 2
max_steering = math.radians(max_steering_deg)
steering_speed = math.radians(steering_speed_deg)

# Arrow geometry for steering visualization
arrow_length = 80
arrow_head_size = 16
arrow_head_angle = math.pi / 8

# Center of rotation offset (20% from rear)
center_offset = 0.2 * CAR_LENGTH

running = True
# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((30, 30, 30))  # Clear screen with dark gray

    keys = pygame.key.get_pressed()
    # --- Acceleration/Reverse ---
    if keys[pygame.K_w]:
        velocity += acceleration
        if velocity > max_velocity:
            velocity = max_velocity
    elif keys[pygame.K_s]:
        velocity -= acceleration
        if velocity < reverse_max_velocity:
            velocity = reverse_max_velocity
    else:
        velocity *= friction
        if abs(velocity) < 0.01:
            velocity = 0

    # --- Steering (separate kinematics) ---
    if keys[pygame.K_a]:
        steering_angle -= steering_speed
        if steering_angle < -max_steering:
            steering_angle = -max_steering
    elif keys[pygame.K_d]:
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
    # Update position and heading using the model
    # The reference point (car_x, car_y) is now 20% from the rear
    car_x += velocity * math.cos(car_angle)
    car_y += velocity * math.sin(car_angle)
    if abs(steering_angle) > 1e-4:
        car_angle += (velocity / WHEELBASE) * math.tan(steering_angle)

    # Draw car as a rotated rectangle, with rotation center 20% from rear
    car_rect = pygame.Rect(0, 0, CAR_LENGTH, CAR_WIDTH)
    # Compute the center of rotation in local car coordinates
    # (0,0) is topleft, so offset from rear is (center_offset, CAR_WIDTH/2)
    local_center = (center_offset, CAR_WIDTH/2)
    # Compute the world position of the center of rotation
    car_center = (int(car_x), int(car_y))
    # Create car surface
    car_surf = pygame.Surface((CAR_LENGTH, CAR_WIDTH), pygame.SRCALPHA)
    car_surf.fill(CAR_COLOR)
    # Rotate the car surface
    rotated_car = pygame.transform.rotate(car_surf, -math.degrees(car_angle))
    # To blit so that the center of rotation is at car_x, car_y:
    # Find the offset from the local center to the surface center, rotate it, and adjust blit position
    surf_center = (CAR_LENGTH/2, CAR_WIDTH/2)
    offset_x = surf_center[0] - local_center[0]
    offset_y = surf_center[1] - local_center[1]
    cos_a = math.cos(car_angle)
    sin_a = math.sin(car_angle)
    rot_offset_x = cos_a * offset_x - sin_a * offset_y
    rot_offset_y = sin_a * offset_x + cos_a * offset_y
    blit_x = car_center[0] - rotated_car.get_width()//2 + int(rot_offset_x)
    blit_y = car_center[1] - rotated_car.get_height()//2 + int(rot_offset_y)
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