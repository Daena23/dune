from utils import PLAYER_COORDINATE_VARIANTS
from bomb import Bomb
from grave import Grave


class Player:
    def __init__(self):
        self.print_symbol = 'P'
        self.priority = 2
        self.y = 1
        self.x = 1
        self.y_old_coord = 1
        self.x_old_coord = 1
        self.is_alive = True
        self.refractory_period = False
        self.refractory_time = 0
        self.can_player_pass = True
        self.can_monster_pass = True
        self.stop_explosion = False
        self.max_bombs_n = 2
        # self.player_coord = [1, 1, False]
        # self.player_step_counter = 0
        self.explosible = False

    def player_turn(self, field, all_bombs):
        wasd = 'wasdz'
        tfgh = ['t', 'f', 'g', 'h', 'x']
        if self.is_alive:
            if not self.refractory_period:
                event = input('Do you want to put a bomb? Enter the direction of player | wasd/tfgh')
                if event in wasd:
                    self.player_move(field, event)
                elif event in tfgh:
                    self.bomb_creation(field, all_bombs)
                    self.player_move(field, event)
                else:
                    print('Ti che nabral allo?')
            elif self.refractory_period:
                event = input('Enter the direction of player | wasd')
                self.player_move(field, event)

    def player_move(self, field, event):
        if self.is_alive:
            self.y_old_coord = self.y
            self.x_old_coord = self.x
            for i in range(len(PLAYER_COORDINATE_VARIANTS)):
                if event == PLAYER_COORDINATE_VARIANTS[i][3] or event == PLAYER_COORDINATE_VARIANTS[i][4]:
                    y_new = self.y + PLAYER_COORDINATE_VARIANTS[i][0]
                    x_new = self.x + PLAYER_COORDINATE_VARIANTS[i][1]
                    if [y_new, x_new] in field.penetrable_cells_coord: # direction_choice
                        self.y = y_new
                        self.x = x_new
                    field.field[self.y_old_coord][self.x_old_coord].remove(self)
                    field.field[self.y][self.x].append(self)

    def if_player_eaten(self, field, monster):
        eating_condition = False
        if self.is_alive:
            if monster.y == self.y and monster.x == self.x:
                eating_condition = True
                print('you are eaten')
                self.player_dead(field)
            switch_eating_condition1 = False
            switch_eating_condition2 = False
            if monster.y == self.y_old_coord and monster.x == self.x_old_coord:
                switch_eating_condition1 = True
            if monster.y_old_coord == self.y and monster.x_old_coord == self.x:
                switch_eating_condition2 = True
            if switch_eating_condition1 and switch_eating_condition2:
                print('sam nabizhal na monstra')
                self.player_dead(field)

    def player_dead(self, field):
        if self.is_alive:
            self.is_alive = False
            field.field[self.y][self.x].remove(self)
            field.field[self.y][self.x].append(Grave())

    def is_player_win(self, portal):
        if self.y == portal.y and self.x == portal.x:
            self.print_symbol = 'W'
            return True
        return False

    def bomb_creation(self, field, all_bombs):
        bomb = Bomb()
        bomb.bomb_exist = True
        self.refractory_period = True
        self.player_step_counter = field.step
        bomb.y = self.y
        bomb.x = self.x
        bomb.timer = 0
        bomb.explosion_area = bomb.bomb_explosion_area_ident(field)
        field.field[self.y][self.x].append(bomb)
        all_bombs.append(bomb)
        field.penetrable_cells_coord.remove([self.y, self.x])
        return all_bombs

    def player_cooldown_switch(self, all_bombs):
        self.refractory_period = len(all_bombs) >= self.max_bombs_n
