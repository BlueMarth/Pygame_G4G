import pygame
import time
pygame.init()

display_screen = pygame.display.set_mode((500, 500))

text = "Welcome!"

font = pygame.font.SysFont(None, 40)
font_color = "wheat"

img = font.render(text, True, font_color)
rect = img.get_rect()
rect.topleft = (20, 20)
cursor = pygame.Rect(rect.topright, (3, rect.height))

run = True

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(text) > 0:
                    # stores the text exceot the last character
                    text = text[:-1]
                    
            else:
                text += event.unicode

            img = font.render(text, True, font_color)
            rect.size = img.get_size()
            cursor.topleft = rect.topright

    display_screen.fill("gray15")
    display_screen.blit(img, rect)

    # cursor made to blink after every 0.5 second
    if time.time() % 1 > 0.5:
        pygame.draw.rect(display_screen, font_color, cursor)

    pygame.display.update()

pygame.quit()