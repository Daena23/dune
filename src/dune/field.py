import random
from copy import deepcopy
from typing import List

from bomb import Bomb
from configurations import PENETRABLE_OBJECTS, PLAYER_INIT_POSITIONS, SYMBOLS
from monster import Monster
from player import Player


class Field:
    unbreakable_boundary_wall_id = 1
    unbreakable_intermediate_wall_id = 2
    breakable_wall_id = 3
    max_bombs_number = 3

    def __init__(self, size=13, p_walls=0):
        self.size = size
        self.field = []
        self.empty_field = self.create_empty_field()
        self.breakable_walls_coord = []
        self.penetrable_cells_coord = []
        self.p_walls = p_walls
        self.max_bombs_reached = False

    def create_empty_field(self) -> List:
        zero_field = [[0] * self.size for _ in range(self.size)]
        empty_field = zero_field
        for row in range(self.size):
            for column in range(self.size):
                if row % 2 == column % 2 == 0:
                    empty_field[row][column] = Field.unbreakable_intermediate_wall_id  # unbreakable intermediate walls
                if (row == 0 or row == self.size - 1) or (column == 0 or column == self.size - 1):
                    empty_field[row][column] = Field.unbreakable_boundary_wall_id  # boundary walls TODO поменять 1 и 2
        return empty_field

    def find_init_breakable_walls_coord(self) -> List:
        breakable_walls_coord = []
        for row in range(self.size):
            for column in range(self.size):
                if not self.empty_field[row][column] and [row, column] not in PLAYER_INIT_POSITIONS:
                    if random.random() < self.p_walls:
                        breakable_walls_coord.append([row, column])
        breakable_walls_coord.sort()
        return breakable_walls_coord

    def find_monsters_available_cells(self) -> List[List[int]]:
        monster_available_cells = []
        for row in range(self.size):
            for column in range(self.size):
                if self.field[row][column] == 0 and [row, column] not in PLAYER_INIT_POSITIONS:
                    monster_available_cells.append([row, column])
        return monster_available_cells

    def find_init_penetrable_cells_coord(self) -> List[List[int]]:
        penetrable_cells_coord = []
        for row in range(self.size):
            for column in range(self.size):
                if self.field[row][column] in PENETRABLE_OBJECTS:
                    penetrable_cells_coord.append([row, column])
        penetrable_cells_coord_sorted = [list(x) for x in sorted(set([tuple(y) for y in penetrable_cells_coord]))]
        return penetrable_cells_coord_sorted

    def find_empty_cells(self) -> List[List[int]]:
        empty_cells_coord = []
        for row in range(self.size):
            for column in range(self.size):
                if self.field[row][column] == 0:
                    empty_cells_coord.append([row, column])
        return empty_cells_coord

    def check_if_refractory(self, my_bombs: List[Bomb]) -> bool:
        if len(my_bombs) > self.max_bombs_number:  # TODO: checkpoint
            print('error line 98 file player')
        if len(my_bombs) == self.max_bombs_number:
            return True
        return False

    def put_player_and_monsters(self, player: Player, monster_list: List[Monster]) -> List[Monster]:
        self.field = deepcopy(self.empty_field)
        self.field[player.row_init][player.column_init] = Player.id
        for monster in monster_list:
            self.field[monster.row][monster.column] = monster.id
        return monster_list

    def visualize(self):
        print()
        # border
        print(4 * ' ', end='')
        for size in range(self.size):
            print(size, end=2 * ' ')
        print()
        for row in range(self.size):
            # border
            if row < 10:
                string = str(row) + ' '
            else:
                string = str(row)
            # field visualization
            for column in range(self.size):
                cell = self.field[row][column]
                string = string + 2 * ' ' + SYMBOLS[cell]
            print(string)  # field
        print()
