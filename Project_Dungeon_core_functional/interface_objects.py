import pygame
import os
import dungeon
import random

# LOADING SCREEN
class Load_button:
    # Load button on the loading screen
    def __init__(self,screen, font):
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.width = screen.get_width() /2 - 70
        self.height = screen.get_height() /2 + 50
        self.text = font.render('LOAD', True, (255, 255, 255))
        self.screen = screen

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
            pygame.draw.rect(screen,self.color_light,[self.width,self.height,140,40])
        else:
            pygame.draw.rect(screen, self.color_dark,[self.width, self.height, 140, 40])
        self.screen.blit(self.text, (self.width + 30, self.height + 5))

    def click(self, event, game_state):
        global loading_screen, load_game
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
                game_state.loading_screen = False
                game_state.load_game = True
                existing_file = False
                while existing_file == False:
                    filename = input("Input your saved file in format hero_name_DMY_HMS.dng: ")
                    if os.path.exists(filename):
                        existing_file = True
                        with open(filename, "rb") as f:
                            dungeon = pickle.load(f)
                            hero_name = filename.split('_')[0] # cool advice from chatGPT
                    else:
                        break
        
class Play_button:
    # Play button on the loading screen
    def __init__(self,screen, font):
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.width = screen.get_width() /2 - 70
        self.height = screen.get_height() /2
        self.text = font.render('PLAY', True, (255, 255, 255))
        self.screen = screen

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.width <= mouse[0] <= self.width + 140 and self.height <= mouse[1] <= self.height + 40:
            pygame.draw.rect(screen,self.color_light,[self.width,self.height,140,40])
        else:
            pygame.draw.rect(screen, self.color_dark,[self.width, self.height, 140, 40])
        self.screen.blit(self.text, (self.width + 30, self.height + 5))

    def click(self, event, dungeon, game_state):
        global loading_screen, play_game
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

class Game_map:
    def __init__(self, dungeon, screen):
        self.size = dungeon.size
        self.dungeon = dungeon
        self.tile_size = 50
        self.screen = screen
        self.decorations = 25
        self.values = [dungeon_wall, wall_decoration]
        self.walls = None

    def Make_walls(self):
        # New function just because the decorations weren't working otherwise
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
        # Should make the whole game map + entities
        for y, row in enumerate(self.walls):
            for x, symbol in enumerate(row):
                block = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                    self.tile_size, self.tile_size)
                if symbol:
                    self.screen.blit(symbol, (x*self.tile_size, y*self.tile_size))

        for y, row in enumerate(self.dungeon.current_map):
            for x, symbol in enumerate(row):
                if symbol == "@":  # Hero
                    self.screen.blit(player_figure, (x * self.tile_size, y * self.tile_size))
                elif symbol == "g":  # Goblin = Cactus in this case
                    self.screen.blit(goblin_model, (x * self.tile_size, y * self.tile_size))

class Text_window:
    def __init__ (self, screen, window_font):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height() - 100
        self.font = window_font
        self.text = "Use WASD to move, press SPACE to attack"

    def text_window_update(self, message):
        self.text = message

    def draw (self):
        pygame.draw.rect(self.screen, (0,0,0), [0, self.height, self.width, 100])
        pygame.draw.rect(self.screen, (119, 109, 93), [0, self.height, self.width, 100], border_radius=20)
        lines = self.text.split("\n")
        for i, line in enumerate(lines):
            rendered_line = self.font.render(line ,True, (0,0,0))
            self.screen.blit(rendered_line, (10, self.height+10 + i * 20))
        
