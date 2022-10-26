from utils import COORDINATE_VARIANTS
from copy import deepcopy
from explosion import Explosion
from field import Field
from grave import Grave




class Bomb:
    def __init__(self):
        self.print_symbol = 'B'
        self.priority = 4
        self.bomb_exist = False
        self.y = 0
        self.x = 0
        self.timer = 0
        self.explosion_area = []
        self.explosion_time = 5
        self.explosion_power = 3
        self.walls_to_explode_coord = []
        self.suppl_bomb_coord = []
        self.can_player_pass = False
        self.can_monster_pass = False
        self.stop_explosion = False
        self.explosible = False


    def get_affected_by_explosion(self):
        ...

    def bomb_explosion_area_ident(self, field):
        self.explosion_area.append([self.y, self.x])
        for direction_id in range(len(COORDINATE_VARIANTS)):
            y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
            break_condition = False
            for power in range(self.explosion_power):
                y_explosion, x_explosion = self.y + y_dir * power, self.x + x_dir * power
                cell_items = field.field[y_explosion][x_explosion]
                if len(cell_items) == 0:
                    self.explosion_area.append([y_explosion, x_explosion])
                else:
                    for cell_item in cell_items:
                        # unbreakable wall
                        if cell_item.stop_explosion:
                            break_condition = True
                        # breakable wall
                        elif cell_item.explosible:
                            self.explosion_area.append([y_explosion, x_explosion])
                            break_condition = True
                        else:
                            self.explosion_area.append([y_explosion, x_explosion])
                if break_condition:
                    break
        self.explosion_area = [list(x) for x in sorted(set([tuple(y) for y in self.explosion_area]))]
        return self.explosion_area

    def explosions_list_update(self, field, all_bombs, all_explosions):
        if self.explosion_time <= self.timer:
            for counter in range(len(self.explosion_area)):
                y, x = self.explosion_area[counter]
                explosion = Explosion(x, y)
                all_explosions.append(explosion)
                field.field[y][x].append(explosion)
            field.field[self.y][self.x].remove(self)
            all_bombs.remove(self)
            field.penetrable_cells_coord.append([self.y, self.x])
