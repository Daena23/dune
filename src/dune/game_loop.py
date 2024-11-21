import time
from copy import deepcopy
from random import choice
from typing import List, Tuple

from bomb import Bomb
from configurations import SYMBOLS, LEVEL_CONSTANTS, DIR_VARS
from explosion import Explosion
from field import Field
from game import Game
from monster import MonsterDog, MonsterHexamoebo


def update_bombs(field: Field, game: Game) -> None:
    game.bombs[:] = [bomb for bomb in game.bombs if not bomb.exploding()]
    field.max_bomb_reached = True if len(game.bombs) >= field.max_bomb_number else False
    for bomb in game.bombs:
        bomb.timer += 1


def create_bomb(game: Game) -> None:
    game.bombs.append(Bomb(game.player.previous_row, game.player.previous_column))
    game.penetrable_cell_coord.remove([game.player.previous_row, game.player.previous_column])


def check_if_player_won(game: Game, player_won: bool) -> bool:
    if game.monsters:
        game.portal.deactivate()
    else:
        game.portal.activate()
    return player_won


def update_explosions(field: Field, game: Game) -> None:
    for bomb in game.bombs:
        if bomb.exploding():
            explosion = Explosion(game, bomb.row, bomb.column)
            game.explosions.append(explosion)
            game.penetrable_cell_coord.append([bomb.row, bomb.column])
            is_chain = explosion.affect_own_area(field, game)
            while is_chain:  # circular explosion
                for bomb in game.bombs:
                    if bomb.exploding():
                        explosion = Explosion(game, bomb.row, bomb.column)
                        game.explosions.append(explosion)
                is_chain = False


def update_field(field: Field, game: Game) -> None:
    field.main = deepcopy(field.empty)
    for obj in game.objects:
        field.main[obj.row][obj.column].append(obj)


def update_loop(
        game: Game,
        player_won: bool,
        player_lost: bool,
        postmortem_steps: int,
) -> Tuple[bool, bool, int]:
    if not game.monsters and game.portal.activated:
        player_won = game.portal.check_if_win(game)
    if player_lost:
        game.player.symbol = SYMBOLS['Grave']
    if not game.player.exists:
        player_lost = True
        postmortem_steps += 1
        time.sleep(0.5)
    if player_won:
        postmortem_steps += 1
        time.sleep(0.5)
    return player_won, player_lost, postmortem_steps


def visualize(field: Field, game: Game) -> None:
    print()
    symbol = ''
    for row in range(field.size):
        expl_visual = ''
        for column in range(field.size):
            if not field.main[row][column]:
                symbol = ' '
            else:
                id_repr = max(obj.id for obj in field.main[row][column])
                for obj in field.main[row][column]:
                    if obj.id == id_repr:
                        symbol = obj.symbol
            if put_explosion(game, row, column):
                symbol = SYMBOLS['ExplosionBeam']
            expl_visual = expl_visual + 2 * ' ' + symbol
        print(expl_visual)
    print()


def put_explosion(game: Game, row: int, column: int) -> bool:
    for explosion in game.explosions:
        liv_obj_coord = [[liv_obj.row, liv_obj.column] for liv_obj in game.living_objects]
        if [row, column] in explosion.area and [row, column] not in liv_obj_coord:
            return True
    return False


def remove_objects(field: Field, game: Game) -> None:
    for objects in [game.monsters, game.breakable_walls, game.bombs]:
        objects[:] = [obj for obj in objects if obj.exists]
    field.breakable_wall_coord = [[wall.row, wall.column] for wall in game.breakable_walls]
    game.explosions = []


def put_on_field(field: Field, obj_lst: List) -> None:
    for obj in obj_lst:
        field.main[obj.row][obj.column].append(obj)


def create_monster(game: Game, row: int, column: int) -> None:
    new_monster = (MonsterDog, MonsterHexamoebo)
    game.monsters.append(choice(new_monster)(row, column, DIR_VARS['undefined']))

def create_monsters_from_portal(game: Game) -> None:
    for counter in range(LEVEL_CONSTANTS['portal_monster_number']):
        create_monster(game, game.portal.row, game.portal.column)
    game.portal.is_under_explosion = False
