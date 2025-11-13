"""
Helicopter Controls:

W / Up Arrow    : Tilt rotor forward (accelerate forward)
S / Down Arrow  : Tilt rotor backward (accelerate backward)
A / Left Arrow  : Tilt rotor left (left slide)
D / Right Arrow : Tilt rotor right (right slide)
Q               : Yaw left
E               : Yaw right
Space           : Increase lift (more upward force)
Shift           : Reduce lift (less upward force)

"""
import pygame
import math
import os
from vehicle_drive.Vehicle import Helicopter

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Helicopter Simulation")
clock = pygame.time.Clock()

# Helicopter parameters
default_params = {
    'mass': 1.0,
    'hor_drag': 0.03,
    'lift_force': 0.5,
    'roll_force': 0.2,
    'pitch_force': 0.2,
    'yaw_force': 0.2,
}

heli = Helicopter(x=400, y=300, z=100, angle=0, params=default_params)


font = pygame.font.SysFont(None, 24)


# Altitude bar parameters
ALT_BAR_MAX_HEIGHT = 200
ALT_BAR_WIDTH = 20
ALT_BAR_X = 20
ALT_BAR_Y = 30
ALT_BAR_BG_COLOR = (80, 80, 80)
ALT_BAR_FG_COLOR = (0, 200, 255)
ALT_BAR_BORDER_COLOR = (255, 255, 255)

running = True
dt = 1

# define other variables here
heli_size = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Map pygame keys to string keys for handle_input
    keymap = {
        'w': keys[pygame.K_w],
        'a': keys[pygame.K_a],
        's': keys[pygame.K_s],
        'd': keys[pygame.K_d],
        'q': keys[pygame.K_q],
        'e': keys[pygame.K_e],
        'space': keys[pygame.K_SPACE],
        'Lshift': keys[pygame.K_LSHIFT],
    }

    control = heli.handle_input(keymap)
    heli.update(control, dt)

    # Clamp altitude between 0 and 1000
    heli.x = max(0, min(heli.x, window_size[0]))
    heli.y = max(0, min(heli.y, window_size[1]))
    heli.z = max(0, min(heli.z, 1000))

    window.fill((30, 30, 60))
    # Draw helicopter as a simple circle for now, with size based on altitude
    center = (int(heli.x), int(heli.y))
    radius = int(heli_size)
    pygame.draw.circle(window, (200, 200, 50), center, radius)

    # Draw heading arrow for debug
    arrow_length = 40
    arrow_color = (255, 0, 0)
    end_pos = (
        int(center[0] + arrow_length * math.cos(heli.angle)),
        int(center[1] + arrow_length * math.sin(heli.angle))
    )
    pygame.draw.line(window, arrow_color, center, end_pos, 4)
    # Optional: draw arrowhead
    head_size = 10
    head_angle = math.pi / 6
    left_head = (
        int(end_pos[0] - head_size * math.cos(heli.angle - head_angle)),
        int(end_pos[1] - head_size * math.sin(heli.angle - head_angle))
    )
    right_head = (
        int(end_pos[0] - head_size * math.cos(heli.angle + head_angle)),
        int(end_pos[1] - head_size * math.sin(heli.angle + head_angle))
    )
    pygame.draw.polygon(window, arrow_color, [end_pos, left_head, right_head])

    # Draw altitude as an empty vertical bar (background) with a thin line marker
    bar_height = int((heli.z / 1000) * ALT_BAR_MAX_HEIGHT)
    bar_rect_bg = pygame.Rect(ALT_BAR_X, ALT_BAR_Y, ALT_BAR_WIDTH, ALT_BAR_MAX_HEIGHT)
    pygame.draw.rect(window, ALT_BAR_BG_COLOR, bar_rect_bg) # background (empty)
    pygame.draw.rect(window, ALT_BAR_BORDER_COLOR, bar_rect_bg, 2) # border
    # thin horizontal line to indicate current altitude, clamp within bar
    marker_y = ALT_BAR_Y + ALT_BAR_MAX_HEIGHT - bar_height
    marker_y = max(ALT_BAR_Y, min(ALT_BAR_Y + ALT_BAR_MAX_HEIGHT, marker_y))
    line_padding = 4
    x1 = ALT_BAR_X - line_padding
    x2 = ALT_BAR_X + ALT_BAR_WIDTH + line_padding - 1
    pygame.draw.line(window, ALT_BAR_FG_COLOR, (x1, marker_y), (x2, marker_y), 3)
    text_surface = font.render(str(int(heli.z)), True, (255, 255, 255))
    window.blit(text_surface, (ALT_BAR_X + ALT_BAR_WIDTH + 10, 20))

    # --- Draw lift info (top right) ---
    # Use helicopter attributes: lift_force (N) and mass (kg) to compute vertical accel = lift_force / mass
    base_lift_force = getattr(heli, 'lift_force', getattr(heli, 'lift', 0.2))
    mass = getattr(heli, 'mass', 1.0)
    lift_acc = base_lift_force / mass
    # Curve dimensions
    curve_w = 200
    curve_h = 120
    curve_x = window_size[0] - curve_w - 20
    curve_y = 20
    # Draw background and border
    pygame.draw.rect(window, (30, 30, 40), (curve_x, curve_y, curve_w, curve_h))
    pygame.draw.rect(window, (200, 200, 200), (curve_x, curve_y, curve_w, curve_h), 2)
    # Axes
    pygame.draw.line(window, (180,180,180), (curve_x+40, curve_y+curve_h-20), (curve_x+curve_w-10, curve_y+curve_h-20), 1)
    pygame.draw.line(window, (180,180,180), (curve_x+40, curve_y+10), (curve_x+40, curve_y+curve_h-20), 1)
    # Plot a flat line representing available lift acceleration (no ground effect in current Helicopter)
    # Normalize by a reasonable maximum for display (e.g., 2*g)
    g = 9.80665
    max_display = max(lift_acc * 1.2, 2 * g)
    y_lift = curve_y+curve_h-20 - int((lift_acc / max_display) * (curve_h-30))
    pygame.draw.line(window, (0,200,255), (curve_x+40, y_lift), (curve_x+curve_w-10, y_lift), 3)
    # Draw hover (g) line for reference
    y_hover = curve_y+curve_h-20 - int((g / max_display) * (curve_h-30))
    pygame.draw.line(window, (255,255,0), (curve_x+40, y_hover), (curve_x+curve_w-10, y_hover), 1)
    # Draw current altitude marker (heli.z)
    max_altitude = 1000
    cur_alt = getattr(heli, 'z', 0.0)
    cur_x = curve_x+40+int((cur_alt/max_altitude)*(curve_w-60))
    pygame.draw.circle(window, (255,0,0), (cur_x, y_lift), 5)
    # Labels
    font_s = pygame.font.SysFont(None, 18)
    window.blit(font_s.render("Lift (m/s^2)", True, (220,220,220)), (curve_x+60, curve_y+2))
    window.blit(font_s.render("Altitude", True, (180,180,180)), (curve_x+curve_w//2-20, curve_y+curve_h-16))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
