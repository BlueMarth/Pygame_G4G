import pygame
import random

pygame.init()
SIZE = [480, 270]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("The Matrix")

digitRain = []

for i in range(150):
    x = random.randrange(0, SIZE[0])
    y = random.randrange(0, SIZE[1])
    w = random.randrange(1,3)
    h = random.randrange(3,9)
    digitRain.append([x,y,w,h])

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill("black")

    for i in range(len(digitRain)):
        pygame.draw.rect(screen, "GREEN", digitRain[i])
        area = digitRain[i][2] * digitRain[i][3]
        digitRain[i][1] += area // 8
        if digitRain[i][1] > SIZE[1]:
            y = random.randrange(-40,-10)
            digitRain[i][1] = y
            x = random.randrange(0,SIZE[0])
            digitRain[i][0] = x
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit