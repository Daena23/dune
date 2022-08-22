from utils import COORDINATE_VARIANTS, EXPLOSIBLE_OBJECTS, OBJECTS_TO_STOP_EXPLOSION
from copy import deepcopy


class Bomb:
    def __init__(self):
        self.id = 6
        self.explosion_id = 7
        self.bomb_exist = False
        self.y = 0
        self.x = 0
        self.timer = 0
        self.explosion_area = []
        self.explosion_time = 4
        self.walls_to_explode_coord = []
        self.explosion_power = 3
        self.max_bombs_n = 3
        self.suppl_bomb_coord = []

    def bomb_is_not_passable(self, lines):
        if self.timer == 1 and [self.y, self.x] in lines.penetrable_cell_coord:
            lines.penetrable_cell_coord.remove([self.y, self.x])
        if self.timer == self.explosion_time and [self.y, self.x] not in lines.penetrable_cell_coord:
            lines.penetrable_cell_coord.append([self.y, self.x])

    def bomb_explosion_area_ident(self, lines):
        self.explosion_area.append([self.y, self.x])
        for direction_id in range(len(COORDINATE_VARIANTS)):
            y_dir, x_dir, dir_name = COORDINATE_VARIANTS[direction_id]
            for power in range(self.explosion_power):
                y_explosion, x_explosion = self.y + y_dir * power, self.x + x_dir * power
                # print('y_explosion, x_explosion', y_explosion, x_exp', breakable_walls_for_removal_coordlosion)
                if lines.field[y_explosion][x_explosion] in OBJECTS_TO_STOP_EXPLOSION:
                    break
                if [y_explosion, x_explosion] not in self.explosion_area:
                    self.explosion_area.append([y_explosion, x_explosion])
                if lines.field[y_explosion][x_explosion] == EXPLOSIBLE_OBJECTS[4]:
                    self.suppl_bomb_coord.append([y_explosion, x_explosion])
                   #  print('SUPPL_coord', self.suppl_bomb_coord)
                if lines.field[y_explosion][x_explosion] == EXPLOSIBLE_OBJECTS[1]:
                    self.walls_to_explode_coord.append([y_explosion, x_explosion])
                    break
        return self.explosion_area

    def bomb_kills_player(self, player):
        if player.is_alive and self.timer == self.explosion_time - 1 and [player.y_player,
                                                                          player.x_player] in self.explosion_area:
            player.player_dead()
            print('you are dead due to explosion. game over')

    def bomb_kills_monster(self, my_monsters):
        if self.timer == self.explosion_time - 1:
            dead_monsters = []
            for monster in my_monsters:
                if [monster.y_monster, monster.x_monster] in self.explosion_area:
                    monster.is_alive = False
                    dead_monsters.append(monster)
                    print('monster is dead', monster.y_monster, monster.x_monster, monster.name)
            for monster in dead_monsters:
                my_monsters.remove(monster)

    def bomb_explodes_bomb(self, my_bombs):
        if len(my_bombs) >= 2:
            first_bomb_timer = my_bombs[0].timer
            first_bomb_explosion_area = my_bombs[0].explosion_area
            y_first_bomb = my_bombs[0].y
            x_first_bomb = my_bombs[0].x
            explosed_bomb = []
            if first_bomb_timer == self.explosion_time - 1:
                circular_explosion_area = deepcopy(first_bomb_explosion_area)
                circular_explosion_area.remove([y_first_bomb, x_first_bomb])
                for power in range(self.explosion_power):
                    y_explosion, x_explosion = self.y + y_dir * power, self.x + x_dir * power
                    # print('y_explosion, x_explosion', y_explosion, x_exp', breakable_walls_for_removal_coordlosion)
                    if lines.field[y_explosion][x_explosion] in OBJECTS_TO_STOP_EXPLOSION:
                        break
                    if [y_explosion, x_explosion] not in self.explosion_area:
                        self.explosion_area.append([y_explosion, x_explosion])

                for bomb in my_bombs:
                    if [self.y, self.x] in self.explosion_area:
                        explosed_bomb.append(bomb)
                        print('CEA', circular_explosion_area, 'yx', self.y, self.x)
                        my_bombs.remove(bomb)

    def wall_explosion(self, lines):
        if self.timer == self.explosion_time:
            for wall_coords_to_remove in self.walls_to_explode_coord:
                if wall_coords_to_remove in lines.breakable_walls_coord:
                    lines.breakable_walls_coord.remove(wall_coords_to_remove)
                    lines.penetrable_cell_coord.append(wall_coords_to_remove)
            self.walls_to_explode_coord = []
        return lines.breakable_walls_coord

    def circular_explosion(self, lines, my_bombs):
        if len(my_bombs) >= 2:
            first_bomb_timer = my_bombs[0].timer
            first_bomb_explosion_area = my_bombs[0].explosion_area
            y_first_bomb = my_bombs[0].y
            x_first_bomb = my_bombs[0].x
            if first_bomb_timer == self.explosion_time - 1:
                circular_explosion_area = deepcopy(first_bomb_explosion_area)
                circular_explosion_area.remove([y_first_bomb, x_first_bomb])
                print('CEA', circular_explosion_area)

                for counter in range(len(circular_explosion_area)):
                    y, x = circular_explosion_area[counter]
                    if lines.field[self.y][self.x] == 6:
                        for bomb in my_bombs:
                            if y == self.y and x == self.x:
                                self.timer = self.explosion_time - 2
            print('cyrk')
