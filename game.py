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

# gravity
GRAVITY = 0.75

# game modes
running = True


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/iron_man/0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.bottom = 500
        self.speed = 5
        self.flip = False
        self.alive = True
        self.jump = False
        self.in_air = False
        self.dy = 0

    def move(self):
        if self.alive:
            if moving_right:
                self.flip = False
                self.rect.x += self.speed
            if moving_left:
                self.flip = True
                self.rect.x -= self.speed
            if self.jump:
                if self.rect.top > 5:
                    self.rect.y -= 5
            else:
                self.rect.bottom += 3
            if self.rect.bottom > 500:
                self.rect.bottom = 500

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Ultron(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/ultron/0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.flip = False

    def draw(self):
        screen.blit(self.image, self.rect)


player = Player()
ultron = Ultron(200, 200)

# game loop
while running:
    clock.tick(FPS)
    screen.fill(GREEN)
    pygame.draw.line(screen, (0, 0, 0), (0, 500), (WIDTH, 500))
    player.move()
    ultron.draw()
    player.draw()

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d: # moving right
                moving_right = True
            elif event.key == pygame.K_a: # moving left
                moving_left = True
            if event.key == pygame.K_w:
                player.jump = True

        # keyboard up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_w:
                player.jump = False

    pygame.display.update()

pygame.quit()
