import random
from typing import List

from configurations import LEVEL_CONSTANTS, PLAYER_INIT_COORD
from game import Game
from wall import BoundaryWall, BreakableWall, IntermediateWall, Wall


class Field:
    def __init__(self):
        self.size = LEVEL_CONSTANTS['size']
        self.p_walls = LEVEL_CONSTANTS['p_walls']
        self.max_bomb_number = LEVEL_CONSTANTS['max_bomb_num']
        self.max_bomb_reached = False
        self.breakable_wall_coord = []
        self.non_breakable_wall_coord = []
        self.empty = []
        self.main = []

    def add_wall(self, wall_type, row, column, game: Game):
        wall = wall_type(row, column)
        self.empty[row][column].append(wall)
        game.bound_walls.append(wall) if isinstance(wall, BoundaryWall) else game.inter_walls.append(wall)

    def create_field_with_non_breakable_walls(self, game: Game):
        self.empty = [[[] for _1 in range(self.size)] for _2 in range(self.size)]
        for row in range(self.size):
            for column in range(self.size):
                if (row in (0, self.size - 1)) or (column in (0, self.size - 1)):
                    self.add_wall(BoundaryWall, row, column, game)
                elif row % 2 == column % 2 == 0:
                    self.add_wall(IntermediateWall, row, column, game)
        game.non_breakable_walls = game.bound_walls + game.inter_walls
        self.non_breakable_wall_coord = [[wall.row, wall.column] for wall in game.non_breakable_walls]

    def create_breakable_walls(self, game) -> None:
        for row in range(self.size):
            for column in range(self.size):
                if not (self.empty[row][column] or [row, column] in PLAYER_INIT_COORD):
                    if random.random() < self.p_walls:
                        game.breakable_walls.append(BreakableWall(row, column))
                        self.breakable_wall_coord.append([row, column])

    def find_init_penetrable_cell_coord(self) -> List[List[int]]:
        penetrable_cell_coord = []
        for row in range(self.size):
            for column in range(self.size):
                if not self.main[row][column] or all(some_object.penetrable for some_object in self.main[row][column]):
                    penetrable_cell_coord.append([row, column])
        return penetrable_cell_coord

    def find_monster_available_cells(self, game) -> List[List[int]]:
        monster_available_cells = []
        lst = [[obj.row, obj.column] for obj in game.objects]
        for row in range(self.size):
            for column in range(self.size):
                if [row, column] not in (lst + PLAYER_INIT_COORD):
                    monster_available_cells.append([row, column])
        return monster_available_cells
