from abc import abstractmethod
from random import choice
from typing import List

from any_object import LivingObject
from configurations import COORD_VARS, DIR_VARS
from field import Field
from game_objects import Game


class Monster(LivingObject):
    def __init__(self, row, column, direction):
        super().__init__(row, column)
        # coord
        self.previous_row = None
        self.previous_column = None
        self.dir = direction

    def make_move(self,
                  field: Field,
                  game: Game,
                  step: int,
                  player_won: bool,
                  player_lost: bool,
                  ) -> None:
        self.previous_row, self.previous_column = self.row, self.column
        self.move(field=field, game=game, step=step)
        if not player_won:
            monster_eats_player(self, game)

    @abstractmethod
    def move(self, field: Field, game: Game, step: int):
        pass


class MonsterHexamoebo(Monster):
    def __init__(self, row, column, direction):
        super().__init__(row, column, direction)

    def move(self, field: Field, game: Game, step: int) -> None:
        if step % 2 == 0:
            random_move(self, game)


class MonsterDog(Monster):
    p_turn = 0.9

    def __init__(self, row, column, direction):
        super().__init__(row, column, direction)

    def move(self, field: Field, game: Game, step: int) -> None:
        available_directions = find_available_directions(self, game)
        if self.dir in range(4):  # defined direction
            if self.dir in [variant[2] for variant in available_directions]:
                straight_move(self, available_directions)
            else:
                random_move(self, game)
        else:  # undefined direction
            random_move(self, game)


def random_move(monster: Monster, game: Game) -> None:
    direction_variants = find_available_directions(monster, game)
    if direction_variants:
        monster.row, monster.column, monster.dir = choice(direction_variants)
    else:
        monster.dir = DIR_VARS['no_way']


def find_available_directions(monster: Monster, game: Game) -> List[List[int]]:
    direction_variants = []
    for coord in COORD_VARS[0:4]:
        if [monster.row + coord[0], monster.column + coord[1]] in game.penetrable_cell_coord:
            direction_variants.append([monster.row + coord[0], monster.column + coord[1], COORD_VARS.index(coord)])
    return direction_variants


def straight_move(monster: Monster, available_directions: List) -> None:
    if len(available_directions) <= 2:
        monster.row += COORD_VARS[monster.dir][0]
        monster.column += COORD_VARS[monster.dir][1]
    else:
        do_casual_turn(monster, available_directions)


def do_casual_turn(monster: Monster, available_directions: List) -> None:
    direction = monster.dir
    reverse_direction = invert_direction(direction)
    monster_coord = choice([variant for variant in available_directions if variant[2] != reverse_direction])
    monster.row, monster.column, monster.dir = monster_coord


def invert_direction(direction: int) -> int:
    return (direction + 2) % 4
    # return direction+2 if (3 >= direction+2 >= 0) else direction-2


def monster_eats_player(monster: Monster, game: Game) -> None:
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
