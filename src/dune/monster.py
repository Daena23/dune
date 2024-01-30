from random import choice
import random
from copy import deepcopy
from configurations import COORDINATE_VARIANTS


class Monster:
    def __init__(self):
        self.y_monster = 0
        self.x_monster = 0
        self.direction = "undefined"
        self.id = 0
        self.name = ""
        self.is_alive = True
        self.x_monster_old_coord = []
        self.y_monster_old_coord = []

    def monster_death(self, my_monsters):
        for monster in my_monsters:
            if not self.is_alive:
                print(f'dead monster: {monster}')
                my_monsters.remove(monster)
        return my_monsters


class MonsterCat(Monster):

    def __init__(self):
        super().__init__()
        # Это нужно, чтобы для наследника выполнился тот код, который написан в __init__ базового класса
        self.name = "Cat"
        self.id = 4

    def monster_move(self, lines):
        direction_variants = direction_variants_identification(self, lines)
        if lines.step % 2 == 0:
            monster_new_coord = self.y_monster, self.x_monster, self.direction
        else:
            monster_new_coord = random_action(self, direction_variants)
        return monster_new_coord


class MonsterDog(Monster):
    def __init__(self):
        super().__init__()
        self.name = "Dog"
        self.id = 5

    def monster_move(self, lines):
        direction_variants = direction_variants_identification(self, lines)
        if self.direction == 'undefined' or self.direction == 'no_way':
            monster_new_coord = random_action(self, direction_variants)
        else:
            monster_new_coord = action_straight(self, direction_variants, lines)
        return monster_new_coord


    # Функции
    # функции движения монстров


def direction_variants_identification(monster, lines):
    # Функция поиска направления монстром
    direction_variants = []
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        y_sum, x_sum = monster.y_monster + y_dir, monster.x_monster + x_dir
        if [y_sum, x_sum] in lines.penetrable_cell_coord:
            direction_variants.append([y_sum, x_sum, dir_name])
    # print('dir_var', direction_variants)
    return direction_variants


def monster_movement(monster, lines):
    y_monster, x_monster, monster_direction, monster_id, is_alive = monster.y_monster, monster.x_monster, monster.direction, monster.id, monster.is_alive
    monster.y_monster_old_coord, monster.x_monster_old_coord = y_monster, x_monster
    monster_new_coord = monster.monster_move(lines)
    monster.y_monster, monster.x_monster, monster.direction = monster_new_coord


def random_action(monster, direction_variants):
    # Функция рандомного движения монстра
    if len(direction_variants) > 0:
        monster_new_coord = choice(direction_variants)
    else:
        monster_new_coord = [monster.y_monster, monster.x_monster, 'no_way']
    return monster_new_coord


def action_straight(monster, direction_variants, lines):
    # ФУНКЦИЯ движения по прямой с возможностью поворота
    p_turn = 0.9
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        y_sum = monster.y_monster + y_dir
        x_sum = monster.x_monster + x_dir
        if monster.direction == dir_name and [y_sum, x_sum] in lines.penetrable_cell_coord:
            monster_new_coord = [y_sum, x_sum, dir_name]
            if len(direction_variants) > 2 and p_turn < random.random():
                monster_new_coord = casual_turn(monster, monster_new_coord, direction_variants)
        elif monster.direction == dir_name and [y_sum, x_sum] not in lines.penetrable_cell_coord:
            monster_new_coord = random_action(monster, direction_variants)
    return monster_new_coord


def casual_turn(monster, monster_new_coord, direction_variants):
    # откатить к предыд коорд
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        if dir_name == monster_new_coord[2]:
            y_monster_reverse = monster.y_monster - y_dir
            x_monster_reverse = monster.x_monster - x_dir
    for i in range(len(direction_variants)):
        if y_monster_reverse == direction_variants[i][0] and x_monster_reverse == direction_variants[i][1]:
            direction_variants.pop(i)
            break
    monster_new_coord = choice(direction_variants)
    return monster_new_coord


