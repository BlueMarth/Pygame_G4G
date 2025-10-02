"""
Car Simulation Controls:

W / Up Arrow    : Accelerate forward
S / Down Arrow  : Brake and reverse
A / Left Arrow  : Steer left
D / Right Arrow : Steer right
Space           : Handbrake

Use WASD or arrow keys to control the car.
"""
import pygame
import math
import os
from vehicle_drive.Vehicle import Car

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Car Simulation (Class-based)")
clock = pygame.time.Clock()

# Car parameters
default_params = {
    'length': 100,
    'width': 40,
    'max_velocity': 6,
    'reverse_max_velocity': -2,
    'acceleration': 0.2,
    'friction': 0.99,
    'reverse_friction': 0.97,
    'handbrake_strength': 0.9,
    'max_steering_deg': 35,
    'steering_speed_deg': 2.5,
    'wheelbase': 80,
    'rear_bumper_offset': 10  # distance from rear axle to rear bumper
}

# Load and scale car image
car_img_path = os.path.join('visual', 'red_car_top.png')
car_img_raw = pygame.image.load(car_img_path).convert_alpha()
car_img = pygame.transform.smoothscale(car_img_raw, (default_params['length'], default_params['width']))

car = Car(x=100, y=300, params=default_params)

running = True
dt = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    keymap = {
        'w': keys[pygame.K_w],
        'a': keys[pygame.K_a],
        's': keys[pygame.K_s],
        'd': keys[pygame.K_d],
        'up': keys[pygame.K_UP],
        'down': keys[pygame.K_DOWN],
        'left': keys[pygame.K_LEFT],
        'right': keys[pygame.K_RIGHT],
        'space': keys[pygame.K_SPACE],
    }
    control = car.handle_input(keymap)
    car.update(control, dt)

    window.fill((30, 30, 30))
    # Draw car as a rotated image, with rear axle at (car.x, car.y)
    center = (int(car.x), int(car.y))
    angle = car.angle
    # Offset from image center to rear axle in local coordinates
    rear_bumper_offset = car.rear_bumper_offset
    car_length = car.length
    car_width = car.width
    # In image coordinates, rear axle is at (rear_bumper_offset, car_width/2)
    local_axle = (rear_bumper_offset, car_width/2)
    img_center = (car_length/2, car_width/2)
    # Vector from image center to rear axle
    center_to_axle = (local_axle[0] - img_center[0], local_axle[1] - img_center[1])
    # Rotate this vector
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rot_x = cos_a * center_to_axle[0] - sin_a * center_to_axle[1]
    rot_y = sin_a * center_to_axle[0] + cos_a * center_to_axle[1]
    # Rotate image
    rotated_car = pygame.transform.rotate(car_img, -math.degrees(angle))
    rot_rect = rotated_car.get_rect()
    # Blit so that rear axle is at (car.x, car.y)
    blit_x = center[0] - rot_rect.width//2 - int(rot_x)
    blit_y = center[1] - rot_rect.height//2 - int(rot_y)
    window.blit(rotated_car, (blit_x, blit_y))
    # Draw heading arrow
    arrow_length = 60
    arrow_color = (0, 255, 0)
    end_pos = (
        int(center[0] + arrow_length * math.cos(angle)),
        int(center[1] + arrow_length * math.sin(angle))
    )
    pygame.draw.line(window, arrow_color, center, end_pos, 4)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
