"""
Boat Simulation Controls:

W / Up Arrow    : Accelerate forward
A / Left Arrow  : Steer left
D / Right Arrow : Steer right

Boat cannot reverse. Use WASD or arrow keys to control.
"""
import pygame
import math
from vehicle_drive.Vehicle import Boat

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Boat Simulation")
clock = pygame.time.Clock()

# Boat parameters
default_params = {
    'length': 120,
    'width': 50,
    'max_velocity': 4,
    'acceleration': 0.1,
    'friction': 0.995,
    'steering_speed_deg': 1.5,
    'max_steering_deg': 25
}

boat = Boat(x=400, y=300, params=default_params)

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
        'd': keys[pygame.K_d],
        'up': keys[pygame.K_UP],
        'left': keys[pygame.K_LEFT],
        'right': keys[pygame.K_RIGHT],
    }
    control = boat.handle_input(keymap)
    boat.update(control, dt)

    window.fill((30, 60, 90))
    # Draw boat as a rotated rectangle
    center = (int(boat.x), int(boat.y))
    length = boat.length
    width = boat.width
    angle = boat.angle
    # Calculate rectangle corners
    corners = []
    for dx, dy in [(-length/2, -width/2), (length/2, -width/2), (length/2, width/2), (-length/2, width/2)]:
        x = center[0] + dx * math.cos(angle) - dy * math.sin(angle)
        y = center[1] + dx * math.sin(angle) + dy * math.cos(angle)
        corners.append((int(x), int(y)))
    pygame.draw.polygon(window, (100, 200, 255), corners)
    # Draw heading arrow
    arrow_length = 60
    arrow_color = (255, 0, 0)
    end_pos = (
        int(center[0] + arrow_length * math.cos(angle)),
        int(center[1] + arrow_length * math.sin(angle))
    )
    pygame.draw.line(window, arrow_color, center, end_pos, 4)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
