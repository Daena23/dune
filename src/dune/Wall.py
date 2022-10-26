class Wall:
    def __init__(self):
        self.priority = 0
        self.y = 0
        self.x = 0
        self.can_player_pass = False
        self.can_monster_pass = False

class Boundary_Wall(Wall):
    def __init__(self):
        super().__init__()
        self.print_symbol = '#'
        self.y = 0
        self.x = 0
        self.can_player_pass = False
        self.can_monster_pass = False
        self.stop_explosion = True

class Unbreakable_Wall(Wall):
    def __init__(self):
        super().__init__()
        self.print_symbol = '#'
        self.priority = 0
        self.can_player_pass = False
        self.can_monster_pass = False
        self.stop_explosion = True
        self.explosible = False

class Breakable_Wall(Wall):
    def __init__(self):
        super().__init__()
        self.print_symbol = '+'
        self.priority = 1
        self.can_player_pass = False
        self.can_monster_pass = False
        self.stop_explosion = False
        self.explosible = True