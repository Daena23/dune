from typing import List

from any_object import NonLivingObject
from configurations import SYMBOLS
from dune.src.dune.field import Field
from game_objects import Game
import random


class Portal(NonLivingObject):
    def __init__(self, field, game):
        super().__init__()
        self.activated = False
        self.row, self.column = self.find_init_coord(field, game)

    def check_win_condition(self, game: Game):
        if self.activated and (self.row, self.column) == (game.player.row, game.player.column):
            self.symbol = SYMBOLS['UsedPortal']
            return True
        return False

    def find_init_coord(self, field: Field, game: Game) -> List[int]:
        if game.breakable_walls:
            location = random.choice(game.breakable_walls)
            coord = [location.row, location.column]
        else:
            coord = random.choice(self.find_empty_cell_coord(field, game))
        return coord

    @staticmethod
    def find_empty_cell_coord(field: Field, game: Game) -> List[List[int]]:
        lst = [[obj.row, obj.column] for obj in game.get_objects()]
        for row in range(field.size):
            empty_cell_coord = [[row, column]for column in range(field.size) if [row, column] not in lst]
        return empty_cell_coord

