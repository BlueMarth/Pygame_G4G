import pygame
import random
import math

pygame.init()
SIZE = [1024, 512]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space")
fps = 60

color_list = ["gray15", "gray30", "gray45", "gray60"]
stars = []

for i in range(50):
    # Use polar coordinates for more natural spread
    min_dist = 30  # minimum distance from center
    max_dist = min(SIZE)//2 - 10  # max distance from center
    dist = random.uniform(min_dist, max_dist)
    angle = random.uniform(0, 2*math.pi)
    x = int(SIZE[0]//2 + dist * math.cos(angle))
    y = int(SIZE[1]//2 + dist * math.sin(angle))
    radius = random.randrange(1, 3)
    speed = radius / 2
    color = random.choice(color_list)
    stars.append([x, y, radius, angle, speed, color])

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill("black")
    
    for i in range(len(stars)):
        # compute distance of star from screen center
        dist = math.sqrt((stars[i][0]-SIZE[0]//2)**2
                         + (stars[i][1]-SIZE[1]//2)**2)
        
        # draw star only if close enough (further away from screen center)
        if dist > stars[i][2] * 2:
            pygame.draw.circle(screen, stars[i][5],
                           [stars[i][0],stars[i][1]], stars[i][2])
        
        # compute displacement angle
        dx = math.cos(stars[i][3])
        dy = math.sin(stars[i][3])

        # the closer the faster and bigger
        stars[i][0] += stars[i][4] * dx         # x position
        stars[i][1] += stars[i][4] * dy         # y position
        stars[i][4] = dist * stars[i][2] / 80   # speed
        stars[i][2] += math.sqrt(dist) / 80     # radius

        # reset star position once outside of window
        if (((stars[i][0] <= 0) or (stars[i][0] >= SIZE[0]))
            or ((stars[i][1] <= 0) or (stars[i][1] >= SIZE[1]))):
            min_dist = 30
            max_dist = min(SIZE)//2 - 10
            dist = random.uniform(min_dist, max_dist)
            angle = random.uniform(0, 2*math.pi)
            stars[i][0] = int(SIZE[0]//2 + dist * math.cos(angle))
            stars[i][1] = int(SIZE[1]//2 + dist * math.sin(angle))
            stars[i][2] = random.randrange(1,3)
            stars[i][3] = angle

    #print(stars)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit