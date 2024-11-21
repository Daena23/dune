import random
from copy import deepcopy
from typing import Tuple

from configurations import LEVEL_CONSTANTS
from field import Field
from game_loop import put_on_field, visualize, create_monster
from game import Game
from player import Player
from portal import Portal


def initialize_game() -> Tuple[Field, Game]:
    field = Field()
    game = Game(Player())
    # Create initial field
    field.create_field_with_non_breakable_walls(game)
    field.main = deepcopy(field.empty)
    # Create and put objects
    field.create_breakable_walls(game)
    game.portal = Portal(field, game)
    init_create_monsters(field, game)
    put_on_field(field, game.objects)
    game.penetrable_cell_coord = field.find_init_penetrable_cell_coord()
    visualize(field, game)
    return field, game


def init_create_monsters(field: Field, game: Game) -> None:
    init_monster_coord = []
    for counter in range(LEVEL_CONSTANTS['init_monster_number']):
        init_monster_coord.append(sorted(random.choice(field.find_monster_available_cells(game))))
    for row, column in init_monster_coord:
        create_monster(game, row, column)
