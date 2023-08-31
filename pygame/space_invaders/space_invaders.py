import pygame
import random
import math
from time import sleep

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('freesansbold', 100)

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
        self.surf = pygame.image.load('space_invaders\images\player.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.bottom = screen_height-10
        self.rect.right = screen_width/2
        self.cooldown = 750
        self.last_shot_time = 0
    
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
            new_bullet = Bullet(width, height, -1)
            player_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            self.last_shot_time = current_time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, up_down):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 15))  
        self.surf.fill((255, 255, 255))  
        self.rect = self.surf.get_rect(center=((width + 30), height))
        self.direction = up_down

    def update(self):
        self.rect.move_ip(0, 10*self.direction)
        if self.rect.top == 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(image_path).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

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
        new_bullet = Bullet(width, height, 1)
        enemy_bullets.add(new_bullet)
        all_sprites.add(new_bullet)

class RedAlien(Enemy):
    def __init__(self):
        super().__init__(r'space_invaders\images\red.png')
        self.health = 1

class GreenAlien(Enemy):
    def __init__(self):
        super().__init__(r'space_invaders\images\green.png')
        self.health = 5

class YellowAlien(Enemy):
    def __init__(self):
        super().__init__(r'space_invaders\images\yellow.png')
        self.health = 10

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
        self.surf = pygame.image.load('space_invaders\images\extra.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.top = 500
        self.health = 5

# Create the player
player = Player()

# Make groups to render sprites
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
shields = pygame.sprite.Group()
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

lose = False

game_over_time = None

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

        for enemy in enemies:
            direction = enemy.update(direction, level.speed)
            if pygame.sprite.collide_rect(enemy, player):
                lose = True

            for bullet in enemy_bullets:
                if pygame.sprite.collide_rect(bullet, player):
                    lose = True
                for shield in shields:
                    if pygame.sprite.collide_rect(bullet, shield):
                        shield.health -= 1
                        bullet.kill()
                        if shield.health == 0:
                            shield.kill()

            for bullet in player_bullets:
                if pygame.sprite.collide_rect(enemy, bullet):
                    enemy.health -= 1
                    if enemy.health == 0:
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
                            new_enemy = RedAlien()
                        elif enemy_type == 'green':
                            new_enemy = GreenAlien()
                        elif enemy_type == 'yellow':
                            new_enemy = YellowAlien()
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
                            new_enemy = RedAlien()
                        elif enemy_type == 'green':
                            new_enemy = GreenAlien()
                        elif enemy_type == 'yellow':
                            new_enemy = YellowAlien()

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



    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()

    clock.tick(40)

pygame.quit()
