import random
from copy import deepcopy
from random import choice
from typing import List, Tuple

from bomb import Bomb
from explosion import Explosion
from field import Field
from monster import Monster, MonsterDog, MonsterHexamoebo
from player import Player


def initialize_game(field: Field) -> Tuple[Player, List[Monster], List[Bomb], List[Explosion]]:
    # put breakable walls
    field.field = deepcopy(field.empty_field)
    field.breakable_walls_coord = field.find_init_breakable_walls_coord()
    for row, column in field.breakable_walls_coord:
        field.field[row][column] = Field.breakable_wall_id
    # create objects
    monster_list = create_monsters(field)
    player = Player()
    bomb_list = []
    explosion_list = []
    put_living_things(field, player, monster_list)
    field.penetrable_cells_coord = field.find_init_penetrable_cells_coord()
    field.visualize()
    return player, monster_list, bomb_list, explosion_list


def find_monsters_init_coord(field: Field) -> List[List[int]]:
    n_monsters = 1  # random.randint(2, int(len(field.find_monsters_available_cells()) / field.size))
    init_monsters_description = []
    for counter in range(n_monsters):
        row_coord, column_coord = choice(field.find_monsters_available_cells())
        init_monsters_description.append([row_coord, column_coord])
    init_monsters_description.sort()
    return init_monsters_description


def create_monsters(field: Field) -> List[Monster]:
    init_monsters_coord = find_monsters_init_coord(field)
    monster_list = []
    for monster_description in init_monsters_coord:
        monster = MonsterDog() if random.random() > 0.5 else MonsterHexamoebo()  # TODO: change if add monster types
        monster.row, monster.column = monster_description
        monster.dir, monster.alive = 5, True
        monster_list.append(monster)
    return monster_list


def put_living_things(field: Field, player: Player, monster_list: List[Monster]):
    field.field[player.row_init][player.column_init] = player.id
    for monster in monster_list:
        field.field[monster.row][monster.column] = monster.id
