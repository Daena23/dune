import random
from random import choice
from copy import deepcopy
from utils import INIT_POSITIONS, PENETRABLE_OBJECTS
from monster import MonsterDog
from monster import MonsterCat


class Field:
    def __init__(self, size=13, p_walls=0):
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
        for y_breakable_wall, x_breakable_wall in self.breakable_walls_coord:
            self.field_with_walls[y_breakable_wall][x_breakable_wall] = 3

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
        n_monster = random.randint(int(self.size / 7), int(self.size * 1))
        # n_monster = 0
        while n_monster > len(monster_available_cells):
            n_monster = random.randint(3, self.size)
            # создаем лист с init координатами монстров
        for counter in range(n_monster):
            monster_coord_init = choice(monster_available_cells)
            y_monster, x_monster = monster_coord_init
            monster_list_init.append([y_monster, x_monster, "undefined", True])
        monster_list_init.sort()
        return monster_list_init

    def create_monsters(self):
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
        self.penetrable_cell_coord = [list(x) for x in sorted(set([tuple(y) for y in self.penetrable_cell_coord]))]
        return self.penetrable_cell_coord

    def field_player_and_monsters_placement_init(self, my_monsters):
        self.field = deepcopy(self.field_with_walls)
        self.field[1][1] = 9
        for monster in my_monsters:
            self.field[monster.y_monster][monster.x_monster] = monster.id
        # self.field[1][2] = 0
        # self.field[2][1] = 0
        return self.field

    def playfield_update(self, player, my_monsters, my_bombs, portal):
        self.field_with_walls_creation()
        self.field = self.field_with_walls
        # ставим бомбы
        for bomb in my_bombs:
            if bomb.bomb_exist and bomb.timer < bomb.explosion_time - 1:
                self.field[bomb.y][bomb.x] = bomb.id
        # ставим монстров и игрока
        self.field[player.y_player][player.x_player] = player.id
        if portal.portal_exists:
            self.field[portal.y][portal.x] = portal.id
        if player.is_player_win(portal):
            self.field[player.y_player][player.x_player] = player.player_win_id
        for monster in my_monsters:
            self.field[monster.y_monster][monster.x_monster] = monster.id
        # взрыв бомбы и ее исчезновение
        for bomb in my_bombs:
            if bomb.timer == bomb.explosion_time - 1:
                for y_explosion, x_explosion in bomb.explosion_area:
                    self.field[y_explosion][x_explosion] = bomb.explosion_id
            if bomb.timer == bomb.explosion_time:
                my_bombs.remove(bomb)

        return self.field

    def playfield_visualization(self):
        print('    0  1  2  3  4  5  6  7  8  9  10 11 12')
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
                elif x == 11:
                    d += 'W'
                else:
                    d += ''
            print(d)
        print()
