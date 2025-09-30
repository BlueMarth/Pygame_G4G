import pygame

SCREEN_COLOR = "darkslategray"
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
fps = 60


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(SCREEN_COLOR)
        
        pygame.draw.rect(self.image,color,
                         pygame.Rect(0, 0, width, height))
        
        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels
    
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    
    def moveForth(self, speed):
        self.rect.y -= speed * speed / 10
    
    def moveBack(self, speed):
        self.rect.y += speed * speed / 10

pygame.init()

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creatiing Sprite")

all_sprites_list = pygame.sprite.Group()

car = Sprite("white", 20, 30)
car.rect.x = 200
car.rect.y = 300

all_sprites_list.add(car)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        car.moveLeft(10)
    if keys[pygame.K_d]:
        car.moveRight(10)
    if keys[pygame.K_s]:
        car.moveBack(10)
    if keys[pygame.K_w]:
        car.moveForth(10)

    all_sprites_list.update()
    screen.fill(SCREEN_COLOR)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(fps)