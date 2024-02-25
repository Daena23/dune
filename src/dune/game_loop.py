import time
from copy import deepcopy
from typing import List, Tuple

from bomb import Bomb
from configurations import ID_DICT, SYMBOLS
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
    game.penetrable_cell_coord.remove([game.player.previous_row, game.player.previous_column])


def update_portal(game: Game, player_won: bool, player_lost: bool) -> bool:
    if not (player_won or player_lost):
        # portal activation and usage
        if not game.monsters:
            if not game.portal.activated:  # activation
                game.portal.activated = True
                game.portal.id = ID_DICT['Portal']
            else:
                if game.portal.check_win_condition(game):  # usage
                    player_won = True
        # portal is exploded
        else:
            if game.portal.activated:
                game.portal.activated = False
                game.portal.id = ID_DICT['PortalDeactivated']
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
    field.field = deepcopy(field.empty_field)
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
        time.sleep(0.5)
    return player_won, player_lost, postmortem_steps


def visualize(field: Field, game: Game) -> None:
    print()
    symbol = ''
    for row in range(field.size):
        string = ''
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


def put_explosion(game: Game, row: int, column: int) -> bool:
    for explosion in game.explosions:
        liv_obj_coord = [[liv_obj.row, liv_obj.column] for liv_obj in game.get_living_objects()]
        if [row, column] in explosion.area and [row, column] not in liv_obj_coord:
            return True
    return False


def update_object_state(field: Field, game: Game) -> None:
    for lst in [game.monsters, game.breakable_walls, game.bombs]:
        lst[:] = [obj for obj in lst if obj.exists]
    field.breakable_wall_coord = [[wall.row, wall.column] for wall in game.breakable_walls]
    game.explosions = []


def put_on_field(field: Field, obj_lst: List) -> None:
    for obj in obj_lst:
        field.field[obj.row][obj.column].append(obj)
