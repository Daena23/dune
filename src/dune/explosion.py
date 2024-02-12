from typing import List

from bomb import Bomb
from configurations import COORD_VARS, EXPLOSIBLE_OBJECTS, OBJECTS_TO_STOP_EXPLOSION
from field import Field
from monster import Monster
from player import Player


class Explosion:
    explosion_power = 3  # min = 2

    def __init__(self, field, bomb):
        self.id_center = 9
        self.id_corners = 10
        self.id_destroyed = 11
        self.row_center = bomb.row
        self.column_center = bomb.column
        self.explosion_area = []
        self.walls_to_explode_coord = []
        self.find_explosion_area(field)

    def find_explosion_area(self, field: Field):
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
        self.walls_to_explode_coord = walls_to_explode_coord
        explosion_area = set(explosion_area)
        self.explosion_area = [list(explosion_point) for explosion_point in explosion_area]

    def kills_player(self, player: Player, destroyed_objects: List[List[int]]):
        if player.alive and [player.row, player.column] in self.explosion_area:
            player.kill()
            destroyed_objects.append([player.row, player.column])

    def kills_monster(self, monster_list: List[Monster], destroyed_objects: List):
        for monster in monster_list:
            if [monster.row, monster.column] in self.explosion_area:
                monster.alive = False
                destroyed_objects.append([monster.row, monster.column])
        #         print('monster is dead', monster.row, monster.column)
        # monster_list[:] = [monster for monster in monster_list if not monster.alive]

    @staticmethod
    def explodes_wall(field: Field, explosion_list: List, destroyed_objects: List):
        for explosion in explosion_list:
            for coord in explosion.walls_to_explode_coord:
                if coord in field.breakable_walls_coord:
                    field.breakable_walls_coord.remove(coord)
                    field.penetrable_cells_coord.append(coord)
                    destroyed_objects.append(coord)
        for explosion in explosion_list:
            # if [explosion.row_center, explosion.column_center] in field.penetrable_cells_coord:
            field.penetrable_cells_coord.append([explosion.row_center, explosion.column_center])

    @staticmethod
    def explodes_bomb(bomb_list: List[Bomb], explosion_list: List):
        for explosion in explosion_list:
            for bomb in bomb_list:
                if [bomb.row, bomb.column] in explosion.explosion_area:
                    bomb.timer = Bomb.lifespan
    #
    # def circular_explosion(self, lines, my_bombs):
    #     if len(my_bombs) >= 2:
    #         first_bomb_timer = my_bombs[0].timer
    #         first_bomb_explosion_area = my_bombs[0].explosion_area
    #         y_first_bomb = my_bombs[0].row
    #         x_first_bomb = my_bombs[0].column
    #         if first_bomb_timer == self.lifespan - 1:
    #             circular_explosion_area = deepcopy(first_bomb_explosion_area)
    #             circular_explosion_area.remove([y_first_bomb, x_first_bomb])
    #             print('CEA', circular_explosion_area)
    #
    #             for counter in range(len(circular_explosion_area)):
    #                 y, x = circular_explosion_area[counter]
    #                 if lines.field[self.row][self.column] == 6:
    #                     for bomb in my_bombs:
    #                         if y == self.row and x == self.column:
    #                             self.timer = self.lifespan - 2
    #         print('cyrk')
