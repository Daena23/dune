from configurations import SYMBOLS, ObjectId


class AnyObject:
    def __init__(self):
        obj_type = type(self).__name__
        self.id = getattr(ObjectId, obj_type).value
        self.symbol = SYMBOLS[obj_type]
        # Coordinates
        self.row = None
        self.column = None
        # Properties
        self.penetrable = True
        self.exists = False


class LivingObject(AnyObject):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column
        self.exists = True

    def make_move(
            self,
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
