from auxiliary_func import get_symbol
from configurations import ID_DICT, SYMBOLS


class AnyObject:
    def __init__(self):
        self.id = get_symbol(self, ID_DICT)
        self.symbol = get_symbol(self, SYMBOLS)
        # coord
        self.row = None
        self.column = None
        # properties
        self.penetrable = True
        self.exists = False


class LivingObject(AnyObject):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column
        self.exists = True

    def make_move(self,
                  field,
                  game,
                  step,
                  player_won,
                  player_lost,
                  ) -> None:
        pass


class NonLivingObject(AnyObject):
    def __init__(self):
        super().__init__()
        self.row = None
        self.column = None
        self.exists = True
