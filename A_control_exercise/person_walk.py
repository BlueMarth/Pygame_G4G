import pygame
import math

pygame.init()
SIZE = [600, 400]
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Person Walk")
clock = pygame.time.Clock()
fps = 60

# Colors
HEAD_COLOR = (255, 0, 0)
SHOULDER_COLOR = (0, 255, 0)

# Person properties
x, y = SIZE[0]//2, SIZE[1]//2 #only initial position
head_radius = 10
shoulder_width = 34
shoulder_height = 12

speed = 2
move_x, move_y = 0, 0
angle = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse-based direction, space to walk
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - x
    dy = mouse_y - y
    angle = math.degrees(math.atan2(dy, dx)) if dx != 0 or dy != 0 else angle

    keys = pygame.key.get_pressed()
    walking = keys[pygame.K_SPACE]
    if walking and (dx != 0 or dy != 0):
        dist = math.hypot(dx, dy)
        if dist > 0:
            move_x = (dx / dist) * speed
            move_y = (dy / dist) * speed
        else:
            move_x = move_y = 0
    else:
        move_x = move_y = 0


    # Move and clamp
    x += int(move_x)
    y += int(move_y)
    x = max(head_radius, min(SIZE[0]-head_radius, x))
    y = max(head_radius, min(SIZE[1]-head_radius-shoulder_height, y))

    window.fill((0,0,0))

    # Draw shoulders (rotated ellipse, width always major axis)
    shoulders_cx = x + int((head_radius+shoulder_height//2)*math.cos(math.radians(angle)))
    shoulders_cy = y + int((head_radius+shoulder_height//2)*math.sin(math.radians(angle)))
    major = max(shoulder_width, shoulder_height)
    minor = min(shoulder_width, shoulder_height)
    rect = pygame.Rect(0, 0, major, minor)
    rect.center = (shoulders_cx, shoulders_cy)
    shoulder_surf = pygame.Surface((major, minor), pygame.SRCALPHA)
    pygame.draw.ellipse(shoulder_surf, SHOULDER_COLOR, [0, 0, major, minor])
    pygame.draw.ellipse(shoulder_surf, (0,0,0), [0, 0, major, minor], 2)
    rotated_shoulder = pygame.transform.rotate(shoulder_surf, -angle)
    rot_rect = rotated_shoulder.get_rect(center=rect.center)
    window.blit(rotated_shoulder, rot_rect)

    # Draw head (rotated)
    head_cx = x + int((head_radius+shoulder_height)*math.cos(math.radians(angle)))
    head_cy = y + int((head_radius+shoulder_height)*math.sin(math.radians(angle)))
    pygame.draw.circle(window, HEAD_COLOR, (head_cx, head_cy), head_radius)
    pygame.draw.circle(window, (0,0,0), (head_cx, head_cy), head_radius, 2)

    # Draw direction triangle (rotated with head)
    # tri_len = head_radius
    # tri_angle = math.radians(angle)
    # triangle_points = [
    #     (head_cx + tri_len * math.cos(tri_angle), head_cy + tri_len * math.sin(tri_angle)),
    #     (head_cx + tri_len * math.cos(tri_angle + 2.5), head_cy + tri_len * math.sin(tri_angle + 2.5)),
    #     (head_cx + tri_len * math.cos(tri_angle - 2.5), head_cy + tri_len * math.sin(tri_angle - 2.5)),
    # ]
    # pygame.draw.polygon(window, (0,0,0), triangle_points)
    # pygame.draw.polygon(window, (255,255,255), triangle_points, 2)

    pygame.display.flip()
    clock.tick(fps)
