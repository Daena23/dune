from random import choice


class Portal:
    def __init__(self):
        # self.exists = False
        self.row = None
        self.column = None
        self.id = 10

    def appear(self, field):
        self.row, self.column = choice(field.find_penetrable_cells_coord())

    def player_pass(self, player):
        pass
