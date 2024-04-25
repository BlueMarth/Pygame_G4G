import pygame
import time

pygame.init()

screen = pygame.display.set_mode()
x, y = screen.get_size()
pygame.display.quit()
x, y = int(x/2), int(y/2)
surface = pygame.display.set_mode((x, y))
print(x, y)
bgcolour = (84, 110, 122)
surface.fill(bgcolour)

paint = (240, 244, 195)
pygame.draw.rect(surface, paint,
                 pygame.Rect(30, 30, 90, 60))

# load an image in the centre of the window
image = pygame.image.load('visual/github_icon.png')
w, h = image.get_size()
w, h = int(x/2-w/2), int(y/2-h/2)
surface.blit(image, (w, h))
# blitting: copying pixels of on surface to another

# scaling image and setting colour key
image = pygame.transform.scale(image, (128, 128))
image = pygame.transform.rotate(image, 45)
#pygame.Surface.set_colorkey (image, [0, 0, 0])
print(pygame.Surface.get_colorkey(image))
surface.blit(image,(0,0))

pygame.display.flip()

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            surface.quit()