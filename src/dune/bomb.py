class Bomb:
    lifespan = 3

    def __init__(self):
        self.id = 8
        self.row = None
        self.column = None
        self.exists = True
        self.timer = 0
        self.exploding = False

    def if_explodes(self):
        return self.timer == Bomb.lifespan
