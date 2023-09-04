from space_invaders.space_invaders import SpaceInvadersGame
from missiles.missiles import MissilesGame

import pygame
from pygame.locals import *

# Initialize Pygame and create a screen
pygame.init()
pygame.font.init()
large_font = pygame.font.SysFont("freesansbold", 100)
small_font = pygame.font.SysFont("freesansbold", 30)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define button coordinates and dimensions
button_play_game1 = pygame.Rect(100, 200, 250, 50)
button_play_game2 = pygame.Rect(450, 200, 250, 50)

# Main menu loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_play_game1.collidepoint(mouse_pos):
                SpaceInvadersGame.run_game()
                
            elif button_play_game2.collidepoint(mouse_pos):
                MissilesGame.run_game()

    # Draw the main menu
    screen.fill((204, 204, 255))
    pygame.draw.rect(screen, (0, 128, 255), button_play_game1)
    pygame.draw.rect(screen, (0, 128, 255), button_play_game2)

    # Add button labels
    title_text = large_font.render("RETRO ARCADE GAME", True, (102, 0, 102))
    screen.blit(title_text, 
                (screen_width / 2 - title_text.get_width() / 2, 100))
    play_space_invaders_text = small_font.render("Play Space Invaders", True, (102, 0, 102))
    screen.blit(play_space_invaders_text,
                (button_play_game1.x + (button_play_game1.width // 2 - play_space_invaders_text.get_width() // 2),
                 button_play_game1.y + (button_play_game1.height // 2 - play_space_invaders_text.get_height() // 2)))
    play_missiles = small_font.render("Play Missiles", True, (102, 0, 102))
    screen.blit(play_missiles,
                (button_play_game2.x + (button_play_game2.width // 2 - play_missiles.get_width() // 2),
                 button_play_game2.y + (button_play_game2.height // 2 - play_missiles.get_height() // 2)))

    pygame.display.flip()

pygame.quit()