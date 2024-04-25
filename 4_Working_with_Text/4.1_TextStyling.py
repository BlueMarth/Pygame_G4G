import pygame

pygame.font.init()

pygame.font.get_init() # check whetehr font is initilized

size = width, height = 500, 500
display_surface = pygame.display.set_mode(size)

pygame.display.set_caption("Our Text")
font1 = pygame.font.SysFont('freesanbold.ttf', 50)
font2 = pygame.font.SysFont('chalfduster.ttf', 50)