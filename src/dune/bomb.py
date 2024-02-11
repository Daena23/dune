from configurations import EXPLOSIBLE_OBJECTS, OBJECTS_TO_STOP_EXPLOSION
from copy import deepcopy


class Bomb:
    lifespan = 3

    def __init__(self):
        self.id = 7
        self.exists = True
        self.row = None
        self.column = None
        self.timer = 0
        self.suppl_bomb_coord = []

    def exploding(self):
        return self.timer == Bomb.lifespan

    # def is_not_passable(self, field):
    #     # if self.timer == 1 and [self.row, self.column] in field.penetrable_cells_coord:
    #     # if [self.row, self.column] in field.penetrable_cells_coord():
    #     print(field.find_penetrable_cells_coord())
    #     print(self.row, self.column)
    #     field.find_penetrable_cells_coord().remove([self.row, self.column])
    #     # if self.timer == self.lifespan and [self.row, self.column] not in field.penetrable_cells_coord:
    #     #     field.penetrable_cells_coord.append([self.row, self.column])
