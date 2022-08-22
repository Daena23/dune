from random import choice
import random
from copy import deepcopy

PENETRABLE_OBJECTS = [0, 4, 5, 7, 8, 9]
OBJECTS_TO_STOP_EXPLOSION = [1, 2]
NON_EXPLOSIBLE_OBJECTS = [1, 2, 7, 8]  # 1 - boundary wall, 2 - unbreakable intermediate walls, 7 - burst, 8 - grave
EXPLOSIBLE_OBJECTS = [0, 3, 4, 5, 6, 7, 8, 9, 10]  # 3 - breakable wall, 4, 5 - monsters, 6 - bomb,  9 - player, 10 - portal
OBJECTS_PASSED_BY_THE_EXPLOSION_BEAM = [0, 4, 5, 6, 7, 8, 9]
COORDINATE_VARIANTS = [[-1, 0, 'up'], [0, -1, 'left'], [1, 0, 'down'], [0, 1, 'right']]
PLAYER_COORDINATE_VARIANTS = [[-1, 0, 'up', 'w', 't'], [0, -1, 'left', 'a', 'f'], [1, 0, 'down', 's', 'g'],
                              [0, 1, 'right', 'd', 'h'], [0, 0, 'stay', 'z', 'x']]
INIT_POSITIONS = [[1, 1], [2, 1], [1, 2]]


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


def monster_one_step(monster, lines):
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


player_alive = True


# Player functions
class Player:
    def __init__(self):
        self.id = 9
        self.y_player = 1
        self.x_player = 1
        self.y_player_old_coord = 1
        self.x_player_old_coord = 1
        self.player_alive = True
        self.refractory_period = False
        self.player_coord = [1, 1, False]

    def player_move(self, lines, event):
        if self.player_alive:
            for i in range(len(PLAYER_COORDINATE_VARIANTS)):
                y_player_new = self.y_player + PLAYER_COORDINATE_VARIANTS[i][0]
                x_player_new = self.x_player + PLAYER_COORDINATE_VARIANTS[i][1]
                direction_choice = False
                if event == PLAYER_COORDINATE_VARIANTS[i][3] or event == PLAYER_COORDINATE_VARIANTS[i][4]:
                    direction_choice = True
                if direction_choice and [y_player_new, x_player_new] in lines.penetrable_cell_coord:
                    self.y_player_old_coord = self.y_player
                    self.x_player_old_coord = self.x_player
                    self.y_player = y_player_new
                    self.x_player = x_player_new
        self.player_coord = [self.y_player, self.x_player, self.refractory_period]
        return self.player_coord

    def if_player_eaten(self, monster):
        eating_condition = False
        if self.player_alive:
            if monster.y_monster == self.y_player and monster.x_monster == self.x_player:
                eating_condition = True
                print('you are eaten')
                self.player_dead()

            # к следующему условию мгого вопросов: надо еще добавить старые координаты монстра
            switch_eating_condition1 = False
            switch_eating_condition2 = False
            if monster.y_monster == self.y_player_old_coord and monster.x_monster == self.x_player_old_coord:
                switch_eating_condition1 = True
            if monster.y_monster_old_coord == self.y_player and monster.x_monster_old_coord == self.x_player:
                switch_eating_condition2 = True
            if switch_eating_condition1 and switch_eating_condition2:
                print('sam nabizhal na monstra')
                self.player_dead()

    def player_dead(self):
        self.id = 8
        self.player_alive = False

    def bomb_creation(self, lines, my_bombs):
        # bomb_number += 1
        bomb = Bomb()
        bomb.bomb_exist = True
        self.refractory_period = True
        bomb.y_coord = self.y_player
        bomb.x_coord = self.x_player
        bomb.timer = 0
        bomb.explosion_area = bomb.bomb_explosion_area_ident(lines)
        my_bombs.append(bomb)
        return my_bombs

    def is_player_win(self, lines, portal):
        if self.y == portal.y and self.x == portal.x:
            lines.field[self.y, self.x] = 11
            print('you win!')
            return True
        return False


class Field:
    def __init__(self, size=13, p_walls=0.3):
        self.size = size
        self.p_walls = p_walls
        self.lines = []
        self.zero_field = []
        self.empty_field = []
        self.breakable_walls_coord = []
        self.field_with_walls = []
        self.empty_cell_coord = []
        self.penetrable_cell_coord = []
        self.field = []
        self.step = 0
        self.postmortem_steps = 0
        self.monster_list_init = []
        self.zero_field_creation()
        self.empty_field_creation()
        self.breakable_walls_list_creation()
        self.field_with_walls_creation()  # заполняем breakable walls
        self.empty_cells_identification()  # делаем лист с координатами пустых ячеек

    def zero_field_creation(self):
        for x in range(self.size):
            self.zero_field.append([0] * self.size)

    def empty_field_creation(self):
        self.empty_field = deepcopy(self.zero_field)
        for t in range(self.size):
            for m in range(self.size):
                if (t % 2 == 0) and (m % 2 == 0):
                    self.empty_field[t][m] = 2  # unbreakable intermediate walls
                if t == 0 or t == self.size - 1:
                    self.empty_field[t][m] = 1  # boundary walls
                if m == 0 or m == self.size - 1:
                    self.empty_field[t][m] = 1  # boundary walls

    def breakable_walls_list_creation(self):
        for t in range(self.size):
            for m in range(self.size):
                if self.empty_field[t][m] != 1 and self.empty_field[t][m] != 2:
                    if random.random() < self.p_walls:
                        self.breakable_walls_coord.append([t, m])
        for i in range(len(INIT_POSITIONS)):
            if INIT_POSITIONS[i] in self.breakable_walls_coord:
                self.breakable_walls_coord.remove(INIT_POSITIONS[i])
        self.breakable_walls_coord.sort()
        return self.breakable_walls_coord

    def field_with_walls_creation(self):
        self.field_with_walls = deepcopy(self.empty_field)
        for counter in range(len(self.breakable_walls_coord)):
            y_breakable_wall, x_breakable_wall = self.breakable_walls_coord[counter]
            self.field_with_walls[y_breakable_wall][x_breakable_wall] = 3
        return self.field_with_walls

    def empty_cells_identification(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.field_with_walls[y][x] == 0:
                    self.empty_cell_coord.append([y, x])

    def monster_coord_ident_init(self):
        monster_list_init = []
        monster_available_cells = self.empty_cell_coord.copy()
        for counter in range(len(INIT_POSITIONS)):
            if INIT_POSITIONS[counter] in monster_available_cells:
                monster_available_cells.remove(INIT_POSITIONS[counter])
        # n_monster = random.randint(int(self.size / 7), int(self.size * 1))
        n_monster = 1
        while n_monster > len(monster_available_cells):
            n_monster = random.randint(3, self.size)
            # создаем лист с init координатами монстров
            is_alive = True
        for counter in range(n_monster):
            monster_coord_init = choice(monster_available_cells)
            y_monster, x_monster = monster_coord_init
            monster_list_init.append([y_monster, x_monster, "undefined", True])
        monster_list_init.sort()
        return monster_list_init

    def monster_arrangement_init(self):
        my_monsters = []
        n_monster_types = 2
        for i in range(len(self.monster_list_init)):
            monster_description = self.monster_list_init[i]
            monster_rand = random.randint(0, 4) / n_monster_types
            if monster_rand > 1:
                monster = MonsterDog()
            else:
                monster = MonsterCat()
            monster.y_monster_old_coord = []
            monster.x_monster_old_coord = []
            monster.y_monster, monster.x_monster, monster.direction, monster.is_alive = monster_description
            my_monsters.append(monster)
            # ВАЖНО!my_monsters - лист с обьектами monster, monster - обьект, содержащий информацию о координатах и направлении
        return my_monsters

    def penetrable_cell_coord_ident(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.field_with_walls[y][x] in PENETRABLE_OBJECTS:
                    self.penetrable_cell_coord.append([y, x])
        self.penetrable_cell_coord.append([1, 1])
        return self.penetrable_cell_coord

    def field_player_and_monsters_arrangement_init(self, my_monsters):
        self.field = deepcopy(self.field_with_walls)
        self.field[1][1] = 9
        for monster in my_monsters:
            self.field[monster.y_monster][monster.x_monster] = monster.id
        # self.field[1][2] = 0
        # self.field[2][1] = 0
        return self.field

    def wall_explosion(self, bomb):
        if bomb.timer == bomb.explosion_time:
            print('Hello, Im a wall explosion:', bomb.walls_to_explode_coord)
            for wall_coords_to_remove in bomb.walls_to_explode_coord:
                if wall_coords_to_remove in self.breakable_walls_coord:
                    self.breakable_walls_coord.remove(wall_coords_to_remove)
                    self.penetrable_cell_coord.append(wall_coords_to_remove)
            bomb.walls_to_explode_coord = []
        return self.breakable_walls_coord

    def playfield_update(self, player, my_monsters, my_bombs, bomb):
        self.field = self.field_with_walls_creation()
        if my_bombs != 0:
            for bomb in my_bombs:
                if bomb.bomb_exist and bomb.timer < bomb.explosion_time:
                    self.field[bomb.y][bomb.x] = bomb.id

        self.field[player.y_player][player.x_player] = player.id
        for monster in my_monsters:
            self.field[monster.y_monster][monster.x_monster] = monster.id
        if my_bombs != 0:
            for bomb in my_bombs:
                if bomb.timer == bomb.explosion_time:
                    for counter in range(len(bomb.explosion_area)):
                        y_explosion, x_explosion = bomb.explosion_area[counter]
                        self.field[y_explosion][x_explosion] = bomb.explosion_id
                    bomb.bomb_disappearance(player, my_bombs)
        return self.field

    def playfield_creation(self):
        print('    0  1  2  3  4  5  6  7  8  9  10 11 12 14 15 16 17 18 19')
        for t in range(self.size):
            if t < 10:
                d = str(t) + ' '
            else:
                d = str(t) + ''
            for m in range(self.size):
                x = self.field[t][m]
                d = d + '  '
                if x == 0:
                    d += ' '
                elif x == 1:
                    d += '#'
                elif x == 2:
                    d += '#'
                elif x == 3:
                    d += '+'
                elif x == 4:
                    d += 'C'
                elif x == 5:
                    d = d + 'D'
                elif x == 6:
                    d += 'B'
                elif x == 7:
                    d += 'E'
                elif x == 8:
                    d += 'M'
                elif x == 9:
                    d += 'P'
                elif x == 10:
                    d += 'T'
                else:
                    d += ''
            print(d)
        print()


class Bomb:
    def __init__(self):
        self.id = 6
        self.explosion_id = 7
        self.bomb_exist = False
        self.y_coord = 0
        self.x_coord = 0
        self.timer = 0
        self.explosion_area = []
        self.explosion_time = 5
        self.walls_to_explode_coord = []
        self.explosion_power = 1

    @staticmethod
    def bomb_positioning(player, lines, my_bombs):
        wasd = ['w', 'a', 's', 'd', 'z']
        tfgh = ['t', 'f', 'g', 'h', 'x']
        if player.is_alive:
            if not player.refractory_period:
                event = input('Do you want to put a bomb? Enter the direction of player | wasd/tfgh')
                if event in wasd:
                    player_coord = player.player_move(lines, event)
                elif event in tfgh:
                    player.bomb_creation(lines, my_bombs)
                    player_coord = player.player_move(lines, event)
            elif player.refractory_period:
                event = input('Enter the direction of player | wasd')
                player_coord = player.player_move(lines, event)
        return player.player_coord

    def bomb_impassability(self, lines):
        if self.bomb_exist and self.timer == 0:
            lines.penetrable_cell_coord.remove([self.y_coord, self.x_coord])
        if self.timer == 4:
            lines.penetrable_cell_coord.append([self.y_coord, self.x_coord])

    # print(len(lines.penetrable_cell_coord), lines.penetrable_cell_coord)

    def bomb_explosion_area_ident(self, lines):
        self.explosion_area.append([self.y_coord, self.x_coord])
        for direction_id in range(len(COORDINATE_VARIANTS)):
            y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
            for power in range(self.explosion_power):
                y_explosion, x_explosion = self.y_coord + y_dir * power, self.x_coord + x_dir * power
                print('y_explosion, x_explosion', y_explosion, x_explosion)
                if lines.field[y_explosion][x_explosion] in OBJECTS_TO_STOP_EXPLOSION:
                    break
                if [y_explosion, x_explosion] not in self.explosion_area:
                    self.explosion_area.append([y_explosion, x_explosion])
                if lines.field[y_explosion][x_explosion] == EXPLOSIBLE_OBJECTS[1]:
                    self.walls_to_explode_coord.append([y_explosion, x_explosion])
                    break
        print('walls_to_explode_coord', self.walls_to_explode_coord, 'explosion_area', self.explosion_area)
        return self.explosion_area

    def bomb_disappearance(self, player, my_bombs):
        self.timer = 0
        self.explosion_area = []
        self.bomb_exist = False
        player.refractory_period = False
        for self.bomb in my_bombs:
            self.bomb_exist is False
            my_bombs.remove(self.bomb)

    def bomb_kills_player(self, player):
        if self.timer == self.explosion_time and [player.y_player, player.x_player] in self.explosion_area:
            player.player_dead()
            print('you are dead due to explosion. game over')

    def bomb_kills_monster(self, my_monsters, my_bombs):
        for monster in my_monsters:
            for self.bomb in my_bombs:
                if self.timer == self.explosion_time and [monster.y_monster, monster.x_monster] in self.explosion_area:
                    self.monster_dead(my_monsters, monster)
                    print('monster is dead', monster.y_monster, monster.x_monster, monster.name)

    def monster_dead(self, my_monsters, monster):
        for monster in my_monsters:
            monster.is_alive is False
            my_monsters.remove(monster)

class Portal:
    def __init__(self):
        self.portal_exists = False
        self.y = 0
        self.x = 0
        self.id = 10

    def portal_appearance(self, lines, my_monsters, player):
        if len(my_monsters) == 0 and not self.portal_exists:
            self.portal_exists = True
            portal_coord = choice(lines.penetrable_cell_coord)
            print('port', portal_coord)
            self.y, self.x = portal_coord
            lines.field[self.y][self.x] = self.id