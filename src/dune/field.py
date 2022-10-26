import random
from random import choice
from copy import deepcopy
from typing import List

from utils import INIT_POSITIONS, COORDINATE_VARIANTS
from monster import MonsterDog
from monster import MonsterCat
from wall import Boundary_Wall
from wall import Unbreakable_Wall
from wall import Breakable_Wall
from grave import Grave

# Monster, Player, Portal, Explosion, Bomb, BreakableWall, UnbreakableWall

# print_symbol
# x, y
# get_affected_by_explosion
# can_player_pass
# can_monster_pass


class Field:
    def __init__(self, size=13, p_walls=0.3):
        self.size = size
        self.p_walls = p_walls
        self.empty_field = []
        self.breakable_walls_coord = []
        self.field_with_walls = []
        self.empty_cell_coord = []
        self.penetrable_cells_coord = []
        self.field: List[List[List]] = []
        self.step = 0
        self.postmortem_steps = 0
        self.monster_list_init = []
        zero_field = self.zero_field_creation()
        self.empty_field_creation(zero_field)
        self.breakable_walls_list_creation()
        self.field_with_walls_creation()  # заполняем breakable walls
        self.empty_cells_identification()  # делаем лист с координатами пустых ячеек
        self.can_player_pass = True
        self.can_monster_pass = True

    def zero_field_creation(self):
        zero_field = []
        for y in range(self.size):
             zero_field.append([[] for _ in range(self.size)])
        return zero_field

    def empty_field_creation(self, zero_field):
        self.empty_field = zero_field
        for t in range(self.size):
            for m in range(self.size):
                if (t % 2 == 0) and (m % 2 == 0):
                    unbreakable_wall = Unbreakable_Wall()
                    self.empty_field[t][m].append(unbreakable_wall)  # unbreakable intermediate walls
                if t == 0 or t == self.size - 1:
                    unbreakable_wall = Boundary_Wall()
                    self.empty_field[t][m].append(unbreakable_wall)  # boundary walls
                if m == 0 or m == self.size - 1:
                    unbreakable_wall = Boundary_Wall()
                    self.empty_field[t][m].append(unbreakable_wall)  # boundary walls

    def breakable_walls_list_creation(self):
        for t in range(self.size):
            for m in range(self.size):
                cell_item = self.empty_field[t][m]
                if len(cell_item) == 0:
                    if random.random() < self.p_walls:
                        self.breakable_walls_coord.append([t, m])
        for i in range(len(INIT_POSITIONS)):
            if INIT_POSITIONS[i] in self.breakable_walls_coord:
                self.breakable_walls_coord.remove(INIT_POSITIONS[i])
        self.breakable_walls_coord.sort()
        return self.breakable_walls_coord

    def field_with_walls_creation(self):
        self.field_with_walls = deepcopy(self.empty_field)
        for y, x in self.breakable_walls_coord:
            breakable_wall = Breakable_Wall()
            self.field_with_walls[y][x].append(breakable_wall)

    def empty_cells_identification(self):
        for y in range(self.size):
            for x in range(self.size):
                if len(self.field_with_walls[y][x]) == 0:
                    self.empty_cell_coord.append([y, x])

    def playfield_visualization(self):
        print('    0  1  2  3  4  5  6  7  8  9  10 11 12')
        for t in range(self.size):
            if t < 10:
                print(t, '  ', end='')
            else:
                print(t, ' ', end='')
            for m in range(self.size):
                cell_item = self.field[t][m]
                if len(cell_item) > 0:  # and type(cell_item[0]) != str:
                    priority = 0
                    print_symbol = cell_item[0].print_symbol
                    for i in range(len(cell_item)):
                        if cell_item[i].priority > priority:
                            priority = cell_item[i].priority
                            print_symbol = cell_item[i].print_symbol
                    d = print_symbol
                    d += '  '
                    print(d, end='')
                else:
                    print('   ', end='')
            print()
        print()

    def monster_coord_ident_init(self):
        monster_list_init = []
        n_monster = 4
        # n_monster = random.randint(int(self.size / 3), int(self.size / 2))
        monster_available_cells = self.empty_cell_coord.copy()
        for counter in INIT_POSITIONS:
            if counter in monster_available_cells:
                monster_available_cells.remove(counter)
        while n_monster > len(monster_available_cells):
            n_monster = random.randint(1, self.size)
            # создаем лист с init координатами монстров
        for counter in range(n_monster):
            monster_coord_init = choice(monster_available_cells)
            y_monster, x_monster = monster_coord_init
            monster_list_init.append([y_monster, x_monster, "undefined", True])
        monster_list_init.sort()
        return monster_list_init

    def create_monsters(self):
        all_monsters = []
        n_monster_types = 2
        for i in range(len(self.monster_list_init)):
            monster_description = self.monster_list_init[i]
            monster_rand = random.randint(0, 4) / n_monster_types
            if monster_rand > 1:
                monster = MonsterDog()
            else:
                monster = MonsterCat()
            all_monsters.append(monster)
            monster.y_old_coord = []
            monster.x_old_coord = []
            monster.y, monster.x, monster.direction, monster.is_alive = monster_description
            # ВАЖНО!all_monsters - лист с обьектами monster, monster - обьект, содержащий информацию о координатах и направлении
        return all_monsters

    def penetrable_cells_coord_ident(self):
        for y in range(self.size):
            for x in range(self.size):
                if len(self.field[y][x]) == 0:
                    self.penetrable_cells_coord.append([y, x])
                cell_item = self.field[y][x]
                for object_counter in range(len(cell_item)):
                    if cell_item[object_counter].can_player_pass and cell_item[object_counter].can_monster_pass:
                        self.penetrable_cells_coord.append([y, x])
        self.penetrable_cells_coord.append([1, 1])
        self.penetrable_cells_coord = [list(x) for x in sorted(set([tuple(y) for y in self.penetrable_cells_coord]))]
        self.penetrable_cells_coord.sort()
        return self.penetrable_cells_coord

    def field_player_and_monsters_placement_init(self, player, all_monsters):
        self.field = self.field_with_walls
        self.field[1][1].append(player)
        for monster in all_monsters:
            self.field[monster.y][monster.x].append(monster)
        return self.field


