"""
This file adds appearence to the game.
Textures are defined here along with the working buttons.
"""

import pygame
import os
import random
# from datetime import datetime - maybe I'll make the save better again

# LOADING SCREEN
class Load_button:
    """
    Class that manages the loading button.
    
    Attributes:
        color_light (tuple): RGB color for the button when hovered.
        color_dark (tuple): RGB color thats default for the button.
        width (int): Width of the button.
        height (int): Height of the button.
        text (Surface): Rendered text for the button.
        screen (Surface): Pygame screen surface.
    """
    def __init__(self,screen, font):
        """
        Initialites the load button.

        Arguments:
            creen (Surface): Pygame screen surface.
            font (Font): Pygame font for the text.
        """
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.width = screen.get_width() /2 - 70
        self.height = screen.get_height() /2 + 50
        self.text = font.render('LOAD', True, (255, 255, 255))
        self.screen = screen

    def draw(self, screen):
        """
        Draws the button on the screen.

        Arguments:
            screen (Surface): Pygame screen surface
        """
        mouse = pygame.mouse.get_pos()
        if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
            pygame.draw.rect(screen,self.color_light,[self.width,self.height,140,40])
        else:
            pygame.draw.rect(screen, self.color_dark,[self.width, self.height, 140, 40])
        self.screen.blit(self.text, (self.width + 30, self.height + 5))

    def click(self, event, game_state, dungeon):
        """
        Handles the click event on the button.

        Arguments:
            event (Event): Pygame event.
            game_state (GameState): Game state object.
            dungeon (Dungeon): Dungeon object.
        """
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
                game_state.loading_screen = False
                game_state.play_game = True
                filename = "my_save.dng"
                if os.path.exists(filename):
                    if os.path.getsize(filename) > 0:  # Check if file is not empty
                        dungeon.load(filename)
                    else:
                        print(f"File {filename} is empty.")
                else:
                    print(f"File {filename} does not exist.")
        
        
        
class Play_button:
    """
    Class that manages the play button.

    Attributes:
        color_light (tuple): RGB color for the button when hovered.
        color_dark (tuple): RGB color thats default for the button.
        width (int): Width of the button.
        height (int): Height of the button.
        text (Surface): Rendered text for the button.
        screen (Surface): Pygame screen surface.
    """
    def __init__(self,screen, font):
        """
        Initialites the play button.

        Arguments:
            screen (Surface): Pygame screen surface.
            font (Font): Pygame font for the text.
        """
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.width = screen.get_width() /2 - 70
        self.height = screen.get_height() /2
        self.text = font.render('PLAY', True, (255, 255, 255))
        self.screen = screen

    def draw(self, screen):
        """
        Draws the button on the screen.

        Arguments:
            screen (Surface): Pygame screen surface
        """
        mouse = pygame.mouse.get_pos()
        if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
            pygame.draw.rect(screen,self.color_light,[self.width,self.height,140,40])
        else:
            pygame.draw.rect(screen, self.color_dark,[self.width, self.height, 140, 40])
        self.screen.blit(self.text, (self.width + 30, self.height + 5))

    def click(self, event, dungeon, game_state):
        """
        Handles the click event on the button.
        
        Arguments:
            event (Event): Pygame event.
            dungeon (Dungeon): Dungeon object.
            game_state (GameState): Game state object.
        """
        load_inicialized = True # So I don't have to have two dif game states for loaded and new game
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
                game_state.loading_screen = False
                game_state.play_game = True

# DUNGEON

# Textures
player_figure = pygame.image.load("graphics/player.png")
dungeon_wall = pygame.image.load("graphics/wall_texture.jpg")
wall_decoration = pygame.image.load("graphics/wall_decoration.png")
goblin_model = pygame.image.load("graphics/cactus.png")

# Generate the map with textures
class Game_map:
    """
    Class that manages the game map.

    Attributes:
        size (tuple): Size of the dungeon.
        dungeon (Dungeon): Dungeon object.
        tile_size (int): Size of the tiles.
        screen (Surface): Pygame screen surface.
        decorations (int): Number of decorations.
        values (list): List of textures.
        walls (list): List of walls.
    """
    def __init__(self, dungeon, screen):
        """
        Initializes the game map.

        Arguments:
            dungeon (Dungeon): Dungeon object.
            screen (Surface): Pygame screen surface.
        """
        self.size = dungeon.size
        self.dungeon = dungeon
        self.tile_size = 50
        self.screen = screen
        self.decorations = 25
        self.values = [dungeon_wall, wall_decoration]
        self.walls = None

    def Make_walls(self):
        """
        New function because the decorations weren't working otherwise.
        Makes the walls for the game map.
        """
        self.walls = []
        for y, row in enumerate(self.dungeon.current_map):
            build_row = []
            for x, symbol in enumerate(row):
                if symbol == "▓":
                    random_pick = dungeon_wall
                    if self.decorations > 0:
                        random_pick = random.choice(self.values)
                        if random_pick == wall_decoration:
                            self.decorations -= 1
                    build_row.append(random_pick)
                else:
                    build_row.append(None)
            self.walls.append(build_row)
                
    def draw (self, dungeon):
        """
        Draws the game map.

        Arguments:
            dungeon (Dungeon): Dungeon object.
        """
        for y, row in enumerate(self.walls):
            for x, symbol in enumerate(row):
                block = pygame.Rect(x * self.tile_size, y * self.tile_size + 25,
                                    self.tile_size, self.tile_size)
                if symbol:
                    self.screen.blit(symbol, (x*self.tile_size, y*self.tile_size + 25))

        for y, row in enumerate(self.dungeon.current_map):
            for x, symbol in enumerate(row):
                if symbol == "@":  # Hero
                    self.screen.blit(player_figure, (x * self.tile_size, y * self.tile_size + 25))
                elif symbol == "g":  # Goblin = Cactus in this case
                    self.screen.blit(goblin_model, (x * self.tile_size, y * self.tile_size + 25))

class Text_window:
    """
    Class that manages the text window. 
    Communicates with the player, shows encounter info.

    Attributes:
        screen (Surface): Pygame screen surface.
        width (int): Width of the window.
        height (int): Height of the window.
        font (Font): Pygame font for the text.
        text (str): Text in the window.
    """
    # Text window on the bottom of the main game screen
    def __init__ (self, screen, window_font):
        """
        Initializes the text window.

        Arguments:
            screen (Surface): Pygame screen surface.
            window_font (Font): Pygame font for the text.
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height() - 100
        self.font = window_font
        self.text = "Use WASD to move, press SPACE to attack"

    def text_window_update(self, message):
        """
        Updates the text in the window.

        Arguments:
            message (str): Message to be displayed.
        """
        self.text = message

    def draw (self):
        """
        Draws the text window.
        """
        pygame.draw.rect(self.screen, (0,0,0), [0, self.height, self.width, 100])
        pygame.draw.rect(self.screen, (192, 158, 90), [0, self.height, self.width, 100], border_radius=20)
        lines = self.text.split("\n")
        for i, line in enumerate(lines):
            rendered_line = self.font.render(line ,True, (0,0,0))
            self.screen.blit(rendered_line, (10, self.height+10 + i * 20))

# Save button in Text_window
class Save_button:
    """
    Class that manages the save button.

    Attributes:
        color_light (tuple): RGB color for the button when hovered.
        color_dark (tuple): RGB color thats default for the button.
        width (int): Width of the button.
        height (int): Height of the button.
        text (Surface): Rendered text for the button.
        screen (Surface): Pygame screen surface
    """
    def __init__(self, screen, font, text_window):
        """
        Initializes the save button.

        Arguments:
            screen (Surface): Pygame screen surface.
            font (Font): Pygame font for the text.
            text_window (Text_window): Text window object.
        """
        self.color_light = (170, 170, 170)
        self.color_dark = (0, 0, 0)
        self.width = text_window.width - 110  
        self.height = text_window.height + 50
        self.text = font.render('SAVE', True, (255, 255, 255))
        self.screen = screen

    def draw(self):
        """
        Draws the button on the screen.
        """
        mouse = pygame.mouse.get_pos()
        if self.width <= mouse[0] <= self.width + 100 and self.height <= mouse[1] <= self.height + 40:
            pygame.draw.rect(self.screen, self.color_light, [self.width, self.height, 100, 40])
        else:
            pygame.draw.rect(self.screen, self.color_dark, [self.width, self.height, 100, 40])
        self.screen.blit(self.text, (self.width + 10, self.height + 5))

    def click(self, event, game_state, dungeon):
        """
        Handles the click event on the button.

        Arguments:
            event (Event): Pygame event.
            game_state (GameState): Game state object.
            dungeon (Dungeon): Dungeon object.
        """
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
                filename = "my_save.dng"
                dungeon.save(filename)

class MyStats:
    """
    Class that manages the player stats.

    Attributes:
        screen (Surface): Pygame screen surface.
        width (int): Width of the window.
        height (int): Height of the window.
        font (Font): Pygame font for the text.
    """
    def __init__ (self, screen, stat_window_font):
        """
        Initializes the player stats window.

        Arguments:
            screen (Surface): Pygame screen surface.
            stat_window_font (Font): Pygame font for the text.
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = 0
        self.font = stat_window_font

    def draw (self, dungeon):
        """
        Draws the player stats window.

        Arguments:
            dungeon (Dungeon): Dungeon object.
        """
        pygame.draw.rect(self.screen, (0,0,0), [0, self.height, self.width, 25])
        pygame.draw.rect(self.screen, (192, 158, 90), [0, self.height, self.width, 25], border_radius=20)
        self.text = (
            f"Level: {dungeon.hero.level}     HP: {dungeon.hero.hp}/{dungeon.hero.max_hp}      "
            f"Stamina: {dungeon.hero.stamina}/{dungeon.hero.max_stamina}     XP: {dungeon.hero.xp}     "
            f"Gold: {dungeon.hero.gold}"
        )
        stat = self.font.render(self.text ,True, (0,0,0))
        self.screen.blit(stat, (10, self.height + 2))