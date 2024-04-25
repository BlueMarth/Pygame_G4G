import pygame

pygame.font.init()

pygame.font.get_init() # check whetehr font is initilized

colours = {
    "white":    (255, 255, 255),
    "gray":     (127, 127, 127),
    "black":    (255, 255, 255),
    "red":      (255, 87, 51),
    "yellow":   (87, 255, 51),
    "green":    (80, 200, 120),
    "blue":     (0, 127, 255),
    "purple":   (200, 162, 200)
}

size = width, height = 500, 500
display_surface = pygame.display.set_mode(size)
pygame.display.set_caption("Our Text")

# passing font file and size
font1 = pygame.font.SysFont('freesanbold.ttf', 50)
font2 = pygame.font.SysFont('chalfduster.ttf', 40)

# render texts to display
text1 = font1.render('G4g', True, "green")
text2 = font2.render('G4g', True, "green")

# create a rectangular object for the text surface object
textRect1 = text1.get_rect()
textRect2 = text2.get_rect()

# setting center of of the reactangles
textRect1.center = (250,250)
textRect2.center = (250,300)

while True:
    display_surface.fill("black")

    display_surface.blit(text1, textRect1)
    display_surface.blit(text2, textRect2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()