import pygame

pygame.init()

# create window, get size, close window
screen = pygame.display.set_mode()
x, y = screen.get_size()
pygame.display.quit()

# create new resizable window with half the screen sizes
screen = pygame.display.set_mode((int(x/2), int(y/2)), pygame.RESIZABLE)

# set colour
colour = (144, 164, 174)
screen.fill(colour)
pygame.display.flip()

#set title & icon
pygame.display.set_caption('G4G')
icon = pygame.image.load('github_icon.png')
pygame.display.set_icon(icon)

# main loop
while True:






    # close window button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()