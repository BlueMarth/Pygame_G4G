import pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

display_screen = pygame.display.set_mode((500,500))
base_font = pygame.font.Font(None, 40)

user_text = ''

input_rect = pygame.Rect(200,200,140,32)
color_active = "springgreen"
color_passive = "springgreen4"
color = color_passive

active = False

ON_TEXT = pygame.USEREVENT + 1

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == ON_TEXT:
            active = True
        else:
            active = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    if input_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.event.post(pygame.event.Event(ON_TEXT))

    display_screen.fill("gray4")

    if active:
        color = color_active
    else:
        color = color_passive

    pygame.draw.rect(display_screen, color, input_rect)

    text_surface = base_font.render(user_text, True, "black")
    display_screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)
    pygame.display.flip()
    clock.tick(fps)