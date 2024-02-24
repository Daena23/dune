from abc import abstractmethod
from random import choice
from typing import List

from any_object import LivingObject
from configurations import COORD_VARS, DIR_VARS
from field import Field
from game_objects import Game


class Monster(LivingObject):
    def __init__(self, row, column, dir):
        super().__init__(row, column)
        # coord
        self.previous_row = None
        self.previous_column = None
        self.dir = dir

    def make_move(self, field, game, step, player_won, player_lost) -> None:
        self.previous_row, self.previous_column = self.row, self.column
        self.move(field=field, game=game, step=step)
        if not player_won:
            monster_eats_player(self, game)

    @abstractmethod
    def move(self, field, game, step):
        pass


class MonsterHexamoebo(Monster):
    def __init__(self, row, column, dir):
        super().__init__(row, column, dir)

    def move(self, field: Field, game: Game, step: int):
        if step % 2 == 0:
            random_move(self, game)


class MonsterDog(Monster):
    p_turn = 0.9

    def __init__(self, row, column, dir):
        super().__init__(row, column, dir)

    def move(self, field: Field, game: Game, step: int):
        available_directions = find_available_directions(self, game)
        if self.dir in range(4):  # defined direction
            if self.dir in [variant[2] for variant in available_directions]:
                straight_move(self, available_directions)
            else:
                random_move(self, game)
        else:  # undefined direction
            random_move(self, game)


def random_move(monster: Monster, game: Game):
    direction_variants = find_available_directions(monster, game)
    if direction_variants:
        monster.row, monster.column, monster.dir = choice(direction_variants)
    else:
        monster.dir = DIR_VARS['no_way']


def find_available_directions(monster: Monster, game: Game):
    direction_variants = []
    for coord in COORD_VARS[0:4]:
        if [monster.row + coord[0], monster.column + coord[1]] in game.penetrable_cell_coord:
            direction_variants.append([monster.row + coord[0], monster.column + coord[1], COORD_VARS.index(coord)])
    return direction_variants


def straight_move(monster: Monster, available_directions: List):
    if len(available_directions) <= 2:
        monster.row += COORD_VARS[monster.dir][0]
        monster.column += COORD_VARS[monster.dir][1]
    else:
        do_casual_turn(monster, available_directions)


def do_casual_turn(monster: Monster, available_directions: List):
    direction = monster.dir
    reverse_direction = invert_direction(direction)
    monster_coord = choice([variant for variant in available_directions if variant[2] != reverse_direction])
    monster.row, monster.column, monster.dir = monster_coord


def invert_direction(direction: int):
    return (direction + 2) % 4
    # return direction+2 if (3 >= direction+2 >= 0) else direction-2


def monster_eats_player(monster: Monster, game: Game):
    condition1 = (monster.row, monster.column) == (game.player.row, game.player.column)
    condition2 = (monster.row, monster.column) == (game.player.previous_row, game.player.previous_column)
    condition3 = (monster.previous_row, monster.previous_column) == (game.player.row, game.player.column)
    eating_conditions = [condition1, condition2 and condition3]
    if game.player.exists and any(eating_conditions):  # and not game.player.won:
        game.player.kill()

# class LazyMonster(Monster):
#     def __init__(self):
#         super().__init__()
#
#     def move(self, field, step: int):
#         pass


# class TuckerCarlson(Monster):
#     putin_detection_range = 3
#
#     def __init__(self):
#         super().__init__()
#         self.id = 77
#
#     def move(self, field, step: int) -> None:
#         carlson_x = self.row
#         carlson_y = self.column
#
#         putin_x, putin_y = None, None
#         for y, row in enumerate(field.field):
#             if Player.id in row:
#                 putin_x, putin_y = row.index(Player.id), y
#                 break
#
#         if putin_x is None and putin_y is None:
#             random_move(self, field)
#
#         dx = putin_x - carlson_x
#         dy = putin_y - carlson_y
#
#         if dx ** 2 + dy ** 2 <= self.putin_detection_range ** 2:
#             move_options = []
#             if dx != 0:
#                 dx_carlson = 1 if dx < 0 else -1
#                 if field.field[self.row + dx_carlson][self.column] in PENETRABLE_OBJECTS:
#                     move_options.append((self.row + dx_carlson, self.column))
#             if dy != 0:
#                 dy_carlson = 1 if dy < 0 else -1
#                 if field.field[self.row][self.column + dy_carlson] in PENETRABLE_OBJECTS:
#                     move_options.append((self.row, self.column + dy_carlson))
#             if move_options:
#                 self.row, self.column = choice(move_options)
#         else:
#             random_move(self, field)

