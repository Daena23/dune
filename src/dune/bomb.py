from any_object import AnyObject
from configurations import LEVEL_CONSTANTS


class Bomb(AnyObject):
    def __init__(self, row, column):
        super().__init__()
        # coord
        self.row = row
        self.column = column
        # properties
        self.exists = True
        self.timer = 0
        self.penetrable = False

    def exploding(self):
        return self.timer == LEVEL_CONSTANTS['bomb_lifetime']
