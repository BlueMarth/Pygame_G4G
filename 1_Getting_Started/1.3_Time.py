import pygame
import sys

pygame.init()
temp = pygame.display.set_mode()
x, y = temp.get_size()
pygame.display.quit()
x, y = int(x/2), int(y/2)
display = pygame.display.set_mode((x, y))
print(x, y)
bgcolour = (84, 110, 122)
display.fill(bgcolour)
image = pygame.image.load('github_icon.png')
w, h = image.get_size()
w, h = int(x/2-w/2), int(y/2-h/2)
display.blit(image, (w, h))


# making the script wait for 1500 ms
pygame.time.wait(1500)
# less accurate because it uses sleeping

i = 0
while i<4:
    ticks = pygame.time.get_ticks()
    print(ticks)
    i = i + 1
    # making the script wait for 500 ms
    pygame.time.delay(500)
    # more accurate because it uses the processor

# creating a running loop
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()