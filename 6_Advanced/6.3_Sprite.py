import pygame

COLOR_KEY = "red"
SCREEN_COLOR = "darkslategray"
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(SCREEN_COLOR)
        self.image.set_colorkey(COLOR_KEY)

        pygame.draw.rect(self.image,COLOR_KEY,
                         pygame.Rect(0, 0, width, height))
        
        self.rect = self.image.get_rect()


pygame.init()

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creatiing Sprite")

all_sprites_list = pygame.sprite.Group()

object_ = Sprite("red", )