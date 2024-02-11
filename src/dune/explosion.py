from configurations import EXPLOSIBLE_OBJECTS, OBJECTS_TO_STOP_EXPLOSION
from copy import deepcopy
from configurations import OBJECTS_TO_STOP_EXPLOSION, NON_EXPLOSIBLE_OBJECTS, COORD_VARS


class Explosion:
    explosion_power = 3  # min = 2

    def __init__(self, field, bomb):
        self.id = 8
        self.row_center = bomb.row
        self.column_center = bomb.column
        self.explosion_area = []
        self.walls_to_explode_coord = []
        self.find_explosion_area(field)

    def find_explosion_area(self, field):
        explosion_area = []
        walls_to_explode_coord = []
        for row_dir, column_dir in COORD_VARS[0:4]:
            for power in range(Explosion.explosion_power):
                row_beam, column_beam = self.row_center + row_dir * power, self.column_center + column_dir * power
                if field.field[row_beam][column_beam] == EXPLOSIBLE_OBJECTS[0]:  # breakable_wall
                    walls_to_explode_coord.append([row_beam, column_beam])
                    explosion_area.append((row_beam, column_beam))
                    break
                if field.field[row_beam][column_beam] in OBJECTS_TO_STOP_EXPLOSION:  # unbreakable_wall
                    break
                explosion_area.append((row_beam, column_beam))
        # remove repeats
        self.walls_to_explode_coord = walls_to_explode_coord  # todo проверить не будет ли проблем с прекрытием если циркулярный
        explosion_area = set(explosion_area)
        self.explosion_area = [list(explosion_point) for explosion_point in explosion_area]
        # for explosion_point in explosion_area:

    def kills_player(self, player):
        print('in self.explosion_area', self.explosion_area)
        if player.alive and [player.row, player.column] in self.explosion_area:
            player.kill()
            # print('you are dead due to explosion. game over')

    # def kills_monster(self, monsters_list):
    #     if self.timer == self.lifespan - 1:
    #         dead_monsters = []
    #         for monster in monsters_list:
    #             if [monster.row, monster.column] in self.explosion_area:
    #                 monster.alive = False
    #                 dead_monsters.append(monster)
    #                 print('monster is dead', monster.row, monster.column, monster.name)
    #         for monster in dead_monsters:
    #             monsters_list.remove(monster)

    # def explodes_bomb(self, bombs_list):
    #     if len(bombs_list) >= 2:
    #         first_bomb_timer = bombs_list[0].timer
    #         first_bomb_explosion_area = bombs_list[0].explosion_area
    #         y_first_bomb = bombs_list[0].row
    #         x_first_bomb = bombs_list[0].column
    #         explosed_bomb = []
    #         if first_bomb_timer == self.lifespan - 1:
    #             circular_explosion_area = deepcopy(first_bomb_explosion_area)
    #             circular_explosion_area.remove([y_first_bomb, x_first_bomb])
    #             for power in range(self.explosion_power):
    #                 y_explosion, x_explosion = self.row + 'y_dir' * power, self.column + 'x_dir' * power
    #                 # print('y_explosion, x_explosion', y_explosion, x_exp', breakable_walls_for_removal_coordlosion)
    #                 # if field.field[y_explosion][x_explosion] in OBJECTS_TO_STOP_EXPLOSION:
    #                 #     break
    #                 if [y_explosion, x_explosion] not in self.explosion_area:
    #                     self.explosion_area.append([y_explosion, x_explosion])
    #
    #             # for bomb in bombs_list:
    #             #     if [self.row, self.column] in self.explosion_area:
    #             #         explosed_bomb.append(bomb)
    #             #         print('CEA', circular_explosion_area, 'yx', self.row, self.column)
    #             #         bombs_list.remove(bomb)

    # def explodes_wall(self, field):
    #     if self.timer == self.lifespan:
    #         for wall_coords_to_remove in self.walls_to_explode_coord:
    #             if wall_coords_to_remove in field.breakable_walls_coord:
    #                 field.breakable_walls_coord.remove(wall_coords_to_remove)
    #                 field.penetrable_cells_coord.append(wall_coords_to_remove)
    #         self.walls_to_explode_coord = []
    #     return field.breakable_walls_coord

    def circular_explosion(self, lines, my_bombs):
        if len(my_bombs) >= 2:
            first_bomb_timer = my_bombs[0].timer
            first_bomb_explosion_area = my_bombs[0].explosion_area
            y_first_bomb = my_bombs[0].row
            x_first_bomb = my_bombs[0].column
            if first_bomb_timer == self.lifespan - 1:
                circular_explosion_area = deepcopy(first_bomb_explosion_area)
                circular_explosion_area.remove([y_first_bomb, x_first_bomb])
                print('CEA', circular_explosion_area)

                for counter in range(len(circular_explosion_area)):
                    y, x = circular_explosion_area[counter]
                    if lines.field[self.row][self.column] == 6:
                        for bomb in my_bombs:
                            if y == self.row and x == self.column:
                                self.timer = self.lifespan - 2
            print('cyrk')


