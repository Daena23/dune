import random
from random import choice
from wall import Breakable_Wall
from monster import MonsterDog
from monster import MonsterCat

class Explosion:
    def __init__(self, x, y):
        self.print_symbol = 'E'
        self.priority = 5
        self.y = y
        self.x = x
        self.can_player_pass = True
        self.can_monster_pass = True
        self.stop_explosion = False
        self.explosible = False
        self.current_time = 0
        self.explosion_duration = 1

    def explosion_update(self, field, all_explosions):
        if self.current_time == self.explosion_duration:
            field.field[self.y][self.x].remove(self)
            all_explosions.remove(self)
            return False
        else:
            self.current_time += 1
            return True

    def kills_player(self, field, player):
        cell_items = field.field[player.y][player.x]
        if self in cell_items:
            player.player_dead(field)

    def kills_monster(self, field, all_monsters):
        dead_monsters = []
        for monster in all_monsters:
            cell_items = field.field[monster.y][monster.x]
            if self in cell_items:
                monster.is_alive = False
                dead_monsters.append(monster)
                print('monster is dead', monster.y, monster.x, monster.name)
        for monster in dead_monsters:
            field.field[monster.y][monster.x].remove(monster)
            all_monsters.remove(monster)

    def wall(self, field):
        cell_items = field.field[self.y][self.x]
        for item in cell_items.copy():
            if isinstance(item, Breakable_Wall): #The isinstance() function returns True if the specified object is of the specified type, otherwise False
                # print(self.y, self.x, type(item), isinstance(item, Breakable_Wall))
                field.field[self.y][self.x].remove(item)
                field.penetrable_cells_coord.append([self.y, self.x])

    def bomb_explodes_bomb(self, field, bomb):
        cell_items = field.field[self.y][self.x]
        cell_items = field.field[self.y][self.x]
        if bomb in cell_items.copy():
            bomb.timer = bomb.explosion_time

    def portal(self, field, all_monsters, portal):
        cell_items = field.field[self.y][self.x]
        if portal in cell_items:
            if not portal.closed_by_wall and self not in portal.ignored_explosions:
                portal.monster_creation_after_explosion(field, all_monsters)
            elif portal.closed_by_wall:
                portal.closed_by_wall = False
                portal.ignored_explosions.append(self)