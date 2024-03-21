import pygame
import random
import math
import json
import os

IMAGES_FOLDER_FILEPATH = os.path.join("pygame", "flappy_bird", "images")
JSON_FILEPATH = os.path.join("pygame", "flappy_bird", "flappy_bird.json")


class FlappyBirdGame:
    def run_game():
        from pygame.locals import (
            RLEACCEL,
            K_LEFT,
            K_RIGHT,
            K_SPACE,
            K_ESCAPE,
            KEYDOWN,
            QUIT,
        )

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
            with open(JSON_FILEPATH, "w") as file:
                json.dump(high_scores, file)

        def load_high_scores():
            if os.path.isfile(JSON_FILEPATH):
                try:
                    with open(JSON_FILEPATH, "r") as file:
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
                high_scores.sort(
                    key=lambda x: x[1], reverse=True
                )  # Sort by score in descending order
                high_scores = high_scores[:10]  # Keep only the top 10 scores
                # Save the updated high scores to a file
                save_high_scores(high_scores)
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
                high_score_text = large_font.render(
                    f"HIGH SCORE!", True, (255, 255, 255)
                )
                txt_surface = small_font.render(text, True, color)
                enter_name_text = small_font.render(
                    f"Enter your name:", True, (255, 255, 255)
                )
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
            def __init__(self, GRAVITY):
                super().__init__()
                self.surf = pygame.image.load(
                    os.path.join(IMAGES_FOLDER_FILEPATH, "fishTile_100.png")
                ).convert()
                self.surf.set_colorkey((0, 0, 0))
                self.rect = self.surf.get_rect()
                self.rect.center = (self.rect.width, screen_height // 2)
                self.surf = pygame.transform.scale(self.surf, (40, 40))
                self.velocity = pygame.math.Vector2(0, 0)
                self.gravity = pygame.math.Vector2(0, GRAVITY)
                # Initial jump force (negative for upward motion)
                self.jump_force = -10
                self.jump_timer = 0  # Timer to control jump delay
                self.jump = False
                self.go = False
                self.mask = pygame.mask.from_surface(self.surf)

            def update(self):
                keys = pygame.key.get_pressed()

                if keys[K_SPACE] and (pygame.time.get_ticks() - self.jump_timer) > 200:
                    self.jump_timer = pygame.time.get_ticks()
                    self.velocity.y = self.jump_force  # Apply the jump force
                    self.jump = True
                    self.go = True

                # Make the jump smoother by gradually reducing upward velocity
                if self.velocity.y < 0:
                    self.velocity.y += 0.5  # Adjust this value for jump speed

                if self.velocity.y >= 0 and self.jump == True:
                    self.velocity += self.gravity
                    self.jump = False

                # Update player's position based on velocity
                self.rect.move_ip(self.velocity)

                if self.rect.y < -30:
                    player.rect.y = -30

                if self.rect.y > screen_height:
                    self.rect.y = screen_height

        class Pipe(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.surf = pygame.image.load(
                    os.path.join(IMAGES_FOLDER_FILEPATH, "block_narrow.png")
                ).convert()
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)
                # self.surf = pygame.image.load(random.choice((r"pygame\flappy_bird\images\hill_large.png",
                #  r"pygame\flappy_bird\images\hill_largeAlt.png",
                #  r"pygame\flappy_bird\images\hill_small.png",
                #  r"pygame\flappy_bird\images\hill_smallAlt.png")))
                self.surf = pygame.transform.scale(self.surf, (60, 300))
                self.rect = self.surf.get_rect()
                self.checked = False
                self.mask = pygame.mask.from_surface(self.surf)

            def update(self, speed):
                self.rect.move_ip(speed, 0)

        class TopPipe(Pipe):
            def __init__(self, height):
                super().__init__()
                self.surf = pygame.transform.flip(self.surf, 0, 1)
                self.rect.y = height

        class BottomPipe(Pipe):
            def __init__(self, height):
                super().__init__()
                self.rect.y = height

        class Level:
            def __init__(self):
                self.round = 1
                self.speed = -2

        all_sprites = pygame.sprite.Group()
        pipes = pygame.sprite.Group()

        background = pygame.image.load(
            os.path.join(IMAGES_FOLDER_FILEPATH, "blue_grass.png")
        ).convert()
        GRAVITY = 4
        clock = pygame.time.Clock()
        running = True
        lose = False
        got_high_scores = False

        player = Player(GRAVITY)
        all_sprites.add(player)

        height = random.randint(-200, 0)
        new_pipe = TopPipe(height)
        new_pipe.rect.x = screen_width // 2
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)

        new_pipe = BottomPipe(screen_height + height - 100)
        new_pipe.rect.x = screen_width // 2
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)

        height = random.randint(-200, 0)
        new_pipe = TopPipe(height)
        new_pipe.rect.x = screen_width - 125
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)

        new_pipe = BottomPipe(screen_height + height - 100)
        new_pipe.rect.x = screen_width - 125
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)

        height = random.randint(-200, 0)
        new_pipe = TopPipe(height)
        new_pipe.rect.x = screen_width + 125
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)

        new_pipe = BottomPipe(screen_height + height - 100)
        new_pipe.rect.x = screen_width + 125
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)
        score = 0
        score_counter = 0
        game_over_time = None

        level = Level()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            # Clear the screen
            screen.blit(background, (0, -180))

            if lose and not got_high_scores:
                if game_over_time == None:
                    game_over_time = pygame.time.get_ticks()

                if (
                    pygame.time.get_ticks() - game_over_time < 5000
                ):  # Display game over message for 5 seconds
                    game_over_text = large_font.render(
                        "GAME OVER", True, (220, 20, 60), (0, 0, 0)
                    )
                    screen.blit(
                        game_over_text,
                        (
                            screen_width // 2 - game_over_text.get_width() // 2,
                            screen_height // 2 - game_over_text.get_height() // 2,
                        ),
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
                    text = small_font.render(
                        text, True, (0, 0, 0), (208, 244, 247))
                    screen.blit(text, (screen_width // 2 - 100, y))
                    y += text.get_height()
                y += text.get_height()
                text = "Press ESC to exit."
                text = small_font.render(
                    text, True, (0, 0, 0), (208, 244, 247))
                screen.blit(text, (screen_width // 2 -
                            text.get_width() // 2, y))

            player.update()

            if player.go:
                for pipe in pipes:
                    pipe.update(level.speed)
                    if (
                        pipe.rect.x < player.rect.x
                        and pipe.__class__.__name__ == "BottomPipe"
                    ):
                        if pipe.checked == False:
                            height = random.randint(-200, 0)
                            new_pipe = TopPipe(height)
                            new_pipe.rect.x = screen_width
                            pipes.add(new_pipe)
                            all_sprites.add(new_pipe)

                            new_pipe = BottomPipe(screen_height + height - 100)
                            new_pipe.rect.x = screen_width
                            pipes.add(new_pipe)
                            all_sprites.add(new_pipe)
                            pipe.checked = True
                            if not lose:
                                score += 1
                    if pygame.sprite.collide_mask(player, pipe):
                        lose = True
                        player.velocity = pygame.math.Vector2(level.speed, 0)
                        player.jump_force = 0
                        player.gravity = pygame.math.Vector2(0, 0)

            score_text = small_font.render(
                f"{score}", True, (0, 0, 0), (208, 244, 247))
            screen.blit(
                score_text,
                (
                    screen_width - score_text.get_width() * 2,
                    score_text.get_height() // 2,
                ),
            )

            # Draw all sprites
            for sprite in all_sprites:
                screen.blit(sprite.surf, sprite.rect)

            level.speed *= 1.0001

            pygame.display.flip()

            clock.tick(60)


if __name__ == "__main__":
    FlappyBirdGame.run_game()
