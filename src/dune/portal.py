from random import choice


class Portal:
    portal_open = 12
    portal_used = 13

    def __init__(self, field):
        self.id = Portal.portal_open
        self.row, self.column = self.find_init_coord(field)  # choice(field.penetrable_cells_coord)

    @staticmethod
    def find_init_coord(field):
        return choice(field.breakable_walls_coord) if field.breakable_walls_coord else choice(field.find_empty_cells())

        # if field.breakable_walls_coord:
        #     self.row, self.column = choice(field.breakable_walls_coord)
        # else:
        #     self.row, self.column = choice(field.find_empty_cells())
