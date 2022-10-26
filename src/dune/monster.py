from random import choice
import random
from copy import deepcopy
from utils import COORDINATE_VARIANTS


class Monster:
    def __init__(self):
        self.priority = 3
        self.y = 0
        self.x = 0
        self.direction = "undefined"
        self.id = 0
        self.name = ""
        self.is_alive = True
        self.x_old_coord = []
        self.y_old_coord = []
        self.can_player_pass = True
        self.can_monster_pass = True
        self.stop_explosion = False
        self.explosible = False

    def monster_death(self, all_monsters):
        for monster in all_monsters:
            if not self.is_alive:
                print(f'dead monster: {monster}')
                all_monsters.remove(monster)
        return all_monsters


class MonsterCat(Monster):

    def __init__(self):
        super().__init__()
        # Это нужно, чтобы для наследника выполнился тот код, который написан в __init__ базового класса
        self.name = "Cat"
        self.print_symbol = 'C'

    def monster_move(self, field):
        direction_variants = direction_variants_identification(self, field)
        if field.step % 2 == 0:
            monster_new_coord = self.y, self.x, self.direction
        else:
            monster_new_coord = random_action(self, direction_variants)
        return monster_new_coord


class MonsterDog(Monster):
    def __init__(self):
        super().__init__()
        self.name = "Dog"
        self.print_symbol = 'D'

    def monster_move(self, field):
        direction_variants = direction_variants_identification(self, field)
        if self.direction == 'undefined' or self.direction == 'no_way':
            monster_new_coord = random_action(self, direction_variants)
        else:
            monster_new_coord = action_straight(self, direction_variants, field)
        return monster_new_coord

    # Функции
    # функции движения монстров


def direction_variants_identification(monster, field):
    # Функция поиска направления монстром
    direction_variants = []
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        y_sum, x_sum = monster.y + y_dir, monster.x + x_dir
        if [y_sum, x_sum] in field.penetrable_cells_coord:
            direction_variants.append([y_sum, x_sum, dir_name])
    # print('dir_var', direction_variants)
    return direction_variants


def monster_movement(monster, field):
    y_monster, x_monster, monster_direction, is_alive = monster.y, monster.x, monster.direction, monster.is_alive
    monster.y_old_coord, monster.x_old_coord = y_monster, x_monster
    monster_new_coord = monster.monster_move(field)
    monster.y, monster.x, monster.direction = monster_new_coord
    if monster.y_old_coord != monster.y or monster.x_old_coord != monster.x and monster in field.field[monster.y_old_coord][monster.x_old_coord]:
        field.field[monster.y_old_coord][monster.x_old_coord].remove(monster)
        field.field[monster.y][monster.x].append(monster)


def random_action(monster, direction_variants):
    # Функция рандомного движения монстра
    if len(direction_variants) > 0:
        monster_new_coord = choice(direction_variants)
    else:
        monster_new_coord = [monster.y, monster.x, 'no_way']
    return monster_new_coord


def action_straight(monster, direction_variants, field):
    # ФУНКЦИЯ движения по прямой с возможностью поворота
    p_turn = 0.9
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        y_sum = monster.y + y_dir
        x_sum = monster.x + x_dir
        if monster.direction == dir_name and [y_sum, x_sum] in field.penetrable_cells_coord:
            monster_new_coord = [y_sum, x_sum, dir_name]
            if len(direction_variants) > 2 and p_turn < random.random():
                monster_new_coord = casual_turn(monster, monster_new_coord, direction_variants)
        elif monster.direction == dir_name and [y_sum, x_sum] not in field.penetrable_cells_coord:
            monster_new_coord = random_action(monster, direction_variants)
    return monster_new_coord


def casual_turn(monster, monster_new_coord, direction_variants):
    # откатить к предыд коорд
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        if dir_name == monster_new_coord[2]:
            y_monster_reverse = monster.y - y_dir
            x_monster_reverse = monster.x - x_dir
    for i in range(len(direction_variants)):
        if y_monster_reverse == direction_variants[i][0] and x_monster_reverse == direction_variants[i][1]:
            direction_variants.pop(i)
            break
    monster_new_coord = choice(direction_variants)
    return monster_new_coord
