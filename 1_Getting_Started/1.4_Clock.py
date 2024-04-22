import pygame
pygame.init()
i = 0
clock = pygame.time.Clock()

while i<5:
    # setting max 1 fps
    clock.tick(1)
    # print time used in the previous tick
    print(clock.get_time())
    # print compute the clock framerate
    print(clock.get_fps())
    i = i + 1