"""
The main file to run the game. It is a rewritten ASCII game.
Some code is a remnant of the original ASCII game, Pygame logic and textures were added.
The game is a dungeon crawler where the player can move around and attack enemies.
"""
from dungeon import Dungeon
import pygame
import interface_objects

# Game states
class GameState:
    """
    Class to manage the game states.

    Attributes:
        loading_screen (bool): True if the game is in the loading screen.
        play_game (bool): True if the game is being played.
    """
    def __init__(self):
        """
        Initializes the game state.
        """
        self.loading_screen = True
        self.play_game = False

# Variables I need
load_inicialized = False
game_state = GameState()
pygame.init()
screen = pygame.display.set_mode((500, 625))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont('Corbel', 35)
window_font = pygame.font.SysFont('Corbel', 20, bold = True)
stat_window_font = pygame.font.SysFont('Corbel', 20, bold = True)
load_button = interface_objects.Load_button(screen, font)
play_button = interface_objects.Play_button(screen, font)
text_window = interface_objects.Text_window(screen, window_font)
save_button = interface_objects.Save_button(screen, font, text_window)
myStats = interface_objects.MyStats(screen, stat_window_font)
dungeon = Dungeon(size=(10, 10), tunnel_number=40, hero_name="Soci", text_window=text_window)
game_map = interface_objects.Game_map(dungeon, screen)
game_map.Make_walls()
player_pos = pygame.Vector2(dungeon.hero.position[0], dungeon.hero.position[1])

# Core
last_move_time = 0
move_delay = 200

while running:
    """
    Main loop of the game. Handles events and movements.
    """
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state.loading_screen:
            load_button.click(event, game_state, dungeon)
            play_button.click(event,dungeon, game_state)
        if game_state.play_game:
            save_button.click(event, game_state, dungeon)
            

    if game_state.loading_screen: 
        screen.fill((192,192,192))
        load_button.draw(screen)
        play_button.draw(screen)
                
    elif game_state.play_game:
        screen.fill((200,200,255))
        if not load_inicialized:
            game_map = interface_objects.Game_map(dungeon, screen)
            game_map.Make_walls()
            player_pos = pygame.Vector2(dungeon.hero.position[0], dungeon.hero.position[1])
            load_inicialized = True
        game_map.draw(dungeon)
        text_window.draw()
        save_button.draw()
        myStats.draw(dungeon)

        if current_time - last_move_time > move_delay:
            if keys[pygame.K_w]:
                dungeon.hero_action("U")
                last_move_time = current_time
            if keys[pygame.K_s]:
                dungeon.hero_action("D")
                last_move_time = current_time
            if keys[pygame.K_a]:
                dungeon.hero_action("L")
                last_move_time = current_time
            if keys[pygame.K_d]:
                dungeon.hero_action("R")
                last_move_time = current_time
            if keys[pygame.K_SPACE]:
                dungeon.hero_action("A")
                last_move_time = current_time
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
