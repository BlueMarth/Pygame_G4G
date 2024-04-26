import pygame
import random
import math

pygame.init()
SIZE = [480, 270]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space")

stars = []

for i in range(100):
    x, y = SIZE[0]//2, SIZE[1]//2
    radius = random.randrange(2, 4)
    stars.append([x,y,radius])

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill("black")

    for i in range(len(stars)):
        pygame.draw.circle(screen, "yellow",
                           [stars[i][0],stars[i][1]], stars[i][2])
        angle = random.randrange(0,359)
        speed = stars[i][2] * 20
        stars[i][0] += speed * int(math.cos(angle/180*math.pi))
        stars[i][1] += speed * int(math.sin(angle/180*math.pi))
        
        if (stars[i][0]<0 or stars[i][0]>SIZE[0]) or (0 > stars[i][1] > SIZE[1]):
            stars[i][0] = SIZE[0]//2
            
    pygame.display.flip()
    clock.tick(60)
pygame.quit