from configurations import EVENTS_JUST_WALK, EVENTS_PUT_BOMB, PLAYER_COORD_VARS


class Player:
    init_id = 4
    dying_id = 11
    dead_id = 5
    win_id = 11

    def __init__(self):
        self.id = Player.init_id
        self.row_init = 1
        self.column_init = 1
        self.row = 1
        self.column = 1
        self.previous_row = 1
        self.previous_column = 1
        self.coord = [1, 1, False]
        self.alive = True
        self.creating_bomb = False
        self.won = False
        self.refractory_time = 0

    @staticmethod
    def command(field) -> str:
        str_just_walk = 'w, a, s, d or z'
        str_walk_and_put_bombs = 't, f, g, h or x'
        event_put_bomb = EVENTS_PUT_BOMB
        if field.max_bombs_reached:
            event_put_bomb = None
            str_walk_and_put_bombs = None
        while True:
            event = input(f'Input {str_just_walk} | {str_walk_and_put_bombs}')
            if event in (EVENTS_JUST_WALK + event_put_bomb):
                return event
            else:
                print('Wrong input')

    def move(self, field, event: str):
        self.previous_row, self.previous_column = self.row, self.column
        for i in range(len(PLAYER_COORD_VARS)):
            if event in (PLAYER_COORD_VARS[i][3], PLAYER_COORD_VARS[i][4]) and \
                    [self.row + PLAYER_COORD_VARS[i][0], self.column + PLAYER_COORD_VARS[i][1]]\
                    in field.penetrable_cells_coord:
                self.previous_row, self.previous_column = self.row, self.column
                self.row = self.row + PLAYER_COORD_VARS[i][0]
                self.column = self.column + PLAYER_COORD_VARS[i][1]

    def kill(self):
        self.id = Player.dying_id
        self.alive = False

    def win(self):
        self.id = Player.win_id
        self.won = True
        print('is_player_win!')
