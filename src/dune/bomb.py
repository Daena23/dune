from configurations import LEVEL_CONSTANTS
from any_object import AnyObject


class Bomb(AnyObject):
    def __init__(self, row, column):
        super().__init__()
        # self.lifetime = LEVEL_CONSTANTS['bomb_lifetime']
        # coord
        self.row = row
        self.column = column
        # properties
        self.exists = True
        self.timer = 0
        self.explosive = True  # взрывоопасный
        self.penetrable = False
        self.explosible = True
        self.stop_explosion = False

    def exploding(self):
        return self.timer == LEVEL_CONSTANTS['bomb_lifetime']
