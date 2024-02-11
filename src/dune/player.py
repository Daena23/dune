from configurations import PLAYER_CV
from bomb import Bomb
from configurations import EVENTS_JUST_WALK, EVENTS_PUT_BOMB


class Player:
    id = 4
    dying_id = 8
    dead_id = 9
    win_id = 11

    def __init__(self):
        self.id = Player.id
        self.row_init = 1
        self.column_init = 1
        self.row = 1
        self.column = 1
        self.previous_row = None
        self.previous_column = None
        self.alive = True
        self.creating_bomb = False

        self.refractory_time = 0
        self.coord = [1, 1, False]
        # self.step_counter = 0

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

    def move(self, field, event):
        self.previous_row, self.previous_row = self.row, self.column
        for i in range(len(PLAYER_CV)):
            if event in (PLAYER_CV[i][3], PLAYER_CV[i][4]) and \
                    [self.row + PLAYER_CV[i][0], self.column + PLAYER_CV[i][1]] in field.find_penetrable_cells_coord():
                self.previous_row = self.row  # todo зачем previous
                self.previous_column = self.column
                self.row = self.row + PLAYER_CV[i][0]
                self.column = self.column + PLAYER_CV[i][1]
            else:
                pass

    def kill(self):
        self.id = Player.dying_id
        self.alive = False
        # self.dying_process = False

    def win(self, my_monsters, portal):
        if not my_monsters and (self.row, self.column == portal.row, portal.column):
            print('is_player_win!')
            return True
        return False
