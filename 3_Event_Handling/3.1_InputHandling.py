import pygame
pygame.init()

gameWindow = pygame.display.set_mode((512,384))
pygame.display.set_caption("Input Handling")
icon = pygame.image.load("visual/github_icon.png")
pygame.display.set_icon(icon)

exit_game = False
game_over = False

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        
        # keyboard interrupts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("Key pressed: Right arrow key")
            elif event.key == pygame.K_LEFT:
                print("Key pressed: Left arrow key")
            elif event.key == pygame.K_UP:
                print("Key pressed: Up arrow key")
            elif event.key == pygame.K_DOWN:
                print("Key pressed: Down arrow key")
        
        # mouse interrupts
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEMOTION:
            if event.rel[0] > 0:
                print("Mouse moving to the right")
            elif event.rel[0] < 0:
                print("Mouse moving to the left")
            elif event.rel[1] > 0:
                print("Mouse moving down")
            elif event.rel[1] < 0:
                print("Mouse moving up")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("LMB pressed")
            elif event.button == 2:
                print("MMB pressed")
            elif event.button == 3:
                print("RMB pressed")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                print("LMB released")
            elif event.button == 2:
                print("MMB released")
            elif event.button == 3:
                print("RMB released")
pygame.quit()
quit()