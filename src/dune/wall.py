from any_object import NonLivingObject


class Wall(NonLivingObject):
    def __init__(self, row, column):
        super().__init__()
        # coord
        self.row = row
        self.column = column
        # properties
        self.penetrable = False


class BoundaryWall(Wall):
    pass


class IntermediateWall(Wall):
    pass


class BreakableWall(Wall):
    def __init__(self, row, column):
        super().__init__(row, column)
