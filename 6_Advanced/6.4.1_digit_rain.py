import pygame
import random
import math

pygame.init()
SIZE = [480, 270]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Digit Rain")

digitRain = []

for i in range(100):
    x = random.randrange(0, SIZE[0])
    y = random.randrange(0, SIZE[1])
    w = random.randrange(1,3)
    h = random.randrange(3,5)
    digitRain.append([x,y,w,h])

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill("black")

    for i in range(len(digitRain)):
        area = digitRain[i][2] * digitRain[i][3]
        if area > 9:
            color = "green"
        elif area > 5:
            color = "green2"
        else:
            color = "green3"
        pygame.draw.rect(screen, color, digitRain[i])
        digitRain[i][1] += math.sqrt(area)/2
        if digitRain[i][1] > SIZE[1]:
            digitRain[i][0] = random.randrange(-2, SIZE[0] + 2)
            digitRain[i][1] = random.randrange(-24, -12)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit