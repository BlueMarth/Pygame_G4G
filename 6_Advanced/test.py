import pygame
pygame.init()

screen = pygame.display.set_mode((500,300))

img = pygame.image.load("visual/options_btn.png")
img_rect = img.get_rect()
img_rect.center = 250, 150

while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()
        
    screen.blit()