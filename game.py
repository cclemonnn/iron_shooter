import random
import settings
from game_data import level_0
from level import Level
import pygame
from pygame.sprite import Sprite, Group

pygame.init()

# screen
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption('Iron Shooter')

# levels
level = Level(level_0, screen)

# colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE_RED = (255, 69, 0)

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


class IronMan(Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(3):
            image = pygame.image.load(f'images/iron_man/{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() // 1.9, image.get_height() // 1.9))
            self.images.append(image)
        self.current_image = 0
        self.rect = self.images[self.current_image].get_rect()
        # starting position
        self.rect.x = 100
        self.rect.bottom = 300
        # move speed
        self.speed = 5
        self.flip = False
        self.alive = True
        self.jump = False
        self.on_ground = True
        self.shoot = False
        # restrict movement
        self.total_movement = 0
        # health
        self.max_health = 100
        self.health = 100

    def move(self, ul_group):
        if self.alive:
            if moving_right:
                self.flip = False
                if self.rect.x >= 100 \
                        and settings.WORLD_WIDTH - (settings.SCREEN_WIDTH + self.rect.width) > self.total_movement >= 0:
                    # shift world to left
                    level.update(- self.speed)
                    # shift all ultrons
                    for ul in ul_group:
                        ul.rect.x -= self.speed
                    self.total_movement += self.speed
                # world reaches right side end, moves iron man only
                elif self.rect.right < settings.SCREEN_WIDTH - 100:
                    self.rect.x += self.speed

            if moving_left:
                self.flip = True
                if self.total_movement > 0:
                    self.total_movement -= player.speed
                    # shift world to right
                    level.update(self.speed)
                    # shift all ultrons
                    for ul in ul_group:
                        ul.rect.x += self.speed
                # world reaches left side end, moves iron man only
                elif self.rect.x > 0:
                    # self.total_movement -= player.speed
                    self.rect.x -= self.speed

            if self.jump:
                if self.rect.top > 5:
                    self.rect.y -= 5
                    self.on_ground = False

            elif not self.on_ground:
                self.rect.bottom += 7


    def draw(self):
        if not self.shoot:
            screen.blit(pygame.transform.flip(self.images[0], self.flip, False), self.rect)
        else:
            self.current_image += 0.15
            if 9 > self.current_image > 2:
                screen.blit(pygame.transform.flip(self.images[2], self.flip, False), self.rect)
                laser.shoot()
            elif self.current_image >= 9:
                self.current_image = 0
                self.shoot = False
            else:
                screen.blit(pygame.transform.flip(self.images[int(self.current_image)], self.flip, False), self.rect)

    def draw_health_bar(self):
        # draw health box boarder
        pygame.draw.rect(screen, BLACK, (8, 18, 204, 14))
        # draw max health
        pygame.draw.rect(screen, RED, (10, 20, 200, 10))
        # draw actual health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, ORANGE_RED, (10, 20, 200 * ratio, 10))


class Laser(Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load(f'images/iron_man/3.png').convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() // 1.9, image.get_height() // 1.9))
        self.rect = self.image.get_rect()

    def shoot(self):
        if not player.flip:
            self.rect.left = player.rect.right + 40
            self.rect.y = player.rect.y + 5
        else:
            self.rect.right = player.rect.left + 10
            self.rect.y = player.rect.y + 5
        screen.blit(pygame.transform.flip(self.image, player.flip, False), self.rect)

        # check collisions with ultron
        ultron_shot = pygame.sprite.spritecollide(laser, ultron_group, False)
        for ul in ultron_shot:
            if ul.alive:
                ul.current_health -= 1
                if ul.current_health <= 0:
                    ul.alive = False


class Ultron(Sprite):
    def __init__(self, x, bottom):
        super().__init__()
        self.death_images = []
        self.current_death_image = 0
        for i in range(6):
            image = pygame.image.load(f'images/ultron_death/{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() // 1.5, image.get_height() // 1.5))
            self.death_images.append(image)
        image = pygame.image.load('images/ultron/0.png').convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() // 1.5, image.get_height() // 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.bottom = bottom
        self.rect.bottom = self.bottom
        self.speed = 5
        self.flip = False
        # health
        self.max_health = 100
        self.current_health = 100
        self.health_bar = UltronHealth(self.max_health)
        self.alive = True
        # movement
        self.delta_move = 0
        self.moving_right = True
        self.moving_left = False
        self.max_movement = random.randint(100, 250)

    def update(self):
        if self.alive:
            if self.moving_right and self.delta_move <= self.max_movement:
                self.delta_move += 3
                self.rect.x += 3
            elif self.moving_right and self.delta_move > self.max_movement:
                self.moving_right = False
                self.moving_left = True
                self.delta_move = 0
                self.flip = True
            if self.moving_left and self.delta_move <= self.max_movement:
                self.delta_move += 3
                self.rect.x -= 3
            elif self.moving_left and self.delta_move > self.max_movement:
                self.moving_right = True
                self.moving_left = False
                self.delta_move = 0
                self.flip = False
            self.health_bar.show_health_bar(self.rect.left, self.rect.top, self.rect.width, self.current_health)
        else:
            self.current_death_image += 0.15
            if self.current_death_image < 5:
                self.image = self.death_images[int(self.current_death_image)]
            else:
                self.image = self.death_images[5]
                self.rect.bottom = self.bottom + 80

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class UltronHealth:
    def __init__(self, max_health):
        self.max_health = max_health

    def show_health_bar(self, left, top, width, health):
        # draw health box boarder
        pygame.draw.rect(screen, BLACK, (left - 2, top - 22, width + 4, 14))
        # draw max health
        pygame.draw.rect(screen, RED, (left, top - 20, width, 10))
        # draw actual health
        ratio = health / self.max_health
        pygame.draw.rect(screen, BLUE, (left, top - 20, width * ratio, 10))


laser = Laser()
player = IronMan()
# x = tile size * tile position, y = tile size * tile position + 1
ultron_0 = Ultron(settings.TILE_SIZE * 11 + 30, settings.TILE_SIZE * 5)
ultron_1 = Ultron(settings.TILE_SIZE * 11 + 30, settings.TILE_SIZE * 10)
ultron_2 = Ultron(settings.TILE_SIZE * 44 + 30, settings.TILE_SIZE * 3)
ultron_3 = Ultron(settings.TILE_SIZE * 40 + 30, settings.TILE_SIZE * 6)


ultron_group = Group()
ultron_group.add(ultron_0)
ultron_group.add(ultron_1)
ultron_group.add(ultron_2)
ultron_group.add(ultron_3)



# game loop
while running:
    clock.tick(FPS)
    screen.fill(GREEN)
    level.draw()
    player.draw_health_bar()
    player.move(ultron_group)
    level.check_collisions(player)
    ultron_group.update()
    for ul in ultron_group:
        ul.draw()
    player.draw()

    # check collisions btw laser and ultron

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:  # moving right
                moving_right = True
            elif event.key == pygame.K_a:  # moving left
                moving_left = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_SPACE:
                player.shoot = True

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
