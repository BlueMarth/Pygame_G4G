import pygame
pygame.init()

COLOR = "red"
SCREEN_COLOR = "darkslategray"
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(SCREEN_COLOR)
        self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image,color,
                         pygame.Rect(0, 0, width, height))
        
        self.rect = self.image.get_rect()


size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creatiing Sprite")

all_sprites_list = pygame.sprite.Group()

object_ = Sprite("red", 20, 30)
object_.rect.x = 200
object_.rect.y = 300

all_sprites_list.add(object_)

exit = True
clock = pygame.time.Clock()

while exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False
    all_sprites_list.update()
    screen.fill(SCREEN_COLOR)
    all_sprites_list(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()