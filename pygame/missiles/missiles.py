import pygame
import random
import os
import json
class MissilesGame:
    def run_game():
        # Import pygame.locals for easier access to key coordinates
        from pygame.locals import (
            RLEACCEL,
            K_UP,
            K_DOWN,
            K_LEFT,
            K_RIGHT,
            K_ESCAPE,
            KEYDOWN,
            QUIT
        )

        # Define constants for the screen width and height
        screen_width = 800
        screen_height = 600

        def display_high_scores(high_scores):
            text = ""
            for i, (name, score) in enumerate(high_scores):
                text += f"{i + 1}. {name}: \t\t{score}\n"
            text += "\nPress ESC to exit."
            text = font.render(text, True, (255, 255, 255))
            return text

        def save_high_scores(high_scores):
            with open(r"pygame\missiles\missiles.json", "w") as file:
                json.dump(high_scores, file)

        def load_high_scores():
            file_path = r"pygame\missiles\missiles.json"
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
                high_score_text = font.render(f"HIGH SCORE!", True, (255, 255, 255))
                txt_surface = score_font.render(text, True, color)
                enter_name_text = score_font.render(f"Enter your name:", True, (255, 255, 255))
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


        # Define a player object by extending pygame.sprite.Sprite
        # The surface drawn on the screen is now an attribute of 'player'
        class Player(pygame.sprite.Sprite):
            def __init__(self):
                super(Player, self).__init__()
                self.surf = pygame.image.load("pygame\missiles\images\jet.png").convert()
                self.surf.set_colorkey((255, 255, 255), RLEACCEL)
                self.rect = self.surf.get_rect()
                self.rect.y = screen_height // 2 

            # Move the sprite based on user keypresses
            def update(self, pressed_keys):
                if pressed_keys[K_UP]:
                    self.rect.move_ip(0, -5)
                    move_up_sound.play()
                if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0, 5)
                    move_down_sound.play()
                if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-5, 0)
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(5, 0)

                # Keep player on the screen
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > screen_width:
                    self.rect.right = screen_width
                if self.rect.top <= 0:
                    self.rect.top = 0
                if self.rect.bottom >= screen_height:
                    self.rect.bottom = screen_height

        # Define the enemy object by extending pygame.sprite.Sprite
        # The surface you draw on the screen is now an attribute of 'enemy'
        class Enemy(pygame.sprite.Sprite):
            def __init__(self):
                super(Enemy, self).__init__()
                self.surf = pygame.image.load("pygame\missiles\images\missile.png").convert()
                self.surf.set_colorkey((255, 255, 255), RLEACCEL)
                self.rect = self.surf.get_rect(
                    center=(
                        random.randint(screen_width + 20, screen_width + 100),
                        random.randint(0, screen_height),
                    )
                )
                self.speed = random.randint(5, 20)

            # Move the sprite based on speed
            # Remove the sprite when it passes the left edge of the screen
            def update(self):
                self.rect.move_ip(-self.speed, 0)
                if self.rect.right < 0:
                    self.kill()

        class Cloud(pygame.sprite.Sprite):
            def __init__(self):
                super(Cloud, self).__init__()
                self.surf = pygame.image.load("pygame\missiles\images\cloud.png").convert()
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)
                self.speed = random.randint(-10, -3)
                self.rect = self.surf.get_rect(
                    center=(
                        screen_width+20,
                        random.randint(0, screen_height),

                    )
                )
            # Move the cloud based on a constant speed
            # Remove the cloud when it passes the left edge of the screen
            def update(self):
                self.rect.move_ip(self.speed, 0)
                if self.rect.right < 0:
                    self.kill()

        # Initialize sound
        pygame.mixer.init()

        # Initialize pygame
        pygame.init()
        pygame.font.init()
        font = pygame.font.SysFont("freesansbold", 100)
        score_font = pygame.font.SysFont("freesansbold", 50)

        # Create the screen object
        # The size is determined by the constant screen_width and screen_height
        screen = pygame.display.set_mode((screen_width, screen_height))

        # Create a custom event for adding a new enemy
        ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDENEMY, 250)
        ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDCLOUD, random.randint(600, 1000))

        # Instantiate player. Right now, this is just a rectangle.
        player = Player()

        # Setup the clock for a decent framerate
        clock = pygame.time.Clock()

        # Create groups to hold enemy sprites and all sprites
        # - enemies is used for collision detection and position updates
        # - all_sprites is used for rendering
        enemies = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        # Load and play background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        pygame.mixer.music.load("pygame\missiles\sound\Apoxode_-_Electric_1.mp3")
        pygame.mixer.music.play(loops=-1)

        # Load all sound files
        # Sound sources: Jon Fincher
        move_up_sound = pygame.mixer.Sound("pygame\missiles\sound\Rising_putter.ogg")
        move_down_sound = pygame.mixer.Sound("pygame\missiles\sound\Falling_putter.ogg")
        collision_sound = pygame.mixer.Sound("pygame\missiles\sound\Collision.ogg")

        # Variable to keep the main loop running
        running = True
        lose = False
        score = 0
        got_high_scores = False
        game_over_time = None

        # Main loop
        while running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    running = False

                # Add a new enemy?
                elif event.type == ADDENEMY:
                    if not lose:
                        # Create the new enemy and add it to sprite groups
                        new_enemy = Enemy()
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        score += 1

                # Add a new cloud?
                elif event.type == ADDCLOUD:
                    # Create the new cloud and add it to sprite groups
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

            # Get all the keys currently pressed
            pressed_keys = pygame.key.get_pressed()

            # Update enemy position
            enemies.update()
            clouds.update()

            # Update the player sprite based on user keypresses
            player.update(pressed_keys)

            # Fill the screen with blue
            screen.fill((135, 206, 250))

            if lose and not got_high_scores:
                if game_over_time == None:
                    game_over_time = pygame.time.get_ticks()

                if pygame.time.get_ticks() - game_over_time < 5000:  # Display game over message for 5 seconds
                    game_over_text = font.render("GAME OVER", True, (220, 20, 60), (135, 206, 250))
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
                    text = score_font.render(text, True, (0, 0, 0), (135, 206, 250))
                    screen.blit(text, (screen_width // 2 - 100, y))
                    y += text.get_height()
                y += text.get_height()
                text = "Press ESC to exit."
                text = score_font.render(text, True, (0, 0, 0), (135, 206, 250))
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, y))

            score_text = score_font.render(f"{score}", True, (0, 0, 0), (135, 206, 250))
            screen.blit(
                score_text,
                (screen_width - score_text.get_width() * 2, score_text.get_height() // 2),
            )

            # Draw all sprites
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(player, enemies):
                # Stop any moving sounds and play the collision sound
                move_up_sound.stop()
                move_down_sound.stop()
                collision_sound.play()

                # If so, then remove the player and stop the loop
                player.kill()

                lose = True

            # Update the display
            pygame.display.flip()

            # Ensure the program maintains a rate of 30 frames per second
            clock.tick(30)

if __name__ == '__main__':
    MissilesGame.run_game()
    pygame.quit()
