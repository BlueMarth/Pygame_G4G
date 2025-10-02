"""
Helicopter Simulation Controls:

W / Up Arrow    : Increase forward speed
S               : Descend (decrease altitude)
Space           : Ascend (increase altitude)
A / Left Arrow  : Turn left (yaw)
D / Right Arrow : Turn right (yaw)

Move with WASD or arrow keys. Hold Space to go up, S to go down.
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
    'max_velocity': 8,
    'acceleration': 0.2,
    'friction': 0.98,
    'altitude': 0.0,
    'vertical_acceleration': 0.2
}

heli = Helicopter(x=400, y=300, params=default_params)


font = pygame.font.SysFont(None, 24)

# Altitude bar parameters
ALT_BAR_MAX_HEIGHT = 200
ALT_BAR_WIDTH = 20
ALT_BAR_X = 10
ALT_BAR_Y = 10
ALT_BAR_BG_COLOR = (80, 80, 80)
ALT_BAR_FG_COLOR = (0, 200, 255)
ALT_BAR_BORDER_COLOR = (255, 255, 255)

running = True
dt = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Map pygame keys to string keys for handle_input

    # --- Double-tap and hold SPACE for descend ---
    if not hasattr(heli, '_space_last'):
        heli._space_last = 0
        heli._space_down = False
        heli._space_double_tap = False
        heli._space_tap_timer = 0

    now = pygame.time.get_ticks()
    space_pressed = keys[pygame.K_SPACE]
    if space_pressed and not heli._space_down:
        if now - heli._space_last < 400:
            heli._space_double_tap = True
        heli._space_last = now
        heli._space_down = True
        heli._space_tap_timer = now
    elif not space_pressed:
        heli._space_down = False
        if now - heli._space_tap_timer > 400:
            heli._space_double_tap = False
    descend = heli._space_double_tap and space_pressed

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
        'descend': descend
    }

    control = heli.handle_input(keymap)
    heli.update(control, dt)

    # Clamp altitude between 0 and 1000
    heli.altitude = max(0, min(heli.altitude, 1000))

    window.fill((30, 30, 60))
    # Draw helicopter as a simple circle for now, with size based on altitude
    center = (int(heli.x), int(heli.y))
    base_radius = 20
    max_scale = 1.2  # 20% increase at max altitude
    scale = 1.0 + 0.4 * (heli.altitude / 1000)
    radius = int(base_radius * scale)
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

    # Draw altitude as a vertical bar (top left)
    bar_height = int((heli.altitude / 1000) * ALT_BAR_MAX_HEIGHT)
    bar_rect_bg = pygame.Rect(ALT_BAR_X, ALT_BAR_Y, ALT_BAR_WIDTH, ALT_BAR_MAX_HEIGHT)
    bar_rect_fg = pygame.Rect(ALT_BAR_X, ALT_BAR_Y + ALT_BAR_MAX_HEIGHT - bar_height, ALT_BAR_WIDTH, bar_height)
    pygame.draw.rect(window, ALT_BAR_BG_COLOR, bar_rect_bg)  # background
    pygame.draw.rect(window, ALT_BAR_FG_COLOR, bar_rect_fg)  # altitude
    pygame.draw.rect(window, ALT_BAR_BORDER_COLOR, bar_rect_bg, 2)  # border

    # --- Draw lift curve (top right) ---
    # Get lift/drag/ground effect params from the helicopter object
    try:
        base_lift = heli.lift
        ground_effect_strength = heli.ground_effect_strength
        lift_decay_rate = heli.lift_decay_rate
        max_altitude = heli.max_altitude
    except AttributeError:
        # fallback for old class version
        base_lift = getattr(heli, 'vertical_acceleration', 0.2)
        ground_effect_strength = 1.5
        lift_decay_rate = 2.0
        max_altitude = 1000

    # Curve dimensions
    curve_w = 200
    curve_h = 120
    curve_x = window_size[0] - curve_w - 20
    curve_y = 20
    # Draw background
    pygame.draw.rect(window, (30, 30, 40), (curve_x, curve_y, curve_w, curve_h))
    pygame.draw.rect(window, (200, 200, 200), (curve_x, curve_y, curve_w, curve_h), 2)
    # Draw axes
    pygame.draw.line(window, (180,180,180), (curve_x+40, curve_y+curve_h-20), (curve_x+curve_w-10, curve_y+curve_h-20), 1)
    pygame.draw.line(window, (180,180,180), (curve_x+40, curve_y+10), (curve_x+40, curve_y+curve_h-20), 1)
    # Plot lift curve
    last_px, last_py = None, None
    for i in range(curve_w-60):
        alt = (i/(curve_w-60)) * max_altitude
        ground_effect = ground_effect_strength * math.exp(-alt / (max_altitude / lift_decay_rate))
        eff_lift = base_lift * (1 + ground_effect)
        # Normalize to fit curve height
        y = curve_y+curve_h-20 - int((eff_lift/base_lift-1) * (curve_h-30) / ground_effect_strength)
        x = curve_x+40+i
        if last_px is not None:
            pygame.draw.line(window, (0,200,255), (last_px,last_py), (x,y), 2)
        last_px, last_py = x, y
    # Draw current altitude marker
    cur_alt = heli.altitude
    cur_x = curve_x+40+int((cur_alt/max_altitude)*(curve_w-60))
    ground_effect = ground_effect_strength * math.exp(-cur_alt / (max_altitude / lift_decay_rate))
    eff_lift = base_lift * (1 + ground_effect)
    cur_y = curve_y+curve_h-20 - int((eff_lift/base_lift-1) * (curve_h-30) / ground_effect_strength)
    pygame.draw.circle(window, (255,0,0), (cur_x, cur_y), 5)
    # Draw labels
    font_s = pygame.font.SysFont(None, 18)
    window.blit(font_s.render("Lift Curve", True, (220,220,220)), (curve_x+60, curve_y+2))
    window.blit(font_s.render("Altitude", True, (180,180,180)), (curve_x+curve_w//2-20, curve_y+curve_h-16))
    window.blit(font_s.render("Lift", True, (180,180,180)), (curve_x+2, curve_y+20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
