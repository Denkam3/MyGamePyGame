from abstract_classes import AbstractDungeon
from copy import deepcopy
from map_entities import Hero, Goblin
import random
from interface_objects import Text_window as window

class Dungeon(AbstractDungeon):
    def __init__(self, size: tuple, tunnel_number: int, hero_name: str, text_window):
        super().__init__(size)
        self.hero = Hero("@", hero_name, [1, 1], 5, 5, 1)
        self.tunnel_number = tunnel_number
        self.starting_entities = ["goblin", "goblin"]
        self.entities = []
        self.empty_space = []
        self.starting_position = (1, 1)
        self.message = ""
        self.create_dungeon()
        self.text_window = text_window

    def __str__(self):
        printable_map = ""
        for row in self.current_map:
            for column in row:
                printable_map += column
            printable_map += "\n"
        return printable_map

    def create_dungeon(self):
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
            if not fighting:
                self.message ="Your big sword is hitting the air really hard!"
                self.text_window.text_window_update(self.message)

        self.update_map(self.entities)

        if self.hero.hp < 1:
            self.message += "\nTHIS IS THE END"

    def place_entities(self):
        position = random.sample(self.empty_space, len(self.starting_entities))
        for idx, entity in enumerate(self.starting_entities):
            if entity == "goblin":
                self.entities.append(Goblin(identifier="g", position = position[idx], base_attack = -1, base_ac = 0, damage = 1))
            for entity in self.entities:
                self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

    def update_map(self, entities: list):
        self.current_map = deepcopy(self.dungeon_map)
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier

    def fight(self, monster):
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
                self.hero.xp += 1
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
