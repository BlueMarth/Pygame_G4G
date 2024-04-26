import pygame
pygame.init()

screen = pygame.display.set_mode((600,300))

options_img = pygame.image.load("visual/options_btn.png")
options_rect = options_img.get_rect()
options_rect.center = 100, 150
play_img = pygame.image.load("visual/play_btn.png")
play_rect = options_img.get_rect()
play_rect.center = 300, 150
quit_img = pygame.image.load("visual/quit_btn.png")
quit_rect = options_img.get_rect()
quit_rect.center = 500, 150


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
    screen.fill("gray2")
    screen.blit(options_img, options_rect)
    screen.blit(play_img, play_rect)
    screen.blit(quit_img, quit_rect)

    pygame.display.update()