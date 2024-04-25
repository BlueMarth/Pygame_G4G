import pygame
pygame.init()

# create window, get size, close window
screen = pygame.display.set_mode()
x, y = screen.get_size()
pygame.display.quit()

# create new resizable window with half the screen sizes
w = int(x/2)
h = int(y/2)
screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

# set colour
colour = (144, 164, 174)
screen.fill(colour)

# update window
pygame.display.flip()

#set title & icon
pygame.display.set_caption('G4G')
icon = pygame.image.load('visual/github_icon.png')
pygame.display.set_icon(icon)

# main loop
while True:

    # update window display
    pygame.display.update()

    # close window button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.quit()