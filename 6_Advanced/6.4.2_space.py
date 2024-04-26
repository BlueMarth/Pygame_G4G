import pygame
import random
import math

pygame.init()
SIZE = [480, 270]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space")

stars = []

for i in range(250):
    x, y = SIZE[0]//2, SIZE[1]//2
    radius = random.randrange(1, 3)
    angle = random.randrange(0, 359)
    speed = radius
    stars.append([x,y,radius,angle,speed])

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill("black")

    for i in range(len(stars)):
        dist = math.sqrt((stars[i][0]-SIZE[0]//2)**2
                         + (stars[i][1]-SIZE[1]//2)**2)
        if dist > stars[i][2]:
            pygame.draw.circle(screen, "gray60",
                           [stars[i][0],stars[i][1]], stars[i][2])
        
        # compute displacement angle
        dx = (math.cos(stars[i][3] / 180 * math.pi))
        dy = (math.sin(stars[i][3] / 180 * math.pi))
        
        # the closer the faster
        if dist < 1:
            dist = 2
        
        stars[i][4] = dist * stars[i][2] / 30
        
        stars[i][0] += stars[i][4] * dx
        stars[i][1] += stars[i][4] * dy
        
        if dist > stars[i][2] + 2:
            pygame.draw.circle(screen, "gray40",
                           [stars[i][0],stars[i][1]], stars[i][2])

        if (((stars[i][0] <= 0) or (stars[i][0] >= SIZE[0]))
            or ((stars[i][1] <= 0) or (stars[i][1] >= SIZE[1]))):
            stars[i][0] = SIZE[0]//2
            stars[i][1] = SIZE[1]//2
            stars[i][3] = random.randrange(0,359)
        
        

    pygame.display.flip()
    clock.tick(60)
pygame.quit