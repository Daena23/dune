import time
# from classes_and_functions_monsters_17_08 import monster_movement, Field, Player, Bomb, Portal

from field import Field
from player import Player
from monster import monster_movement
from bomb import Bomb
from portal import Portal


# initial field
lines = Field(size=13, p_walls=0.3)
lines.monster_list_init = lines.monster_coord_ident_init()  # выбор начальных координат всех монстров
my_monsters = lines.create_monsters()  # определяем id монстров и создаем лист монстров
lines.penetrable_cell_coord = lines.penetrable_cell_coord_ident()
lines.field = lines.field_player_and_monsters_placement_init(my_monsters) # засаживаем монстрами и игроком пустое поле

# initial parameters
player = Player()
bomb = Bomb()
portal = Portal()
my_bombs = []
player_step_counter = 0
lines.penetrable_cell_coord.sort()

lines.playfield_visualization()


while lines.postmortem_steps < 8 and not player.is_player_win(portal):
    #   player_move, bomb creation, bomb_explosion_area_ident
    player.player_turn(lines, my_bombs)
    # определение координат монстров, ход монстра и проверка на сьедение игрока

# до ятобы бомба отлоденннафя становилась не пенетр, это учитывалось, а монстр выбипал напряавление в соответстии с этим усдвлием.
    # также надо чтобы монстр не мог ходить в стену
    for bomb in my_bombs:
        # взрыв стены, непроходимость бомбы, счетчик бомбы
        bomb.timer += 1
        bomb.wall_explosion(lines)
        bomb.bomb_kills_player(player)
        bomb.bomb_kills_monster(my_monsters)
        bomb.bomb_is_not_passable(lines)
        print('bomb timer', bomb.timer, bomb.explosion_area)
    for monster in my_monsters:
        print(monster.y_monster, monster.x_monster, 'm')


    for monster in my_monsters:
        monster_movement(monster, lines)
        player.if_player_eaten(monster)
    if player.player_step_counter + player.refractory_time == lines.step:
        player.refractory_period = False
    #    bomb.bomb_circular_explosion()

    portal.portal_appearance(lines, my_monsters)
    player.is_player_win(portal)
    lines.field = lines.playfield_update(player, my_monsters, my_bombs, portal)
    lines.playfield_visualization()
    lines.step = lines.step + 1
    if not player.is_alive:
        lines.postmortem_steps += 1
        time.sleep(0.5)
