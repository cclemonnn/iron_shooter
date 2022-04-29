import pygame
from pygame.sprite import Sprite

pygame.init()

# screen
WIDTH = 1024
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('mario shooter')

# colors
GREEN = (0, 255, 0)

# game modes
running = True


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/iron_man/0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self):
        screen.blit(self.image, self.rect)


# game loop
while running:
    screen.fill(GREEN)
    Player().draw()
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()