from random import choice
import random
from copy import deepcopy


PENETRABLE_OBJECTS = [0, 4, 5, 7, 8, 9]
NON_EXPLOSIBLE_OBJECTS = [1, 2, 7, 8] # 1 - boundary wall, 2 - unbreakable intermediate walls, 7 - burst, 8 - grave
EXPLOSIBLE_OBJECTS = [0, 3, 4, 5, 6, 7, 8, 9]  # 3 - breakable wall, 4, 5 - monsters, 6 - bomb,  9 - player
COORDINATE_VARIANTS = [[-1, 0, 'up'], [0, -1, 'left'], [1, 0, 'down'], [0, 1, 'right']]
PLAYER_COORDINATE_VARIANTS = [[-1, 0, 'up', 'w'], [0, -1, 'left', 'a'], [1, 0, 'down', 's'], [0, 1, 'right', 'd'], [0, 0, 'stay', 'z']]
INIT_POSITIONS = [[1, 1], [2, 1], [1, 2]]


class Monster:
    def __init__(self):
        self.x_monster = 0
        self.y_monster = 0
        self.direction = "undefined"
        self.id = 0
        self.name = ""
        self.if_monster_alive = True

    def monster_death(self, my_monsters):
        my_monsters_copy = []
        my_monsters_copy = deepcopy(my_monsters)
        for monster in my_monsters:
            if not self.if_monster_alive:
                my_monsters_copy.remove(monster)
        print(f'monsters: {my_monsters}')
        print(f'my_monsters_copy: {my_monsters_copy}')
        my_monsters_copy = my_monsters
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
            monster_new_coord = random_action(self.y_monster, self.x_monster, direction_variants)
        return monster_new_coord


class MonsterDog(Monster):
    def __init__(self):
        super().__init__()
        self.name = "Dog"
        self.id = 5

    def move(self, lines, step):
        direction_variants = direction_variants_identification(self, lines)
        if self.direction == 'undefined' or self.direction == 'no_way':
            monster_new_coord = random_action(self.y_monster, self.x_monster, direction_variants)
        else:
            monster_new_coord = action_straight(self.x_monster, self.y_monster, self.direction, direction_variants, lines.penetrable_cell_coord)
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


def random_action(monster, direction_variants):
    # Функция рандомного движения монстра
    if len(direction_variants) > 0:
        monster_new_coord = choice(direction_variants)
    else:
        monster_new_coord = [monster.y_monster, monster.x_monster, 'no_way']
    return monster_new_coord


def action_straight(x_monster, y_monster, monster_direction, direction_variants, lines):
    # ФУНКЦИЯ движения по прямой с возможностью поворота
    p_turn = 0.9
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        y_sum = y_monster + y_dir
        x_sum = x_monster + x_dir
        if monster_direction == dir_name and [y_sum, x_sum] in lines.penetrable_cell_coord:
            monster_new_coord = [y_sum, x_sum, dir_name]
            if len(direction_variants) > 2 and p_turn < random.random():
                monster_new_coord = casual_turn(x_monster, y_monster, monster_new_coord, direction_variants)
        elif monster_direction == dir_name and [y_sum, x_sum] not in lines.penetrable_cell_coord:
            monster_new_coord = random_action(x_monster, y_monster, direction_variants)
    return monster_new_coord


def casual_turn(x_monster, y_monster, monster_new_coord, direction_variants):
    # откатить к предыд коорд
    for direction_id in range(len(COORDINATE_VARIANTS)):
        y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
        if dir_name == monster_new_coord[2]:
            y_monster_reverse = y_monster - y_dir
            x_monster_reverse = x_monster - x_dir
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


    def player_move(self, lines):
        if self.player_alive:
            event = input('Enter the direction of player')
            for i in range(len(PLAYER_COORDINATE_VARIANTS)):
                y_player_new = self.y_player + PLAYER_COORDINATE_VARIANTS[i][0]
                x_player_new = self.x_player + PLAYER_COORDINATE_VARIANTS[i][1]
                if event == PLAYER_COORDINATE_VARIANTS[i][3] and [y_player_new, x_player_new] in lines.penetrable_cell_coord:
                    self.y_player_old_coord = self.y_player
                    self.x_player_old_coord = self.x_player
                    self.y_player = y_player_new
                    self.x_player = x_player_new
        self.player_coord = [self.y_player, self.x_player, self.refractory_period]
        return self.player_coord

    def if_player_eaten(self, monster_new_coord, monster_old_coord):
        eating_condition1 = False
        eating_condition2 = False
        if self.player_alive:
            if monster_new_coord[0] == self.y_player and monster_new_coord[1] == self.x_player:
                eating_condition1 = True
                print('you are eaten')
            if monster_new_coord[0] == self.y_player_old_coord and monster_new_coord[1] == self.x_player_old_coord:
                eating_condition2 = True
                print('sam nabizhal na monstra')
            if eating_condition1 or eating_condition2:
                self.player_dead()


    def player_dead(self):
        self.id = 8
        self.player_alive = False
        print('game over')


    def bomb_creation(self, bomb, lines):
        # bomb_number += 1
        bomb.bomb_exist = True
        self.refractory_period = True
        bomb.y_bomb_coord = self.y_player
        bomb.x_bomb_coord = self.x_player
        bomb.bomb_timer = 0
        bomb.explosion_area = bomb.bomb_explosion_area_ident(lines)


class Lines:
    def __init__(self):
        self.size = 13
        self.p_walls = 0.3
        self.lines = []
        self.zero_field = []
        self.empty_field = []
        self.breakable_walls_coord = []
        self.field_with_walls = []
        self.empty_cell_coord = []
        self.monster_list_init = []
        self.penetrable_cell_coord = []
        self.field = []
        self.step = 0
        self.postmortem_steps = 0
        self.if_monster_alive = True

    def zero_field_creation(self):
        for x in range(self.size):
            self.zero_field.append([0] * self.size)
        return self.zero_field

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
        return self.empty_field


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
        return self.empty_cell_coord

    def monster_coord_ident(self):
        monster_available_cells = self.empty_cell_coord.copy()
        for counter in range(len(INIT_POSITIONS)):
            if INIT_POSITIONS[counter] in monster_available_cells:
                monster_available_cells.remove(INIT_POSITIONS[counter])
        n_empty = len(monster_available_cells)
        n_monster = random.randint(int(self.size / 2), int(self.size * 1.2))
        while n_monster > n_empty:
            n_monster = random.randint(3, self.size)

        # создаем лист с init координатами монстров
        for counter in range(n_monster):
            monster_new_coord = choice(monster_available_cells)
            y_monster, x_monster = monster_new_coord
            self.monster_list_init.append([y_monster, x_monster, 'undefined', self.if_monster_alive])
        self.monster_list_init.sort()
        return self.monster_list_init

    def monster_arrangement(self):
        monster_list_curr = deepcopy(self.monster_list_init)
        my_monsters = []
        n_monster_types = 2
        for i in range(len(monster_list_curr)):
            monster_description = monster_list_curr[i]
            monster_rand = random.randint(0, 4) / n_monster_types
            if monster_rand > 1:
                monster = MonsterDog()
            else:
                monster = MonsterCat()
            monster.y_monster, monster.x_monster, monster.direction, monster.if_monster_alive = monster_description
            my_monsters.append(monster)
            # ВАЖНО!my_monsters - лист с обьектами monster, monster - обьект, содержащий информацию о координатах и направлении
            # print(monster.y_monster, monster.x_monster, '|', monster.name, '')
        return my_monsters

    def penetrable_cell_coord_ident(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.field_with_walls[y][x] in PENETRABLE_OBJECTS:
                    self.penetrable_cell_coord.append([y, x])
        self.penetrable_cell_coord.append([1, 1])
        return self.penetrable_cell_coord

    def field_creation_init(self, my_monsters):
        self.field = deepcopy(self.field_with_walls)
        self.field[1][1] = 9
        for monster in my_monsters:
            self.field[monster.y_monster][monster.x_monster] = monster.id
        self.field[1][2] = 0
        self.field[2][1] = 0
        return self.field


    def wall_explosion(self, bomb):
        if len(bomb.breakable_walls_for_removal_coord) != 0 and bomb.bomb_timer == bomb.explosion_time:
            for counter in range(len(bomb.breakable_walls_for_removal_coord)):
                self.breakable_walls_coord.remove(bomb.breakable_walls_for_removal_coord[counter])
                self.penetrable_cell_coord.append(bomb.breakable_walls_for_removal_coord[counter])
        return self.breakable_walls_coord


    def playfield_update(self, bomb, player, my_monsters):
        self.field = self.field_with_walls_creation()
        if bomb.bomb_exist is True and bomb.bomb_timer < bomb.explosion_time:
            self.field[bomb.y_bomb_coord][bomb.x_bomb_coord] = bomb.id
        self.field[player.y_player][player.x_player] = player.id
        for monster in my_monsters:
            self.field[monster.y_monster][monster.x_monster] = monster.id

        if bomb.bomb_timer == bomb.explosion_time:
            for counter in range(len(bomb.explosion_area)):
                y_explosion, x_explosion = bomb.explosion_area[counter]
                self.field[y_explosion][x_explosion] = bomb.explosion_id
            bomb.bomb_disappearance(player)
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
                else:
                    d += ''
            print(d)
        print()


class Bomb:
    def __init__(self):
        self.id = 6
        self.explosion_id = 7
        self.bomb_exist = False
        self.y_bomb_coord = 0
        self.x_bomb_coord = 0
        self.bomb_timer = 0
        self.explosion_area = []
        self.explosion_time = [3, 4]
        self.breakable_walls_for_removal_coord = []

    def bomb_positioning(self, player, lines):
        if player.is_alive and not player.refractory_period:
            event_bomb = input('Do you want to put a bomb?')
            if event_bomb == 'y':
                player.bomb_creation(self, lines)
                bomb = Bomb()


    def bomb_explosion_area_ident(self, lines):
        self.explosion_area.append([self.y_bomb_coord, self.x_bomb_coord])
        for direction_id in range(len(COORDINATE_VARIANTS)):
            y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
            y_explosion, x_explosion = self.y_bomb_coord + y_dir, self.x_bomb_coord + x_dir
            if lines.field[y_explosion][x_explosion] in EXPLOSIBLE_OBJECTS:
                self.explosion_area.append([y_explosion, x_explosion])
            if lines.field[y_explosion][x_explosion] == EXPLOSIBLE_OBJECTS[1]:
                self.breakable_walls_for_removal_coord.append([y_explosion, x_explosion])
        return self.explosion_area

    def bomb_disappearance(self, player):
        self.bomb_timer = 0
        self.explosion_area = []
        self.bomb_exist = False
        self.breakable_walls_for_removal_coord = []
        player.refractory_period = False


    def bomb_kills_player(self, player):
        if self.bomb_timer == self.explosion_time - 1 and [player.y_player, player.x_player] in self.explosion_area:
            player.player_dead()
            print('you are dead due to explosion. game over')

    def bomb_kills_monster(self, my_monsters):
        for monster in my_monsters:
            if self.bomb_timer == self.explosion_time - 1 and [monster.y_monster, monster.x_monster] in self.explosion_area:
                monster.monster_dead()
                print('monster is dead')

    def monster_dead(self, my_monsters):
        for monster in my_monsters:
            monster.monster_alive[monster] is False

