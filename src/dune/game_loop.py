import time
from copy import deepcopy
from typing import List, Tuple, Union

from configurations import EVENTS_PUT_BOMB
from dune.src.dune.bomb import Bomb
from explosion import Explosion
from field import Field
from monster import Monster, monster_eats_player
from player import Player
from portal import Portal


def update_player(field: Field, player: Player, bomb_list: List):
    if player.alive and not player.won:
        event = player.command(field)
        player.move(field, event)
        if event in EVENTS_PUT_BOMB and not field.check_if_refractory(bomb_list):
            player.creating_bomb = True
    elif not player.alive:
        player.id = Player.dead_id  # dead(postmortem_steps)
    else:
        player.id = Player.win_id


def update_bombs(field: Field,
                 player: Player,
                 bomb_list: List[Bomb],
                 ) -> List[Explosion]:
    explosion_list = []
    if player.creating_bomb:
        bomb = Bomb()
        bomb.row, bomb.column = player.previous_row, player.previous_column
        bomb_list.append(bomb)
        player.creating_bomb = False
    for bomb in bomb_list:
        bomb.exploding = bomb.if_explodes()
        if bomb.exploding:
            explosion_list.append(Explosion(field, bomb))
        bomb.timer += 1
    bomb_list[:] = [bomb for bomb in bomb_list if not bomb.exploding]
    for bomb in bomb_list:
        field.field[bomb.row][bomb.column] = bomb.id
    return explosion_list


def update_walls(field: Field, bomb_list: List[Bomb]):
    for bomb in bomb_list:
        if [bomb.row, bomb.column] in field.penetrable_cells_coord:
            field.penetrable_cells_coord.remove([bomb.row, bomb.column])


def update_monsters(field: Field, player: Player, monster_list: List[Monster], step: int):
    for monster in monster_list:
        monster.previous_row, monster.previous_column = monster.row, monster.column
        monster.move(field=field, step=step)
        monster_eats_player(player=player, monster=monster)
    monster_list[:] = [monster for monster in monster_list if monster.alive]


def update_explosions(
        field: Field,
        player: Player,
        monster_list: List[Monster],
        bomb_list: List[Bomb],
        explosion_list: List[Explosion],
        ) -> List:
    destroyed_objects = []
    for explosion in explosion_list:
        explosion.kills_player(player, destroyed_objects)
        explosion.kills_monster(monster_list, destroyed_objects)
        explosion.explodes_wall(field, explosion_list, destroyed_objects)
        explosion.explodes_bomb(bomb_list, explosion_list)
        # explodes portal
    return destroyed_objects

#
# def update_path(field: Field, bomb_list: List[Bomb]) -> List[int]:
#     for bomb in bomb_list:
#         if bomb in field.penetrable_cells_coord:
#             field.penetrable_cells_coord.remove([bomb.row, bomb.column])
#     return field.penetrable_cells_coord


def update_portal(field: Field, player: Player, portal: Portal, monster_list: List[Monster]) -> Union[bool, Portal]:
    if not monster_list and portal is None:
        portal = Portal(field)
    if portal:
        if (player.row, player.column) == (portal.row, portal.column):
            portal.id = Portal.portal_used
            player.win()
    return portal


def update_field(field: Field,
                 player: Player,
                 monster_list: List[Monster],
                 bomb_list: List[Bomb],
                 explosion_list: List[Explosion],
                 portal: Portal,
                 player_won: bool,
                 destroyed_objects: List[int],
                 ) -> Field:
    field.field = deepcopy(field.empty_field)
    # put breakable walls
    for row, column in field.breakable_walls_coord:
        field.field[row][column] = field.breakable_wall_id
    # bombs
    for bomb in bomb_list:
        field.field[bomb.row][bomb.column] = bomb.id
    # monsters
    for monster in monster_list:
        field.field[monster.row][monster.column] = monster.id
    # player
    field.field[player.row][player.column] = player.id
    # explosion
    for explosion in explosion_list:
        for row, column in explosion.explosion_area:
            field.field[row][column] = explosion.id_corners
        field.field[explosion.row_center][explosion.column_center] = explosion.id_center
    for row_object, column_object in destroyed_objects:
        field.field[row_object][column_object] = explosion.id_destroyed
    # portal
    if portal is not None:
        field.field[portal.row][portal.column] = portal.id
    # if player_won:
    #     field.field[player.row][player.column] = player.win_id
    return field


def update_loop(player: Player,
                player_lost: bool,
                player_won: bool,
                postmortem_steps: int,
                ) -> Tuple[bool, bool, int]:
    if not player.alive:
        player_lost = True
        postmortem_steps += 1
        time.sleep(0.5)
    if player.won:
        player_won = True
        postmortem_steps = 5
    return player_lost, player_won, postmortem_steps
