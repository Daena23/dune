import random
from copy import deepcopy
from typing import Tuple

from configurations import DIR_VARS, LEVEL_CONSTANTS
from field import Field
from game_loop import put_on_field, visualize
from game_objects import Game
from monster import MonsterDog, MonsterHexamoebo
from player import Player
from portal import Portal


def initialize_game() -> Tuple[Field, Game]:
    field = Field()
    game = Game(Player())
    # create initial field
    field.empty_field = field.create_field_with_non_breakable_walls(game)
    field.field = deepcopy(field.empty_field)
    # create and put objects
    field.create_breakable_walls(game)
    game.portal = Portal(field, game)
    init_create_monsters(field, game)
    put_on_field(field, game.get_objects())
    game.penetrable_cell_coord = field.find_init_penetrable_cell_coord()
    visualize(field, game)
    return field, game


def init_create_monsters(field: Field, game: Game) -> None:
    init_monster_coord = []
    for counter in range(LEVEL_CONSTANTS['n_mon']):
        init_monster_coord.append(sorted(random.choice(field.find_monster_available_cells(game))))
    for row, column in init_monster_coord:
        create_a_monster(game, row, column)


def create_new_monsters(game: Game) -> None:
    if game.create_new_monsters:
        for counter in range(LEVEL_CONSTANTS['n_mon_from_portal']):
            create_a_monster(game, game.portal.row, game.portal.column)
    game.create_new_monsters = False


def create_a_monster(game: Game, row: int, column: int) -> None:
    if random.random() > 0.5:
        game.monsters.append(MonsterDog(row, column, DIR_VARS['undefined']))
    else:
        game.monsters.append(MonsterHexamoebo(row, column, DIR_VARS['undefined']))
