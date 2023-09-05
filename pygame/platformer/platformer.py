import pygame
import random
import math
import json
import os

class PlatformerGame:
    def run_game():

        from pygame.locals import RLEACCEL, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, KEYDOWN, QUIT

        # Initialize Pygame and create a screen
        pygame.init()
        pygame.font.init()

        large_font = pygame.font.SysFont("freesansbold", 100)
        small_font = pygame.font.SysFont("freesansbold", 50)
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))

        GRAVITY = 4

        on_surface = False

        def display_high_scores(high_scores):
            text = ""
            for i, (name, score) in enumerate(high_scores):
                text += f"{i + 1}. {name}: \t\t{score}\n"
            text += "\nPress ESC to exit."
            text = large_font.render(text, True, (255, 255, 255))
            return text


        def save_high_scores(high_scores):
            with open(r"pygame\platformer\platformer.json", "w") as file:
                json.dump(high_scores, file)

        def load_high_scores():
            file_path = r"pygame\platformer\platformer.json"
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as file:
                        return json.load(file)
                except json.JSONDecodeError:
                    # Handle JSON decoding errors (e.g., invalid JSON data in the file)
                    return []
            else:
                # Handle the case where the file doesn't exist
                return []

        def update_high_scores(high_scores, player_score):
            if len(high_scores) < 10 or player_score > high_scores[-1][1]:
                player_name = get_player_name()
                high_scores.append((player_name, player_score))
                high_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order
                high_scores = high_scores[:10]  # Keep only the top 10 scores
                save_high_scores(high_scores)  # Save the updated high scores to a file
            return high_scores

        def get_player_name():
            input_box = pygame.Rect(
                screen_width // 2 - 100, screen_height // 2 - 25, 200, 50
            )
            color_inactive = pygame.Color("lightskyblue3")
            color_active = pygame.Color("dodgerblue2")
            color = color_inactive
            active = False
            text = ""

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False
                        color = color_active if active else color_inactive
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                return text
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            else:
                                text += event.unicode

                screen.fill((30, 30, 30))
                high_score_text = large_font.render(f"HIGH SCORE!", True, (255, 255, 255))
                txt_surface = small_font.render(text, True, color)
                enter_name_text = small_font.render(f"Enter your name:", True, (255, 255, 255))
                width = max(200, txt_surface.get_width() + 10)
                input_box.w = width
                screen.blit(
                        high_score_text,
                        (screen_width // 2 - high_score_text.get_width() // 2, 160),
                    )
                screen.blit(
                        enter_name_text,
                        (screen_width // 2 - enter_name_text.get_width() // 2, 240),
                    )
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pygame.draw.rect(screen, color, input_box, 2)
                pygame.display.flip()
                clock.tick(30)

        class Player(pygame.sprite.Sprite):
            def __init__(self):
                super(Player, self).__init__()
                self.surf = pygame.image.load(
                    r"pygame\platformer\images\playerRed_up1.png"
                ).convert()
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)
                self.rect = self.surf.get_rect()
                self.rect.center = (screen_width // 2, screen_height // 2)
                self.velocity = pygame.math.Vector2(0, 0)
                self.jumping = False
                self.base_jump_velocity = -20
                self.jump_limit = 1
                self.jump_count = 0
                self.last_jump = pygame.time.get_ticks()

            def update(self, on_surface, jump_counter):
                self.velocity = pygame.math.Vector2(0, 0)
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    self.velocity.x = -5
                if keys[K_RIGHT]:
                    self.velocity.x = 5

                if keys[K_SPACE] and self.jump_limit > self.jump_count:
                    if (pygame.time.get_ticks() - self.last_jump) > 200:
                        self.jumping = True  # Start the jump
                        self.jump_velocity = self.base_jump_velocity 
                        self.jump_count += 1
                        jump_counter +=1
                        self.last_jump = pygame.time.get_ticks()
                
                # Handle the player going offscreen
                if player.rect.x < 0:
                    player.rect.x = screen_width
                
                if player.rect.x > screen_width:
                    player.rect.x = 0

                # Apply gravity
                if not on_surface:
                    self.velocity.y += GRAVITY  # Increase vertical velocity due to gravity

                if self.jumping:
                    self.velocity.y += self.jump_velocity  # Apply the jump velocity
                    self.jump_velocity += 1  # Increase jump velocity

                    # Check if jump is complete (reached the peak)
                    if self.jump_velocity >= 0:
                        self.jumping = False

                # Update player's position based on velocity
                self.rect.move_ip(self.velocity)

                # Apply gravity
                self.velocity.y += GRAVITY  # Increase vertical velocity due to gravity

                # Update player's position based on velocity
                self.rect.move_ip(self.velocity)

                return jump_counter


        class Platform(pygame.sprite.Sprite):
            def __init__(self, x, y, width, speed):
                super(Platform, self).__init__()
                self.surf = pygame.image.load(random.choice((r"pygame\platformer\images\tileBlue_07.png",
                                                            r"pygame\platformer\images\tileBrown_08.png",
                                                            r"pygame\platformer\images\tileGreen_07.png",
                                                            r"pygame\platformer\images\tileYellow_08.png")))
                self.surf = pygame.transform.scale(self.surf, (width, 30))  # Resize the image
                self.rect = self.surf.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.velocity = pygame.math.Vector2(0, speed)
            
            def update(self):
                self.rect.move_ip(self.velocity)

        class Level():
            def __init__(self):
                self.round = 1
                self.speed = 1
                self.counter = 0
                self.threshold = 25

            def level_up(self):
                self.counter = 0
                self.speed = math.ceil(1.15 * self.speed)
                self.threshold = math.ceil(self.threshold * 1.3)

        class Cloud(pygame.sprite.Sprite):
            def __init__(self):
                super(Cloud, self).__init__()
                self.surf = pygame.image.load(random.choice((r"pygame\platformer\images\cloud1.png",
                                              r"pygame\platformer\images\cloud2.png",
                                              r"pygame\platformer\images\cloud3.png",
                                              r"pygame\platformer\images\cloud4.png",
                                              r"pygame\platformer\images\cloud5.png",
                                              r"pygame\platformer\images\cloud6.png",
                                              r"pygame\platformer\images\cloud7.png",
                                              r"pygame\platformer\images\cloud8.png",
                                              r"pygame\platformer\images\cloud9.png"))
                )
                self.rect = self.surf.get_rect()
                self.rect.x = random.randint(0, screen_width)
                self.rect.y = 0 - self.surf.get_height()
                self.speed = random.randint(1, 5)

            def update(self):
                self.rect.move_ip(0, self.speed)

        class PowerUp(pygame.sprite.Sprite):
            def __init__(self, type, image_path):
                super(PowerUp, self).__init__()
                self.type = type
                self.surf = pygame.image.load(image_path).convert()
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)
                self.rect = self.surf.get_rect()
                self.rect.x = random.randint(0, screen_width)
                self.rect.y = -10
            
            def update(self):
                self.rect.move_ip(0, 1)
    
        class LowGravity(PowerUp):
            def __init__(self):
                super().__init__("low_gravity", r"pygame\platformer\images\blueCrystal.png")
        
        class DoubleJump(PowerUp):
            def __init__(self):
                super().__init__("double", r"pygame\platformer\images\discRed.png")
        
        class HighJump(PowerUp):
            def __init__(self):
                super().__init__("high", r"pygame\platformer\images\yellowGem.png")

        clock = pygame.time.Clock()
        running = True

        level = Level()

        player = Player()
        platforms = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        # Create and add platform instances to platforms group
        platform = Platform(400, 500, 200, level.speed)
        platforms.add(platform)
        all_sprites.add(platform)

        platform = Platform(random.randint(0, screen_width - 100),
                                            300,
                                            random.randint(100, 300),
                                            level.speed)
        platforms.add(platform)
        all_sprites.add(platform)

        platform = Platform(random.randint(0, screen_width - 100),
                                            100,
                                            random.randint(10, 300),
                                            level.speed)
        platforms.add(platform)
        all_sprites.add(platform)

        platform = Platform(random.randint(0, screen_width - 100),
                                            0,
                                            random.randint(100, 300),
                                            level.speed)
        platforms.add(platform)
        all_sprites.add(platform)
        
        ADD_CLOUD = pygame.USEREVENT + 1
        pygame.time.set_timer(ADD_CLOUD, random.randint(500, 1500))

        ADD_PLATFORM = pygame.USEREVENT + 2
        pygame.time.set_timer(ADD_PLATFORM, 2000)

        ADD_HIGHJUMP = pygame.USEREVENT + 3
        pygame.time.set_timer(ADD_HIGHJUMP, random.randint(10000, 30000))

        ADD_LOW_GRAVITY = pygame.USEREVENT + 4
        pygame.time.set_timer(ADD_LOW_GRAVITY, random.randint(30000, 45000))
                              
        lose = False
        game_over_time = None
        score = 0
        got_high_scores = False
        double_active = False
        double_timer = 0
        high_active = False
        high_timer = 0
        low_gravity_active = False
        low_gravity_timer = 0
        jump_counter = 0

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                if event.type == ADD_CLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

                if event.type == ADD_PLATFORM:
                    if not lose:
                        new_platform = Platform(random.randint(0, screen_width - 100),
                                                -20,
                                                random.randint(50, 200),
                                                level.speed)
                        platforms.add(new_platform)
                        all_sprites.add(new_platform)
                        level.counter += 1
                        score += 1

                if event.type == ADD_HIGHJUMP:
                    if not lose:
                        new_powerup = HighJump()
                        powerups.add(new_powerup)
                        all_sprites.add(new_powerup)

                if event.type == ADD_LOW_GRAVITY:
                    if not lose:
                        new_powerup = LowGravity()
                        powerups.add(new_powerup)
                        all_sprites.add(new_powerup)

            # Clear the screen
            screen.fill((204, 255, 255))

            if lose and not got_high_scores:
                if game_over_time == None:
                    game_over_time = pygame.time.get_ticks()

                if pygame.time.get_ticks() - game_over_time < 5000:  # Display game over message for 5 seconds
                    game_over_text = large_font.render("GAME OVER", True, (220, 20, 60), (204, 255, 255))
                    screen.blit(
                        game_over_text,
                        (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2)
                    )
                else:
                    high_scores = load_high_scores()
                    high_scores = update_high_scores(high_scores, score)
                    high_score_text = display_high_scores(high_scores)
                    got_high_scores = True
            
            if lose and got_high_scores:
                y = 150
                for i, (name, score) in enumerate(high_scores):
                    text = f"{i + 1}. {name}: {score}"
                    text = small_font.render(text, True, (0, 0, 0), (204, 255, 255))
                    screen.blit(text, (screen_width // 2 - 100, y))
                    y += text.get_height()
                y += text.get_height()
                text = "Press ESC to exit."
                text = small_font.render(text, True, (0, 0, 0), (204, 255, 255))
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, y))


            if not lose:
                jump_counter = player.update(on_surface, jump_counter)
                if jump_counter > 30:
                    new_powerup = DoubleJump()
                    powerups.add(new_powerup)
                    all_sprites.add(new_powerup)
                    jump_counter = 0

                # Check for collisions without removing platforms
                if pygame.sprite.spritecollideany(player, platforms) and player.velocity.y > 0:
                    for platform in platforms:
                        if pygame.sprite.collide_rect(player, platform):
                            player.rect.y = (platform.rect.y - player.rect.height)
                            on_surface = True
                            player.jump_count = 0

                else:
                    on_surface = False

                # Remove platforms that are below the screen
                for platform in platforms.copy():
                    if platform.rect.top > screen_height:
                        platforms.remove(platform)

                if player.rect.y > screen_height:
                    lose = True

                if level.counter > level.threshold:
                    level.level_up()

                current_time = pygame.time.get_ticks()

                for powerup in powerups:
                    powerup.update()
                    if pygame.sprite.collide_rect(player, powerup):
                        if powerup.type == 'high':
                            if high_active == False:
                                player.base_jump_velocity = -25
                                high_active = True
                                high_timer = current_time
                        elif powerup.type == 'double':
                            if double_active == False:
                                player.jump_limit = 2
                                double_active == True
                                double_timer = current_time
                        elif powerup.type == 'low_gravity':
                            if low_gravity_active == False:
                                GRAVITY = 2
                                low_gravity_active = True
                                low_gravity_timer = current_time
                        powerup.kill()
                    if powerup.rect.y == screen_height:
                        powerup.kill()

            # Update and draw platforms
            for platform in platforms:
                platform.update()

            for cloud in clouds:
                cloud.update()

            score_text = small_font.render(f"{score}", True, (0, 0, 0), (204, 255, 255))
            screen.blit(
                score_text,
                (screen_width - score_text.get_width() * 2, score_text.get_height() // 2),
            )

            if high_active is True and (current_time - high_timer) > 30000:
                player.base_jump_velocity = -20
                high_active = False

            if double_active is True and (current_time - double_timer) > 30000:
                player.jump_limit = 1
                double_active = False

            if low_gravity_active is True and (current_time - low_gravity_timer) > 30000:
                GRAVITY = 4
                low_gravity_active = False
    
            # Draw all sprites
            for sprite in all_sprites:
                screen.blit(sprite.surf, sprite.rect)

            pygame.display.flip()

            clock.tick(60)

if __name__ == '__main__':
    PlatformerGame.run_game()
    pygame.quit()