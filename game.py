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

# player actions
moving_right = False
moving_left = False

# FPS
clock = pygame.time.Clock()
FPS = 60

# game modes
running = True


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/iron_man/0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 300
        self.speed = 5
        self.flip = False

    def move(self):
        if moving_right:
            self.flip = False
            self.rect.x += self.speed
        if moving_left:
            self.flip = True
            self.rect.x -= self.speed

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Player()

# game loop
while running:
    clock.tick(FPS)
    screen.fill(GREEN)
    player.move()
    player.draw()

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_a:
                moving_left = True

        # keyboard up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_a:
                moving_left = False

    pygame.display.update()

pygame.quit()
