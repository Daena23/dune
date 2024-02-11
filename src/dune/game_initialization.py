import random
from random import choice

from dune.src.dune.bomb import Bomb
from field import Field
from copy import deepcopy
from player import Player
from monster import MonsterDog, MonsterНexamoebo
from portal import Portal
from explosion import Explosion


def initialize_game(field):
    # put breakable walls
    field.field = deepcopy(field.empty_field)
    field.breakable_walls_coord = field.find_init_breakable_walls_coord()
    for row, column in field.breakable_walls_coord:
        field.field[row][column] = Field.breakable_wall_id
    # create objects
    monsters_list = create_monsters(field)
    player = Player()
    # bomb = Bomb()
    bombs_list = []
    explosions_list = []
    new_bomb = []
    portal = Portal()
    put_living_things(field, player, monsters_list)
    field.visualize()
    return player, monsters_list, bombs_list, portal, explosions_list, new_bomb


def find_monsters_init_coord(field):
    n_monsters = 1  # random.randint(2, int(len(field.find_monsters_available_cells()) / field.size))
    init_monsters_description = []
    for counter in range(n_monsters):
        row_coord, column_coord = choice(field.find_monsters_available_cells())
        init_monsters_description.append([row_coord, column_coord])
    init_monsters_description.sort()
    return init_monsters_description


def create_monsters(field):
    init_monsters_coord = find_monsters_init_coord(field)
    my_monsters = []
    for monster_description in init_monsters_coord:
        monster = MonsterDog() if random.random() > 0.5 else MonsterНexamoebo()  # TODO: change if add monster types
        monster.row, monster.column = monster_description
        monster.dir, monster.is_alive = 5, True
        my_monsters.append(monster)
    return my_monsters


def put_living_things(field, player, my_monsters):
    field.field[player.row_init][player.column_init] = player.id
    for monster in my_monsters:
        field.field[monster.row][monster.column] = monster.id
