from random import choice

class Portal:
    def __init__(self):
        self.portal_exists = False
        self.y = 0
        self.x = 0
        self.id = 10

    def portal_appearance(self, lines, my_monsters):
        if len(my_monsters) == 0 and not self.portal_exists:
            self.portal_exists = True
            portal_coord = choice(lines.penetrable_cell_coord)
            print('port', portal_coord)
            self.y, self.x = portal_coord
            lines.field[self.y][self.x] = self.id