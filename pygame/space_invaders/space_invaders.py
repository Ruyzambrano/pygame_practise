import pygame
import random
import math
from time import sleep

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('freesansbold', 100)
score_font = pygame.font.SysFont('freesansbold', 50)

from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Define the window size
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

# Define the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('pygame\space_invaders\images\player.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.bottom = screen_height-10
        self.rect.right = screen_width/2
        self.cooldown = 750
        self.last_shot_time = 0
        self.strength = 1
    
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            self.shoot()
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.cooldown:
            # Shoot and update last shot time
            height = self.rect.y
            width = self.rect.x
            new_bullet = Bullet(width, height, -1, "pygame\space_invaders\images\laserBlue04.png", self.strength)
            player_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            self.last_shot_time = current_time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, up_down, image_path, strength):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load(image_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=((width + 30), height))
        self.direction = up_down
        self.surf = pygame.transform.scale(self.surf,
                                           (int(self.rect.width * 0.5),
                                            int(self.rect.height * 0.5)))
        self.strength = strength

    def update(self):
        self.rect.move_ip(0, 10*self.direction)
        if self.rect.top == 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, enemy_colour):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(image_path).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.type = enemy_colour

    def update(self, direction, speed):
        self.rect.move_ip(direction * speed, 0)
        
        if self.rect.left < 0 or self.rect.right > screen_width:
            direction *= -1  # Reverse the horizontal direction
            for enemy in enemies:
                enemy.rect.move_ip(0, 20)

        if self.rect.left < 0:
            self.rect.left = 0  # Keep the enemy within the left edge

        if self.rect.right > screen_width:
            self.rect.right = screen_width  # Keep the enemy within the right edge
        
        return direction
    
    def shoot(self):
        height = self.rect.y + 5
        width = self.rect.x - 13
        new_bullet = Bullet(width, height, 1,
                            r"pygame\space_invaders\images\laserRed04.png",
                            strength=1)
        enemy_bullets.add(new_bullet)
        all_sprites.add(new_bullet)

class RedAlien(Enemy):
    def __init__(self, colour):
        super().__init__(r'pygame\space_invaders\images\red.png', colour)
        self.health = 1
        self.worth = 1

class GreenAlien(Enemy):
    def __init__(self, colour):
        super().__init__(r'pygame\space_invaders\images\green.png', colour)
        self.health = 4
        self.worth = 2

class YellowAlien(Enemy):
    def __init__(self, colour):
        super().__init__(r'pygame\space_invaders\images\yellow.png', colour)
        self.health = 6
        self.worth = 4

class Level():
    def __init__(self):
        self.round = 0
        self.speed = 0.8
        self.number_enemies = 8
        self.enemy_pool = ['red']

    def next_level(self):
        self.round += 1
        self.speed *= 1.25
        self.number_enemies = math.ceil(self.number_enemies * 1.25)
        if level.round == 2:
            self.enemy_pool.append('green')
        if level.round == 3:
            self.enemy_pool.append('yellow')

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super(Shield, self).__init__()
        self.surf = pygame.image.load('pygame\space_invaders\images\extra.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.top = 500
        self.health = 5

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, image_path, width, height):
        super(PowerUp, self).__init__()
        self.type = power_up_type
        self.surf = pygame.image.load(image_path).convert()
        self.rect = self.surf.get_rect(center=(width, height))
        self.surf = pygame.transform.scale(self.surf,
                                           (int(self.rect.width * 0.5),
                                            int(self.rect.height * 0.5)))

    def update(self):
        # Implement the behavior of the power-up here
        self.rect.move_ip(0, 1)

        # Remove the power-up when it goes off-screen
        if self.rect.top < 0:
            self.kill()

class FirePowerUp(PowerUp):
    def __init__(self, width, height):
        super().__init__('strength_up',
                         r'pygame\space_invaders\images\powerupRed_star.png',
                         width, height)

class FireSpeedUp(PowerUp):
    def __init__(self, width, height):
        super().__init__('speed_up', r'pygame\space_invaders\images\powerupGreen_bolt.png',
                         width, height)

class ExtraShield(PowerUp):
    def __init__(self, width, height):
        super().__init__('extra_shield', r'pygame\space_invaders\images\powerupBlue_shield.png',
                          width, height)

# Create the player
player = Player()

# Make groups to render sprites
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
shields = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

direction = 1

level = Level()

shield_left = Shield()
shield_left.rect.x = 150
shields.add(shield_left)
all_sprites.add(shield_left)

shield_middle_left = Shield()
shield_middle_left.rect.x = 300
shields.add(shield_middle_left)
all_sprites.add(shield_middle_left)

shield_middle_right = Shield()
shield_middle_right.rect.x = 450
shields.add(shield_middle_right)
all_sprites.add(shield_middle_right)

shield_right = Shield()
shield_right.rect.x = 600
shields.add(shield_right)
all_sprites.add(shield_right)

ENEMYSHOT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYSHOT, random.randint(2000, 6000))

add_enemy = True

time_since_start = pygame.time.get_ticks()

running = True
strength_active = False
strength_cooldown = -60000
speed_active = False
speed_cooldown = -60000
lose = False

game_over_time = None

red_kills = 0
green_kills = 0
yellow_kills = 0

score = 0

while running:
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:
                player.shoot()

        if event.type == ENEMYSHOT:
            if not lose:
                enemies.sprites()[random.randint(0, len(enemies) - 1)].shoot()

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    if not lose:
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        for bullet in player_bullets:
            bullet.update()

        for bullet in enemy_bullets:
            bullet.update()

        current_time = pygame.time.get_ticks()
        
        if strength_active == True and (current_time - strength_cooldown) > 60000:
            player.strength -=3
            strength_active = False

        if speed_active == True and (current_time - speed_cooldown) > 60000:
            player.cooldown *= 2
            speed_active = False

        for powerup in powerups:
            powerup.update()
            if pygame.sprite.collide_rect(powerup, player):
                if powerup.type == 'strength_up':
                    if strength_active == False:
                        strength_cooldown = current_time
                        strength_active = True
                        player.strength += 3
                elif powerup.type == 'speed_up':
                    if speed_active == False:
                        speed_cooldown = current_time
                        speed_active = True
                        player.cooldown /= 2
                elif powerup.type == 'extra_shield':
                    pass
                powerup.kill()

        for enemy in enemies:
            direction = enemy.update(direction, level.speed)
            if pygame.sprite.collide_rect(enemy, player):
                lose = True

            for bullet in enemy_bullets:
                if pygame.sprite.collide_rect(bullet, player):
                    lose = True
                for shield in shields:
                    if pygame.sprite.collide_rect(bullet, shield):
                        shield.health -= bullet.strength
                        bullet.kill()
                        if shield.health < 1:
                            shield.kill()

            for bullet in player_bullets:
                if pygame.sprite.collide_rect(enemy, bullet):
                    enemy.health -= bullet.strength
                    if enemy.health < 1:
                        if enemy.type == 'red':
                            red_kills += 1
                        elif enemy.type == 'green':
                            green_kills += 1
                        elif enemy.type == 'yellow':
                            yellow_kills += 1
                        if red_kills > 4:
                            new_power_up = FireSpeedUp(enemy.rect.x, enemy.rect.y)
                            powerups.add(new_power_up)
                            all_sprites.add(new_power_up)
                            red_kills = 0
                        if green_kills > 4:
                            new_power_up = FirePowerUp(enemy.rect.x, enemy.rect.y)
                            powerups.add(new_power_up)
                            all_sprites.add(new_power_up)
                            green_kills = 0
                        if yellow_kills > 4:
                            new_power_up = ExtraShield(enemy.rect.x, enemy.rect.y)
                            powerups.add(new_power_up)
                            all_sprites.add(new_power_up)
                            yellow_kills = 0
                        score += enemy.worth
                        enemy.kill()
                    bullet.kill()
                for shield in shields:
                    if pygame.sprite.collide_rect(bullet, shield):
                        shield.health -= 1
                        bullet.kill()
                        if shield.health == 0:
                            shield.kill()

        if len(enemies) == 0:
            level.next_level()
            enemies.empty()
            add_enemy = True
            time_since_start = pygame.time.get_ticks()

        if add_enemy:
            enemies_to_place = level.number_enemies
            height = 50

            for row in range(math.ceil(level.number_enemies/10)):
                while enemies_to_place >= 10:
                    width = 66
                    for num in range(10):
                        enemy_choice = level.enemy_pool.copy()
                        enemy_type = random.choice(enemy_choice)
                        if enemy_type == 'red':
                            new_enemy = RedAlien(enemy_type)
                        elif enemy_type == 'green':
                            new_enemy = GreenAlien(enemy_type)
                        elif enemy_type == 'yellow':
                            new_enemy = YellowAlien(enemy_type)
                        new_enemy.rect.x = width
                        new_enemy.rect.y = height
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        width += 66
                    height -= 50
                    enemies_to_place -= 10
                if enemies_to_place > 0:
                    divide = (round((screen_width - 150)/enemies_to_place))
                    width = divide
                    while enemies_to_place > 0:
                        enemies_to_place -= 1
                        enemy_choice = level.enemy_pool.copy()
                        enemy_type = random.choice(enemy_choice)
                        if enemy_type == 'red':
                            new_enemy = RedAlien(enemy_type)
                        elif enemy_type == 'green':
                            new_enemy = GreenAlien(enemy_type)
                        elif enemy_type == 'yellow':
                            new_enemy = YellowAlien(enemy_type)

                        new_enemy.rect.x = width
                        new_enemy.rect.y = height
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        width += divide

            add_enemy = False

    screen.fill((0, 0, 0))  # Clear the screen

    if lose:
        if game_over_time is None:
            game_over_time = pygame.time.get_ticks()  # Store the time when game over occurred

        if pygame.time.get_ticks() - game_over_time < 5000:
            game_over_text = font.render(f'GAME OVER', True, (220, 20, 60), (0, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 200))
        else:
            running = False

    if (pygame.time.get_ticks() - time_since_start) <  5000:
        level_round = level.round
        level_text = font.render(f'LEVEL {level_round}', True, (255, 255, 255))
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, 200))

    score_text = score_font.render(f'{score}', True, (225, 225, 225), (0, 0, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() * 2,
                             score_text.get_height() // 2))
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()

    clock.tick(40)

pygame.quit()
