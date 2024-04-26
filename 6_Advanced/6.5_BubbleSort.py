import pygame
import random
pygame.init()

SIZE = [500,400]
screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Bubble Sort")

x = 40
y = 40

width = 20
height = []
for i in range(14):
    height.append(random.randrange(1, 250))

def show(height):
    for i in range(len(height)):
        pygame.draw.rect(screen, "red", (x+30*i, y, width, height[i]))

while True:
    
    execute = False
    
    pygame.time.delay(10)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    if keys[pygame.K_SPACE]:
        execute = True
    
    if execute == False:
        screen.fill("black")
        show(height)
        pygame.display.update
    else:
        for i in range(len(height)-1):
            for j in range(len(height)-i-1):
                if height[j] > height[j+1]:
                    #swap
                    temp = height[j]
                    height[j] = height[j+1]
                    height[j+1] = temp
                screen.fill("black")
                show(height)
                pygame.time.delay(40)
                pygame.display.update
