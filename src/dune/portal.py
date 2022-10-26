from random import choice
from utils import COORDINATE_VARIANTS
import random
from monster import MonsterDog
from monster import MonsterCat


class Portal:
    def __init__(self):
        super().__init__()
        self.print_symbol = 'O'
        self.priority = 0
        self.portal_exists = False
        self.closed_by_wall = True
        self.y = 0
        self.x = 0
        self.can_player_pass = True
        self.can_monster_pass = True
        self.stop_explosion = False
        self.explosible = False
        self.ignored_explosions = []

    def portal_appearance(self, field, all_monsters):
        if len(all_monsters) == 0 and not self.portal_exists:
            self.portal_exists = True
            if len(field.breakable_walls_coord) > 0:
                portal_coord = choice(field.breakable_walls_coord)
            else:
                portal_coord = choice(field.penetrable_cells_coord)
                self.closed_by_wall = False
            self.y, self.x = portal_coord
            field.field[self.y][self.x].append(self)
            print('yx port', self.y, self.x)

    def monster_creation_after_explosion(self, field, all_monsters):
        n_monster_after_explosion = 1
        for monster_counter in range(n_monster_after_explosion):
            monster_description = [self.y, self.x, 'undefined', True]
            monster_rand = random.randint(0, 2)
            if monster_rand > 1:
                monster = MonsterDog()
            else:
                monster = MonsterCat()
            all_monsters.append(monster)
            monster.y_old_coord = monster.y
            monster.x_old_coord = monster.x
            monster.y, monster.x, monster.direction, monster.is_alive = monster_description
        for monster in all_monsters:
            field.field[monster.y][monster.x].append(monster)
