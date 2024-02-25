from typing import List

from any_object import AnyObject
from configurations import COORD_VARS, LEVEL_CONSTANTS, SYMBOLS
from field import Field
from game_objects import Game


class Explosion(AnyObject):
    def __init__(self, game, bomb_row, bomb_column):
        super().__init__()
        self.symbol = SYMBOLS['Explosion']
        self.power = LEVEL_CONSTANTS['power']
        self.exists = True
        # coord
        self.row = bomb_row
        self.column = bomb_column
        self.area = self.find_area(game)
        # properties
        self.penetrable = True

    def find_area(self, game: Game) -> List[List[int]]:
        area = []
        for row_dir, column_dir in COORD_VARS[0:4]:
            for power in range(1, LEVEL_CONSTANTS['power']):
                row_beam, column_beam = self.row + row_dir * power, self.column + column_dir * power
                if has_object(game.non_breakable_walls, row_beam, column_beam):
                    break
                if has_object(game.breakable_walls, row_beam, column_beam):
                    area.append((row_beam, column_beam))
                    break
                area.append((row_beam, column_beam))
        area = set(area)
        return [list(explosion_point) for explosion_point in area]

    def affect_own_area(self, field: Field, game: Game) -> bool:
        chain = False
        for row, column in self.area:
            hits_living_object(game, row, column)
            hits_portal(field, game, row, column)
            hits_wall(game, row, column)
            another_bomb_affected = hits_bomb(game, row, column)
            chain = chain or another_bomb_affected
        # It returns whether this explosion hits another bomb or not.
        return chain


def hits_living_object(game: Game, row_beam: int, column_beam: int) -> None:
    for liv_obj in game.get_living_objects():
        if [liv_obj.row, liv_obj.column] == [row_beam, column_beam]:
            destroy(liv_obj)


def hits_portal(field: Field, game: Game, row_beam: int, column_beam: int) -> None:
    if [game.portal.row, game.portal.column] == [row_beam, column_beam] and\
            [game.portal.row, game.portal.column] not in field.breakable_wall_coord:
        game.create_new_monsters = True


def hits_wall(game: Game, row_beam: int, column_beam: int) -> None:
    for obj in game.breakable_walls:
        if [obj.row, obj.column] == [row_beam, column_beam]:
            destroy(obj)
            game.penetrable_cell_coord.append([row_beam, column_beam])


def destroy(obj) -> None:
    obj.exists = False
    obj.symbol = SYMBOLS['Destroying']


def hits_bomb(game: Game, row_beam: int, column_beam: int) -> bool:
    for bomb in game.bombs:
        if [bomb.row, bomb.column] == [row_beam, column_beam]:
            bomb.timer = LEVEL_CONSTANTS['bomb_lifetime']
            return True
    return False


def has_object(objects: List[AnyObject], row: int, column: int) -> bool:
    for obj in objects:
        if [obj.row, obj.column] == [row, column]:
            return True
    return False
