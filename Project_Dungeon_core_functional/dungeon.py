"""
This file creates the dungeon in the old ASCII way. It is a template used for the pygame textures.
It places entities on the map and handles actions of the hero and fights.
Saving a loading is handled here.
"""

from abstract_classes import AbstractDungeon
from copy import deepcopy
from map_entities import Hero, Evil_Cactus, Duckie
import random
import pickle
import pygame

class Dungeon(AbstractDungeon):
    """
    Class to create the dungeon and handle the game logic.

    Attributes:
        size (tuple): Size of the dungeon.
        tunnel_number (int): Number of tunnels in the dungeon.
        hero_name (str): Name of the hero.
        text_window (Text_window): Text window object.
        hero (Hero): Hero object.
        tunnel_number (int): Number of tunnels in the dungeon.
        starting_entities (list): List of starting entities.
        entities (list): List of entities in the dungeon.
        empty_space (list): List of empty spaces in the dungeon.
        starting_position (tuple): Starting position of the hero.
        message (str): Message to be displayed in the text window.
        dungeon_map (list): Dungeon map.
        current_map (list): Current map.
    """
    def __init__(self, size: tuple, tunnel_number: int, hero_name: str, text_window):
        """
        Initializes the dungeon.

        Arguments:
            size (tuple): Size of the dungeon.
            tunnel_number (int): Number of tunnels in the dungeon.
            hero_name (str): Name of the hero.
            text_window (Text_window): Text window object.
        """
        super().__init__(size)
        self.hero = Hero("@", hero_name, [1, 1], 5, 5, 1)
        self.tunnel_number = tunnel_number
        self.starting_entities = ["Evil cactus", "Evil cactus", "Evil cactus"]
        self.entities = []
        self.empty_space = []
        self.starting_position = (1, 1)
        self.message = ""
        self.create_dungeon()
        self.text_window = text_window
        self.portal_on_map = False
        self.portal_position = None
    
    def save(self, filename, game_state):
        """
        Handles saving the game.
        Pygame.surface can't be saved error solution.

        Arguments:
            filename (str): Name of the file to save the game.
        """
        with open(filename, "wb") as f:
            pickle.dump({
                'hero': self.hero,
                'tunnel_number': self.tunnel_number,
                'starting_entities': self.starting_entities,
                'entities': self.entities,
                'empty_space': self.empty_space,
                'starting_position': self.starting_position,
                'message': self.message,
                'dungeon_map': self.dungeon_map,
                'current_map': self.current_map,
                'portal_on_map': self.portal_on_map,
                'portal_position': self.portal_position,
                'next_level': game_state.next_level,
            }, f)
        self.message = "Game saved."
        self.text_window.text_window_update(self.message)

    def load(self, filename, game_state):
        """
        Handles loading the game.

        Arguments:
            filename (str): Name of the file to load the game.
        """
        with open(filename, "rb") as f:
            data = pickle.load(f)
            self.hero = data['hero']
            self.tunnel_number = data['tunnel_number']
            self.starting_entities = data['starting_entities']
            self.entities = data['entities']
            self.empty_space = data['empty_space']
            self.starting_position = data['starting_position']
            self.message = data['message']
            self.dungeon_map = data['dungeon_map']
            self.current_map = data['current_map']
            self.portal_on_map = data['portal_on_map']
            self.portal_position = data['portal_position']
            game_state.next_level = data.get('next_level')

            if game_state.next_level:
                self.portal_on_map = False
                self.portal_position = None
    
    def create_dungeon(self):
        """
        Creates the dungeon and places entities on the map.
        """
        for x in range(self.size[0]):
            dungeon_row = []
            for y in range(self.size[1]):
                dungeon_row.append("▓")
            self.dungeon_map.append(dungeon_row)
        self.dungeon_map[self.starting_position[0]][self.starting_position[1]] = "."
        self.tunnel()
        for x in range(len(self.dungeon_map)):
            for y in range(len(self.dungeon_map[0])):
                if self.dungeon_map[x][y] == ".":
                    self.empty_space.append((x, y))
        self.place_entities()
        self.current_map = deepcopy(self.dungeon_map)
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier
        

    def tunnel(self):
        """
        Random tunneling for the dungeon.
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = (1,1)
        dig = 0
        while dig < self.tunnel_number:
            random.shuffle(directions)
            for move_x, move_y in directions:
                steps = random.randint(1, min(self.size[0], self.size[1]) - 2) # rectangle or square
                new_x = x + move_x * steps
                new_y = y + move_y * steps
            
                if 1 <= new_x < self.size[1] - 1 and 1 <= new_y < self.size[0] - 1:
                    if self.dungeon_map[new_y][new_x] == "▓" or self.dungeon_map[new_y][new_x] == ".":
                        for step in range(steps + 1):
                            if move_x != 0:
                                self.dungeon_map[y][x + (move_x * step)] = "." # generate path horizontal
                            if move_y != 0:
                                self.dungeon_map[y + (move_y * step)][x] = "." # generate path vertical
                        x, y = new_x, new_y
                        dig += 1           
                else:
                    break

    def hero_action(self, action):
        """
        Handles the hero actions. Remnants of the old ASCII game.

        Arguments:
            action (str): Action to be performed.
        """
        if action == "R" or action == "r":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] + 1] != "▓":
                self.hero.position[1] += 1
                self.update_map(self.entities)
            else:
                self.message = "You can't go that way!"
                self.text_window.text_window_update(self.message)
                
        if action == "L" or action == "l":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] - 1] != "▓":
                self.hero.position[1] -= 1
                self.update_map(self.entities)
            else:
                self.message = "You can't go that way!"
                self.text_window.text_window_update(self.message)
                
        if action == "D" or action == "d":
            if self.dungeon_map[self.hero.position[0] + 1][self.hero.position[1]] != "▓":
                self.hero.position[0] += 1
                self.update_map(self.entities)
            else:
                self.message = "You can't go that way!"
                self.text_window.text_window_update(self.message)
                
        if action == "U" or action == "u":
            if self.dungeon_map[self.hero.position[0] - 1][self.hero.position[1]] != "▓":
                self.hero.position[0] -= 1
                self.update_map(self.entities)
            else:
                self.message = "You can't go that way!"
                self.text_window.text_window_update(self.message)
                
        elif action == "A" or action == "a":
            fighting = False
            for entity in self.entities:
                hero_x, hero_y = self.hero.position
                entity_x, entity_y = entity.position
                if abs(hero_x - entity_x) + abs(hero_y - entity_y) == 1:
                    if hasattr(entity, "attack"):
                        self.fight(entity)
                        fighting = True
                        break # Attack only one entity in range
            if not fighting:
                self.message ="Your big sword is hitting the air really hard!"
                self.text_window.text_window_update(self.message)

        self.update_map(self.entities)

        if self.hero.hp < 1:
            self.message += "\nTHIS IS THE END"

    def place_entities(self):
        """
        Places entities on the map.
        """
        position = random.sample(self.empty_space, len(self.starting_entities))
        for idx, entity in enumerate(self.starting_entities):
            if entity == "Evil cactus":
                self.entities.append(Evil_Cactus(identifier="g", position = position[idx], base_attack = -1, base_ac = 0, damage = 1))
            if entity == "Duckie":
                self.entities.append(Duckie(identifier="d", position = position[idx], base_attack = -1, base_ac = 0, damage = 2))
            for entity in self.entities:
                self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

    def update_map(self, entities: list):
        """
        Updates the map with the entities.

        Arguments:
            entities (list): List of entities.
        """
        self.current_map = deepcopy(self.dungeon_map)
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier

    def fight(self, monster):
        """
        Fight between the hero and the monster.
        Fight logic goes pew pew.

        Arguments:
            monster (Entity): Monster entity.
        """
        hero_roll = self.hero.attack()
        monster_roll = monster.attack()
        if hero_roll["attack_roll"] > monster.base_ac:
            monster.hp -= hero_roll["inflicted_damage"]
            if monster.hp > 0:
                self.message = f"Hero inflicted {hero_roll['inflicted_damage']} damage"
                self.text_window.text_window_update(self.message)
            else:
                self.message = f"Hero Hero inflicted {hero_roll['inflicted_damage']} damage and slain {monster}"
                self.text_window.text_window_update(self.message)
                self.hero.gold += monster.gold
                self.hero.xp += 10
                self.dungeon_map[monster.position[0]][monster.position[1]] = "."
                self.entities.remove(monster)
        if monster_roll["attack_roll"] > self.hero.base_ac:
            self.message += f"\nMonster inflicted {monster_roll['inflicted_damage']} damage"
            self.text_window.text_window_update(self.message)
            self.hero.hp -= monster_roll['inflicted_damage']
            if self.hero.hp < 1:
                self.message += f"{self.hero.name} have been slained by {monster}"
                self.text_window.text_window_update(self.message)
        self.message += f"\nHero HP: {self.hero.hp}  Monster HP: {monster.hp}"
        self.text_window.text_window_update(self.message)

    def portal(self, screen):
        """
        Portal to the next level.
        """
        if not self.portal_on_map:
            self.portal_position = list(random.choice(self.empty_space))
            self.portal_on_map = True
        
        # Add transparency to the portal
        portal_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        portal_surface.fill((255, 191, 13, 128)) 

        screen.blit(portal_surface, (self.portal_position[1] * 50, self.portal_position[0] * 50 + 25))   