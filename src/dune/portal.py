import random
from typing import List

from any_object import NonLivingObject
from configurations import SYMBOLS, ObjectId
from field import Field
from game import Game


class Portal(NonLivingObject):
    def __init__(self, field: Field, game: Game):
        super().__init__()
        self.activated = False
        self.row, self.column = self.find_init_coord(field, game)
        self.id = ObjectId.PortalDeactivated.value
        self.is_under_explosion = False

    def check_if_win(self, game: Game) -> bool:
        if (self.row, self.column) == (game.player.row, game.player.column):
            self.symbol = SYMBOLS['UsedPortal']
            return True
        return False

    def deactivate(self) -> None:
        if self.activated:
            self.activated = False
            self.id = ObjectId.PortalDeactivated.value

    def activate(self) -> None:
        self.activated = True
        self.id = ObjectId.Portal.value


    def find_init_coord(self, field: Field, game: Game) -> List[int]:
        if game.breakable_walls:
            location = random.choice(game.breakable_walls)
            coord = [location.row, location.column]
        else:
            coord = random.choice(self.find_empty_cell_coord(field, game))
        return coord

    @staticmethod
    def find_empty_cell_coord(field: Field, game: Game) -> List[List[int]]:
        object_coord = [[obj.row, obj.column] for obj in game.objects]
        empty_cell_coord = []
        for row in range(field.size):
            empty_cell_coord = [[row, column]for column in range(field.size) if [row, column] not in object_coord]
        return empty_cell_coord
