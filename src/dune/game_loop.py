import time
from copy import deepcopy
from typing import List

from configurations import EVENTS_PUT_BOMB
from dune.src.dune.bomb import Bomb
from field import Field
from monster import eats_player, monster_death
from player import Player
from portal import Portal
from explosion import Explosion


def update_bombs(field, player, bombs_list):
    explosions_list = []
    if player.creating_bomb:
        bomb = Bomb()
        bomb.row, bomb.column = player.previous_row, player.previous_column
        bombs_list.append(bomb)
        player.creating_bomb = False
    for bomb in bombs_list:
        if bomb.exploding():
            explosions_list.append(Explosion(field, bomb))
            bombs_list.remove(bomb)
        bomb.timer += 1
    return explosions_list


def update_explosions(player, explosions_list):
    for explosion in explosions_list:
        explosion.kills_player(player)
        # self.explodes_wall(field)
        # self.kills_monster(my_monsters)
        # self.explodes_bomb(my_bombs)


def update_player(field, player, bombs_list, postmortem_steps):
    print('pl/al', player.alive, 'pl/dy',  'id', player.id)
    if player.alive:
        if not player.alive:
            pass
        else:
            event = player.command(field)
            player.move(field, event)
            if event in EVENTS_PUT_BOMB and not field.check_if_refractory(bombs_list):
                player.creating_bomb = True
            # if field[player.row][player.column] == Bomb.id:
            #     player.creating_bomb = True
    else:
        player.id = Player.dead_id  # dead(postmortem_steps)


def update_monsters(field: Field, player: Player, my_monsters: List, step: int):
    for monster in my_monsters:
        monster.previous_row, monster.previous_column = monster.row, monster.column
        monster.move(field=field, step=step)
        eats_player(player=player, monster=monster)
    monster_death(monster, my_monsters)


def update_portal(field: Field, my_monsters: List, portal_exists: bool, portal: Portal):
    if not my_monsters and not portal_exists:
        portal.appear(field)
        portal_exists = True
    return portal_exists


def update_field(field, player, monsters_list, bombs_list, explosions_list, portal, portal_exists, player_won):
    field.field = deepcopy(field.empty_field)
    # explode walls
    for explosion in explosions_list:
        for coord in explosion.walls_to_explode_coord:
            if coord in field.breakable_walls_coord:
                field.breakable_walls_coord.remove(coord)
    # put breakable walls
    for row, column in field.breakable_walls_coord:
        field.field[row][column] = field.breakable_wall_id
    # bombs
    for bomb in bombs_list:
        field.field[bomb.row][bomb.column] = bomb.id
    # monsters
    for monster in monsters_list:
        field.field[monster.row][monster.column] = monster.id
    # player
    field.field[player.row][player.column] = player.id
    # explosion
    for explosion in explosions_list:
        for row, column in explosion.explosion_area:
            field.field[row][column] = explosion.id
    # portal
    if portal_exists:
        field.field[portal.row][portal.column] = portal.id
    # player is dying
    # if player.dying_process:
    #     field.field[player.row][player.column] = player.dying_id
    #     player.dying_process = False
    # player won
    if player_won:
        field.field[player.row][player.column] = player.win_id
    return field


def update_loop(player, my_monsters, portal, player_lost, postmortem_steps):
    if not player.alive:
        player_lost = True
        postmortem_steps += 1
        if postmortem_steps > 1:
            time.sleep(0.5)
    return player_lost, player.win(my_monsters, portal), postmortem_steps
