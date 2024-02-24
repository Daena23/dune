import random
import time
from copy import deepcopy
from typing import Tuple

from bomb import Bomb
from configurations import DIR_VARS, ID_DICT, SYMBOLS
from monster import MonsterDog, MonsterHexamoebo
from explosion import Explosion
from field import Field
from game_objects import Game


def update_bombs(field: Field, game: Game) -> None:
    game.bombs[:] = [bomb for bomb in game.bombs if not bomb.exploding()]
    field.max_bomb_reached = True if len(game.bombs) >= field.max_bomb_number else False
    for bomb in game.bombs:
        bomb.timer += 1


def create_bomb(game: Game) -> None:
    game.bombs.append(Bomb(game.player.previous_row, game.player.previous_column))
    if [game.player.previous_row, game.player.previous_column] in game.penetrable_cell_coord:
        game.penetrable_cell_coord.remove([game.player.previous_row, game.player.previous_column])
    else:
        print('choto ne tak game loop, 18')  # todo здесь проблема


def update_portal(game: Game, player_won, player_lost):
    if not (player_won or player_lost):
        if not game.monsters:
            if not game.portal.activated:
                game.portal.activated = True
                game.portal.id = ID_DICT['Portal']
            else:
                if game.portal.check_win_condition(game):
                    player_won = True
        else:
            if game.portal.activated:
                game.portal.activated = False
                game.portal.id = -1
    return player_won


def update_explosions(field, game):
    for bomb in game.bombs:
        if bomb.exploding():
            explosion = Explosion(game, bomb.row, bomb.column)
            game.explosions.append(explosion)
            game.penetrable_cell_coord.append([bomb.row, bomb.column])
            is_chain = explosion.affect_own_area(field, game)
            while is_chain:
                for bomb in game.bombs:
                    if bomb.exploding():
                        explosion = Explosion(game, bomb.row, bomb.column)
                        game.explosions.append(explosion)
                is_chain = False
                # Iterate over existing bombs. If one is affected by current explosion
                # (and is not yet exploded) - then we should explode this new bomb.


def create_new_monsters(game):
    if game.create_new_monsters:
        for counter in range(3):
            game.monsters.append(MonsterDog(game.portal.row, game.portal.column, DIR_VARS['undefined']) if random.random() > 0.5
                                 else MonsterHexamoebo(game.portal.row, game.portal.column, DIR_VARS['undefined']))
    game.create_new_monsters = False



def update_object_state(field, game):
    for lst in [game.monsters, game.breakable_walls, game.bombs]:
        lst[:] = [obj for obj in lst if obj.exists]
    game.explosions = []
    field.breakable_wall_coord = [[wall.row, wall.column] for wall in game.breakable_walls]


def update_field(field: Field, game: Game, player_won) -> None:
    field.field = deepcopy(field.empty_field)
    # put objects
    for obj in game.get_objects():
        field.field[obj.row][obj.column].append(obj)


def update_loop(game: Game,
                player_won: bool,
                player_lost: bool,
                postmortem_steps: int,
                ) -> Tuple[bool, bool, int]:
    if player_lost:
        game.player.symbol = SYMBOLS['Grave']
    if not game.player.exists:
        player_lost = True
        postmortem_steps += 1
        time.sleep(0.5)
    if player_won:
        postmortem_steps += 1
    return player_won, player_lost, postmortem_steps


def visualize(field, game):
    print()
    # border
    print(4 * ' ', end='')
    for size in range(field.size):
        print(size, end=2 * ' ')
    print()
    symbol = ''
    for row in range(field.size):
        # border
        if row < 10:
            string = str(row) + ' '
        else:
            string = str(row)
        # field
        for column in range(field.size):
            if not field.field[row][column]:
                symbol = ' '
            else:
                id_repr = max(obj.id for obj in field.field[row][column])
                for obj in field.field[row][column]:
                    if obj.id == id_repr:
                        symbol = obj.symbol
            if put_explosion(game, row, column):
                symbol = SYMBOLS['ExplosionBeam']
            string = string + 2 * ' ' + symbol
        print(string)  # field
    print()


def put_explosion(game, row, column):
    for explosion in game.explosions:
        liv_obj_coord = [[liv_obj.row, liv_obj.column] for liv_obj in game.get_living_objects()]
        if [row, column] in explosion.area and [row, column] not in liv_obj_coord:
            return True
    return False


def put_on_field(field, obj_lst) -> None:
    for obj in obj_lst:
        field.field[obj.row][obj.column].append(obj)

