from abc import ABC, abstractmethod
from random import choice
from typing import List

from configurations import COORD_VARS, PENETRABLE_OBJECTS
from player import Player


class Monster(ABC):

    def __init__(self):
        self.row = None
        self.column = None
        self.previous_row = None
        self.previous_column = None
        self.dir = 6
        self.alive = True

    @abstractmethod
    def move(self, field, step):
        pass


class MonsterHexamoebo(Monster):
    def __init__(self):
        super().__init__()
        self.id = 6

    def move(self, field, step: int):
        if step % 2 == 0:
            random_move(self, field)


class MonsterDog(Monster):
    p_turn = 0.9

    def __init__(self):
        super().__init__()
        self.id = 7

    def move(self, field, step: int):
        available_directions = find_available_directions(self, field)
        if self.dir in range(4):  # defined direction
            if self.dir in [variant[2] for variant in available_directions]:
                straight_move(self, available_directions)
            else:
                random_move(self, field)
        else:  # undefined direction
            random_move(self, field)


class LazyMonster(Monster):
    def __init__(self):
        super().__init__()
        self.id = 6

    def move(self, field, step: int):
        pass


class TuckerCarlson(Monster):
    putin_detection_range = 3

    def __init__(self):
        super().__init__()
        self.id = 77

    def move(self, field, step: int) -> None:
        carlson_x = self.row
        carlson_y = self.column

        putin_x, putin_y = None, None
        for y, row in enumerate(field.field):
            if Player.id in row:
                putin_x, putin_y = row.index(Player.id), y
                break

        if putin_x is None and putin_y is None:
            random_move(self, field)

        dx = putin_x - carlson_x
        dy = putin_y - carlson_y

        if dx ** 2 + dy ** 2 <= self.putin_detection_range ** 2:
            move_options = []
            if dx != 0:
                dx_carlson = 1 if dx < 0 else -1
                if field.field[self.row + dx_carlson][self.column] in PENETRABLE_OBJECTS:
                    move_options.append((self.row + dx_carlson, self.column))
            if dy != 0:
                dy_carlson = 1 if dy < 0 else -1
                if field.field[self.row][self.column + dy_carlson] in PENETRABLE_OBJECTS:
                    move_options.append((self.row, self.column + dy_carlson))
            if move_options:
                self.row, self.column = choice(move_options)
        else:
            random_move(self, field)


# monster's move functions
def random_move(monster: Monster, field):
    direction_variants = find_available_directions(monster, field)
    if direction_variants:
        monster.row, monster.column, monster.dir = choice(direction_variants)
    else:
        monster.dir = 4


def find_available_directions(monster: Monster, field):
    direction_variants = []
    for coord in COORD_VARS[0:4]:
        if [monster.row + coord[0], monster.column + coord[1]] in field.find_init_penetrable_cells_coord():
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


def monster_eats_player(player: Player, monster: Monster):
    condition1 = (monster.row, monster.column) == (player.row, player.column)
    condition2 = (monster.row, monster.column) == (player.previous_row, player.previous_column)
    condition3 = (monster.previous_row, monster.previous_column) == (player.row, player.column)
    eating_conditions = [condition1, condition2 and condition3]
    if player.alive and any(eating_conditions):
        player.kill()
