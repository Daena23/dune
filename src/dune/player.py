from any_object import LivingObject
from configurations import EVENTS_JUST_WALK, EVENTS_PUT_BOMB, PLAYER_INIT_COORD, PLAYER_VARS, SYMBOLS
from field import Field
from game_loop import create_bomb
from game_objects import Game


class Player(LivingObject):
    def __init__(self):
        super().__init__(PLAYER_INIT_COORD[0][0], PLAYER_INIT_COORD[0][1])
        # coord
        self.row_init = 1
        self.column_init = 1
        self.row = 1
        self.column = 1
        self.previous_row = 1
        self.previous_column = 1
        self.coord = [1, 1, False]
        # properties
        self.exists = True
        self.penetrable = True

    def make_move(self,
                  field: Field,
                  game: Game,
                  step: int,
                  player_won: bool,
                  player_lost: bool,
                  ) -> None:
        if not (player_won or player_lost):
            event = self.get_command(field)
            self.make_step(game, event)
            if event in EVENTS_PUT_BOMB and not field.max_bomb_reached:
                self.put_bomb(game)

    @staticmethod
    def get_command(field: Field) -> str:
        str_just_walk, str_walk_and_put_bombs = 'w, a, s, d or z', 't, f, g, h or x'
        if field.max_bomb_reached:
            str_walk_and_put_bombs = ''
        while True:
            event = input(f'Input {str_just_walk} | {str_walk_and_put_bombs}')
            if event in (EVENTS_JUST_WALK + EVENTS_PUT_BOMB):
                return event
            else:
                print('Wrong input')

    def make_step(self, game, event: str) -> None:
        self.previous_row, self.previous_column = self.row, self.column
        for i in range(len(PLAYER_VARS)):
            event_vars = PLAYER_VARS[i][3] + PLAYER_VARS[i][4]
            coord_vars = [self.row + PLAYER_VARS[i][0], self.column + PLAYER_VARS[i][1]]
            if event in event_vars + event_vars.upper() and coord_vars in game.penetrable_cell_coord:
                self.previous_row, self.previous_column = self.row, self.column
                self.row += PLAYER_VARS[i][0]
                self.column += PLAYER_VARS[i][1]

    def put_bomb(self, game: Game) -> None:
        if [self.previous_row, self.previous_column] != [game.portal.row, game.portal.column] and \
                [game.player.row, game.player.column] in game.penetrable_cell_coord:
            create_bomb(game)

    def kill(self) -> None:
        self.symbol = SYMBOLS['Destroying']
        self.exists = False
