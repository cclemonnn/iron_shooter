import random

from pygame.surface import Surface

import settings
from game_data import level_0
from level import Level
import pygame
from pygame.sprite import Sprite, Group

pygame.init()

# screen
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption('Iron Shooter')

# colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE_RED = (255, 69, 0)
ORANGE = (255, 165, 0)
SPRING_GREEN = (0, 255, 127)

# player actions
moving_right = False
moving_left = False

# FPS
clock = pygame.time.Clock()
FPS = 60

# game modes
running = True


class StartAnimation:
    def __init__(self):
        # check to see if start animation has ended
        self.run_start_animation = True
        # left background rect
        self.left_surface = Surface((settings.SCREEN_WIDTH / 2 + 10, settings.SCREEN_HEIGHT))
        self.left_rect = self.left_surface.get_rect()
        self.left_rect.topright = (1, 0)

        # right background rect
        self.right_surface = Surface((settings.SCREEN_WIDTH / 2 + 10, settings.SCREEN_HEIGHT))
        self.right_rect = self.right_surface.get_rect()
        self.right_rect.topleft = (settings.SCREEN_WIDTH - 1, 0)

        # iron man start image
        self.iron_man_start_image = pygame.image.load('images/iron_man/ironman_start_image.png').convert_alpha()
        self.iron_man_start_rect = self.iron_man_start_image.get_rect()
        self.iron_man_start_rect.midright = (-200, settings.SCREEN_HEIGHT / 2)

        # ultron start image
        self.ultron_start_image = pygame.image.load('images/ultron/ultron_start_image.png').convert_alpha()
        self.ultron_start_rect = self.ultron_start_image.get_rect()
        self.ultron_start_rect.midleft = (settings.SCREEN_WIDTH + 200, settings.SCREEN_HEIGHT / 2)

        # lightning
        lightning = pygame.image.load('images/start_images/start_lightning_cropped.png').convert_alpha()
        self.lightning_image = \
            pygame.transform.scale(lightning, (lightning.get_width() // 2, lightning.get_height() // 2))
        self.lightning_rect = self.lightning_image.get_rect()
        self.lightning_rect.center = (settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

        # instruction font
        self.font_bold = pygame.font.match_font('arial', bold=True)
        self.instruction_font = pygame.font.Font(self.font_bold, 40)
        self.instruction = self.instruction_font.render('Destroy All the Ultrons!', True, WHITE)
        self.instruction_rect = self.instruction.get_rect()
        self.instruction_rect.center = (settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT - 100)

        self.speed = 5
        self.reached_dest = False
        self.show_lightning = False

        # set time to make animation stop for a period when reached middle of the screen
        self.time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        # if rect hasnt reached middle of the screen
        if not self.reached_dest:
            self.left_rect.right += self.speed
            self.right_rect.left -= self.speed
            self.iron_man_start_rect.right += self.speed
            self.ultron_start_rect.left -= self.speed
        # if rect reached middle for a short period of time
        elif current_time > self.time + 4500:
            self.show_lightning = False
            self.left_rect.right -= self.speed
            self.right_rect.left += self.speed
            self.iron_man_start_rect.right -= self.speed
            self.ultron_start_rect.left += self.speed

        if self.left_rect.right >= settings.SCREEN_WIDTH / 2:
            self.reached_dest = True
            self.show_lightning = True

        # stops animation
        if self.left_rect.right <= 0:
            self.run_start_animation = False

    def draw(self):
        screen.blit(self.left_surface, self.left_rect)
        screen.blit(self.right_surface, self.right_rect)
        screen.blit(self.iron_man_start_image, self.iron_man_start_rect)
        screen.blit(self.ultron_start_image, self.ultron_start_rect)
        if self.show_lightning:
            # shows lightning
            screen.blit(self.lightning_image, self.lightning_rect)
            # shows instruction
            screen.blit(self.instruction, self.instruction_rect)


class EndAnimation:
    def __init__(self):
        # background
        self.background_surf = Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT + 10))
        self.background_rect = self.background_surf.get_rect()
        self.background_surf.fill(BLACK)
        self.background_rect.bottomleft = (0, 0)

        # ultron image
        self.end_image = pygame.image.load('images/ultron/ultron_end_image.png').convert_alpha()
        self.end_rect = self.end_image.get_rect()
        self.end_rect.center = (settings.SCREEN_WIDTH / 2, -settings.SCREEN_HEIGHT / 2)

        # restart font
        self.font_bold = pygame.font.match_font('arial', bold=True)
        self.restart_font = pygame.font.Font(self.font_bold, 25)
        self.restart = self.restart_font.render('Press \'1\' to restart the game', True, WHITE)
        self.restart_rect = self.restart.get_rect()
        self.restart_rect.bottomright = (settings.SCREEN_WIDTH - 20, settings.SCREEN_HEIGHT - 40)

        # ultron death message (excluded)
        # self.ultron_death_font = pygame.font.Font(self.font_bold, 40)
        # self.ultron_death_message = self.ultron_death_font.render('I WILL BE BACK, Iron Man!!!', True, RED)
        # self.ultron_death_message_rect = self.ultron_death_message.get_rect()
        # self.ultron_death_message_rect.topright = (settings.SCREEN_WIDTH - 100, 40)

        self.speed = 5
        self.reached_dest = False

    def update(self):
        if not self.reached_dest:
            self.background_rect.y += self.speed
            self.end_rect.y += self.speed

            if self.background_rect.bottom >= settings.SCREEN_HEIGHT:
                self.reached_dest = True

    def draw(self):
        screen.blit(self.background_surf, self.background_rect)
        screen.blit(self.end_image, self.end_rect)
        if self.reached_dest:
            screen.blit(self.restart, self.restart_rect)
            # the following message produce ultron death message. didnt like it so not gonna include it
            # screen.blit(self.ultron_death_message, self.ultron_death_message_rect)


class IronMan(Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        # static and shoot images
        for i in range(3):
            image = pygame.image.load(f'images/iron_man/{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() // 1.9, image.get_height() // 1.9))
            self.images.append(image)
        self.current_image = 0
        self.rect = self.images[self.current_image].get_rect()
        # starting position
        self.rect.x = 100
        self.rect.bottom = 300
        # death image
        death = pygame.image.load(f'images/iron_man/ironman_dead.png').convert_alpha()
        self.death_image = pygame.transform.scale(death, (death.get_width() // 1.9, death.get_height() // 1.9))
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

        # energy
        self.max_energy = 100
        self.energy = 100

        # flight
        self.flight_image = pygame.image.load('images/iron_man/flight_1.png').convert_alpha()
        self.flight_rect = self.flight_image.get_rect()

        # icon image
        icon = pygame.image.load('images/iron_man/ironman_icon.png').convert_alpha()
        self.icon_image = pygame.transform.scale(icon, (icon.get_width() // 1.7, icon.get_height() // 1.7))
        self.icon_rect = self.icon_image.get_rect()
        self.icon_rect.topleft = (0, 0)

        # energy image
        energy = pygame.image.load('images/iron_man/energy.png').convert_alpha()
        self.energy_image = pygame.transform.scale(energy, (energy.get_width() // 1.7, energy.get_height() // 1.7))
        self.energy_rect = self.energy_image.get_rect()
        self.energy_rect.y = 60
        self.energy_rect.right = self.icon_rect.right

    def move(self, ul_group):
        if self.alive:
            if moving_right:
                self.flip = False
                if self.rect.x >= 100 \
                        and settings.WORLD_WIDTH - (settings.SCREEN_WIDTH + self.rect.width) > self.total_movement >= 0:
                    # scrolls world to left
                    level.update(- self.speed)
                    # scrolls all ultrons
                    for ul in ul_group:
                        ul.rect.x -= self.speed
                    self.total_movement += self.speed
                    # scrolls ultron laser
                    for laser in ultron_laser_group:
                        laser.rect.x -= self.speed
                # world reaches right side end, moves iron man only
                elif self.rect.right < settings.SCREEN_WIDTH - 100:
                    self.rect.x += self.speed

            if moving_left:
                self.flip = True
                if self.total_movement > 0:
                    self.total_movement -= player.speed
                    # scrolls world to right
                    level.update(self.speed)
                    # scrolls all ultrons
                    for ul in ul_group:
                        ul.rect.x += self.speed
                    # scrolls ultron laser
                    for laser in ultron_laser_group:
                        laser.rect.x += self.speed
                # world reaches left side end, moves iron man only
                elif self.rect.x > 0:
                    # self.total_movement -= player.speed
                    self.rect.x -= self.speed

            if self.jump and self.energy > 0:
                self.energy -= 1
                if self.rect.top > 5:
                    self.rect.y -= 5
                    self.on_ground = False

            # iron man falls if in air
            elif not self.on_ground and self.rect.bottom < settings.SCREEN_HEIGHT - 7:
                self.rect.bottom += 7

            if self.on_ground and self.energy < self.max_energy:
                self.energy += 2

    def draw(self):
        if not self.alive:
            self.image = self.death_image
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        elif not self.shoot:
            screen.blit(pygame.transform.flip(self.images[0], self.flip, False), self.rect)
        else:
            self.current_image += 0.15
            if 9 > self.current_image > 2:
                screen.blit(pygame.transform.flip(self.images[2], self.flip, False), self.rect)
                iron_man_laser.shoot(self)
            elif self.current_image >= 9:
                self.current_image = 0
                self.shoot = False
            else:
                screen.blit(pygame.transform.flip(self.images[int(self.current_image)], self.flip, False), self.rect)

    def draw_flight(self):
        if self.alive and self.jump and player.energy > 0:
            self.flight_rect.midtop = (self.rect.centerx, self.rect.bottom + 10)
            screen.blit(self.flight_image, self.flight_rect)

    def draw_health_bar(self):
        # draw health box boarder
        pygame.draw.rect(screen, BLACK, (58, 15, 204, 19))
        # draw max health
        pygame.draw.rect(screen, RED, (60, 17, 200, 15))
        # draw actual health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, SPRING_GREEN, (60, 17, 200 * ratio, 15))

    def draw_icon(self):
        screen.blit(self.icon_image, self.icon_rect)

    def draw_energy_bar(self):
        # draw energy box boarder
        pygame.draw.rect(screen, BLACK, (58, 63, 104, 14))
        # draw max energy
        pygame.draw.rect(screen, RED, (60, 65, 100, 10))
        # draw actual energy
        ratio = self.energy / self.max_energy
        pygame.draw.rect(screen, ORANGE, (60, 65, 100 * ratio, 10))

    def draw_energy_icon(self):
        screen.blit(self.energy_image, self.energy_rect)

    def check_alive(self):
        if self.health <= 0:
            self.alive = False


class IronManLaser(Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load(f'images/iron_man/3.png').convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() // 1.9, image.get_height() // 1.9))
        self.rect = self.image.get_rect()

    def shoot(self, iron_man):
        if not iron_man.flip:
            self.rect.left = iron_man.rect.right + 40
            self.rect.y = iron_man.rect.y + 5
        else:
            self.rect.right = iron_man.rect.left + 10
            self.rect.y = iron_man.rect.y + 5
        screen.blit(pygame.transform.flip(self.image, iron_man.flip, False), self.rect)
        # player.energy -= 1 (could let shooting cost energy if added this code)
        # check collisions with ultron
        ultron_shot = pygame.sprite.spritecollide(iron_man_laser, ultron_group, False)
        for ul in ultron_shot:
            if ul.alive:
                ul.current_health -= 1
                if ul.current_health <= 0:
                    ul.alive = False
        # removes ultron laser if collided with iron man laser
        pygame.sprite.spritecollide(iron_man_laser, ultron_laser_group, True)


class Ground(Sprite):
    # sky background
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/sky/sky_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -1500
        self.rect.y = -2700

    def update(self, movement):
        # this method scrolls the background (not called)
        self.rect.x += movement

    def draw(self):
        screen.blit(self.image, self.rect)


class Ultron(Sprite):
    def __init__(self, x, bottom):
        super().__init__()
        # death images
        self.death_images = []
        self.current_death_image = 0
        for i in range(6):
            image = pygame.image.load(f'images/ultron_death/{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() // 1.5, image.get_height() // 1.5))
            self.death_images.append(image)
        # shoot image
        self.shoot_image = []
        self.current_shoot_image = 0
        for i in range(3):
            image = pygame.image.load(f'images/ultron/{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() // 1.5, image.get_height() // 1.5))
            self.shoot_image.append(image)
        # static image
        # image = pygame.image.load(f'images/ultron/0.png').convert_alpha()
        self.image = self.shoot_image[0]
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

        # vision
        self.vision_surf = Surface((settings.SCREEN_WIDTH // 2.3, 10))
        self.vision_surf.fill(RED)
        self.vision_rect = self.vision_surf.get_rect()
        self.shoot = False

        # time used to restrict shooting frequency
        self.time = pygame.time.get_ticks()
        self.can_shoot = True

    def update(self):
        # time used to restrict shooting frequency
        current_time = pygame.time.get_ticks()
        if current_time > self.time + 800:
            self.time = current_time
            self.can_shoot = True

        # if alive and iron man not in vision
        if self.alive and not self.shoot:
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
        # if dead
        elif not self.alive:
            self.current_death_image += 0.15
            if self.current_death_image < 5:
                self.image = self.death_images[int(self.current_death_image)]
            else:
                self.image = self.death_images[5]
                self.rect.bottom = self.bottom + 80
        # if alive and iron man in vision
        elif self.alive and self.shoot:
            self.current_shoot_image += 0.1
            if self.current_shoot_image < 2 and self.can_shoot:
                self.image = self.shoot_image[int(self.current_shoot_image)]
            elif 2 <= self.current_shoot_image < 3:  # and self.can_shoot:
                self.image = self.shoot_image[int(self.current_shoot_image)]
                # ultron_laser_group.add(UltronLaser(self))
                # self.can_shoot = False
            else:
                self.current_shoot_image = 0
                # self.can_shoot = True
                self.image = self.shoot_image[int(self.current_shoot_image)]
                self.shoot = False
                self.can_shoot = False
            if 2 <= self.current_shoot_image < 3 and self.can_shoot:
                # shoot
                ultron_laser_group.add(UltronLaser(self))
                self.can_shoot = False

            self.health_bar.show_health_bar(self.rect.left, self.rect.top, self.rect.width, self.current_health)
            # ultron_laser_group.add(UltronLaser(self))

    def check_vision(self, iron_man):
        # position the vision rect
        if not self.flip:
            self.vision_rect.midleft = self.rect.midright
        else:  # facing left
            self.vision_rect.midright = self.rect.midleft
        # check if player in ultron's vision
        if self.vision_rect.colliderect(iron_man.rect):
            self.shoot = True

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # the following line shows the vision
        # screen.blit(self.vision_surf, self.vision_rect)


class UltronLaser(Sprite):
    def __init__(self, ultron):
        super().__init__()
        image = pygame.image.load('images/ultron_laser/lightsaber_green.png').convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() // 4, image.get_height() // 4))
        self.rect = self.image.get_rect()
        self.speed = 7
        if not ultron.flip:
            self.right = True
            self.rect.left = ultron.rect.right
            self.rect.y = ultron.rect.centery - 50
        else:
            self.right = False
            self.rect.right = ultron.rect.left
            self.rect.y = ultron.rect.centery - 50

    def update(self, iron_man):
        if self.right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.left >= settings.SCREEN_WIDTH or self.rect.right < 0:
            self.kill()
        # check collision with iron man reduce health if hit
        if iron_man.alive and self.rect.colliderect(iron_man.rect):
            self.kill()
            iron_man.health -= 10


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


class UltronIcon(Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('images/ultron/ultron_icon.png').convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() // 1.5, image.get_height() // 1.5))
        self.rect = self.image.get_rect()
        self.rect.topright = (settings.SCREEN_WIDTH - 60, 20)

        # font for number of ultrons alive
        self.font_bold = pygame.font.match_font('arial', bold=True)
        self.font = pygame.font.Font(self.font_bold, 20)
        self.ultron_count = 0
        self.ultron_number = self.font.render(f'X {self.ultron_count}', False, BLACK)
        self.ultron_number_rect = self.ultron_number.get_rect()
        self.ultron_number_rect.topleft = (settings.SCREEN_WIDTH - 50, 30)

        # check if all ultron dead
        self.diaplay_end_animation = False

    def update(self, ultron_group):
        self.ultron_count = 0
        for ul in ultron_group:
            if ul.alive:
                self.ultron_count += 1
        self.ultron_number = self.font.render(f'X {self.ultron_count}', True, BLACK)
        if self.ultron_count == 0:
            self.diaplay_end_animation = True

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.ultron_number, self.ultron_number_rect)



def initialize_movable_components():
    global player, ultron_group, level, start_animation, end_animation, ultron_icon
    # levels
    level = Level(level_0, screen)
    # start animation
    start_animation = StartAnimation()

    # end animation
    end_animation = EndAnimation()

    # ultron icon
    ultron_icon = UltronIcon()

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


initialize_movable_components()

iron_man_laser = IronManLaser()

# sky background
ground = Ground()

ultron_laser_group = Group()

# game loop
while running:
    clock.tick(FPS)
    screen.fill(GREEN)
    ground.draw()
    level.draw()
    player.draw_health_bar()
    player.draw_energy_bar()
    player.draw_icon()
    player.draw_energy_icon()
    player.check_alive()
    player.move(ultron_group)
    player.draw_flight()
    level.check_collisions(player)
    ultron_group.update()
    for ul in ultron_group:
        ul.check_vision(player)
        ul.draw()
    ultron_laser_group.update(player)
    ultron_laser_group.draw(screen)
    ultron_icon.update(ultron_group)
    ultron_icon.draw()
    player.draw()

    # run start animation
    if start_animation.run_start_animation:
        start_animation.update()
        start_animation.draw()

    # run end animation
    if ultron_icon.diaplay_end_animation or not player.alive:
        end_animation.update()
        end_animation.draw()

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard down
        if player.alive and not start_animation.run_start_animation:
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
                # if all ultron dead
                if end_animation.reached_dest and event.key == pygame.K_1:
                    # if player pressed '1', restart game
                    initialize_movable_components()

        else:
            # if iron man dead
            if event.type == pygame.KEYUP:
                if end_animation.reached_dest and event.key == pygame.K_1:
                    # if player pressed '1', restart game
                    initialize_movable_components()

    pygame.display.update()

pygame.quit()
