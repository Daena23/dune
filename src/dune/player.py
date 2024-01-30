from configurations import PLAYER_COORDINATE_VARIANTS
from bomb import Bomb

class Player:
    def __init__(self):
        self.id = 9
        self.player_win_id = 11
        self.y_player = 1
        self.x_player = 1
        self.y_player_old_coord = 1
        self.x_player_old_coord = 1
        self.is_alive = True
        self.refractory_period = False
        self.refractory_time = 0
        self.player_coord = [1, 1, False]
        self.player_step_counter = 0

    def player_turn(self, lines, my_bombs):
        wasd = 'wasdz'
        tfgh = ['t', 'f', 'g', 'h', 'x']
        if self.is_alive:
            if not self.refractory_period:
                event = input('Do you want to put a bomb? Enter the direction of player | wasd/tfgh')
                if event in wasd:
                    self.player_move(lines, event)
                elif event in tfgh:
                    self.bomb_creation(lines, my_bombs)
                    self.player_move(lines, event)
                else:
                    print('Ti che nabral allo?')
            elif self.refractory_period:
                event = input('Enter the direction of player | wasd')
                self.player_move(lines, event)

    def player_move(self, lines, event):
        if self.is_alive:
            for i in range(len(PLAYER_COORDINATE_VARIANTS)):
                y_player_new = self.y_player + PLAYER_COORDINATE_VARIANTS[i][0]
                x_player_new = self.x_player + PLAYER_COORDINATE_VARIANTS[i][1]
                direction_choice = False
                if event == PLAYER_COORDINATE_VARIANTS[i][3] or event == PLAYER_COORDINATE_VARIANTS[i][4]:
                    direction_choice = True
                if direction_choice and [y_player_new, x_player_new] in lines.penetrable_cell_coord:
                    self.y_player_old_coord = self.y_player
                    self.x_player_old_coord = self.x_player
                    self.y_player = y_player_new
                    self.x_player = x_player_new
        self.player_coord = [self.y_player, self.x_player, self.refractory_period]

    def if_player_eaten(self, monster):
        eating_condition = False
        if self.is_alive:
            if monster.y_monster == self.y_player and monster.x_monster == self.x_player:
                eating_condition = True
                print('you are eaten')
                self.player_dead()

            # к следующему условию мгого вопросов: надо еще добавить старые координаты монстра
            switch_eating_condition1 = False
            switch_eating_condition2 = False
            if monster.y_monster == self.y_player_old_coord and monster.x_monster == self.x_player_old_coord:
                switch_eating_condition1 = True
            if monster.y_monster_old_coord == self.y_player and monster.x_monster_old_coord == self.x_player:
                switch_eating_condition2 = True
            if switch_eating_condition1 and switch_eating_condition2:
                print('sam nabizhal na monstra')
                self.player_dead()

    def player_dead(self):
        self.id = 8
        self.is_alive = False

    def bomb_creation(self, lines, my_bombs):
        bomb = Bomb()
        bomb.bomb_exist = True
        self.refractory_period = True
        self.player_step_counter = lines.step
        bomb.y = self.y_player
        bomb.x = self.x_player
        bomb.timer = 0
        bomb.explosion_area = bomb.bomb_explosion_area_ident(lines)
        my_bombs.append(bomb)
        return my_bombs

    def is_player_win(self, portal):
        if self.y_player == portal.y and self.x_player == portal.x:
            # lines.field[self.y_player, self.x_player] = self.player_win_id
            # print('is_player_winyou win!')
            return True
        return False

    def player_cooldown_switch(self, bomb, my_bombs):
        bomb_timer = 0
        if len(my_bombs) == bomb.max_bombs_n:
            bomb_timer = my_bombs[0].timer
        if len(my_bombs) == bomb.max_bombs_n and bomb_timer < bomb.explosion_time - 1:
            self.refractory_period = True
        else:
            self.refractory_period = False
        # print(self.refractory_period, 'my_bombs', len(my_bombs), '1bombtimer', bomb_timer)
