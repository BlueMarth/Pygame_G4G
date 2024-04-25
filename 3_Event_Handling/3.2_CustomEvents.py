## kinda stuck at inflating, come back at it later :/

import pygame
pygame.init()

colours = {
    "white":    (255, 255, 255),
    "gray":     (127, 127, 127),
    "black":    (255, 255, 255),
    "red":      (255, 87, 51),
    "yellow":   (255, 87, 51),
    "green":    (80, 200, 120),
    "blue":     (0, 127, 255),
    "purple":   (200, 162, 200)
}

screen = pygame.display.set_mode((600,300))
screen.fill("gray")
timer = pygame.time.Clock()

pygame.display.set_caption("Custom Events")
pygame.display.set_icon(pygame.image.load("visual/github_icon.png"))

# custom events
CHANGE_COLOUR = pygame.USEREVENT + 1
ON_RED = pygame.USEREVENT + 2
ON_BLUE = pygame.USEREVENT + 3
ON_YELLOW = pygame.USEREVENT + 4
ON_GREEN = pygame.USEREVENT + 5

red_box = pygame.Rect((25, 100, 100, 100))
blue_box = pygame.Rect((175, 100, 100, 100))
yellow_box = pygame.Rect((325, 100, 100, 100))
green_box = pygame.Rect((475, 100, 100, 100))

grow = True

#pygame.time.set_timer(CHANGE_COLOUR, 500)

running = True
while running:

    for event in pygame.event.get():
        
        if event.type == ON_RED:
            if grow:
                red_box.inflate_ip(2, 2)
                grow = red_box.width < 120
            else:
                red_box.inflate_ip(-2, -2)
                grow = red_box.width < 100

        if event.type == ON_BLUE:
            if grow:
                blue_box.inflate_ip(2, 2)
                grow = blue_box.width < 120
            else:
                blue_box.inflate_ip(-2, -2)
                grow = blue_box.width < 100

        if event.type == ON_YELLOW:
            if grow:
                yellow_box.inflate_ip(2, 2)
                grow = yellow_box.width < 120
            else:
                yellow_box.inflate_ip(-2, -2)
                grow = yellow_box.width < 100
        
        if event.type == ON_GREEN:
            if grow:
                green_box.inflate_ip(2, 2)
                grow = green_box.width < 120
            else:
                green_box.inflate_ip(-2, -2)
                grow = green_box.width < 100

        #if event.type == CHANGE_COLOUR:
        #    pass

        if event.type == pygame.QUIT:
            running = False

    if red_box.collidepoint(pygame.mouse.get_pos()):
        pygame.event.post(pygame.event.Event(ON_RED))
    if blue_box.collidepoint(pygame.mouse.get_pos()):
        pygame.event.post(pygame.event.Event(ON_BLUE))
    if yellow_box.collidepoint(pygame.mouse.get_pos()):
        pygame.event.post(pygame.event.Event(ON_YELLOW))
    if green_box.collidepoint(pygame.mouse.get_pos()):
        pygame.event.post(pygame.event.Event(ON_GREEN))
    
    pygame.draw.rect(screen, "red", red_box)
    pygame.draw.rect(screen, "blue", blue_box)
    pygame.draw.rect(screen, "yellow", yellow_box)
    pygame.draw.rect(screen, "green", green_box)

    pygame.display.update()
    print(grow, red_box.width, blue_box.width, yellow_box.width, green_box.width)
    
    timer.tick(30) # frame per second

pygame.quit()