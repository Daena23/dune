import time
# from classes_and_functions_monsters_17_08 import monster_movement, Field, Player, Bomb, Portal

from field import Field
from player import Player
from monster import monster_movement
from bomb import Bomb
from portal import Portal

# penetrable_objects_for_player = [0, 4, 5, 7]

# initial field
lines = Field(size=13, p_walls=0.3)
lines.monster_list_init = lines.monster_coord_ident_init()  # выбор начальных координат всех монстров
my_monsters = lines.create_monsters()  # определяем id монстров и создаем лист монстров
lines.penetrable_cell_coord = lines.penetrable_cell_coord_ident()
lines.field = lines.field_player_and_monsters_placement_init(my_monsters) # засаживаем монстрами и игроком пустое поле
lines.playfield_visualization()

# initial parameters
player = Player()
bomb = Bomb()
portal = Portal()
my_bombs = []

while lines.postmortem_steps < 5 and not player.is_player_win(portal):
    #   player_move, bomb creation, bomb_explosion_area_ident
    player.player_coord = player.player_turn(lines, my_bombs)
    for bomb in my_bombs:
        # конец рефр периода
        if bomb.timer == player.refractory_time:
            player.refractory_period = False
        # взрыв стены, непроходимость бомбы, счетчик бомбы
        lines.wall_explosion(bomb)
        bomb.timer += 1
        bomb.bomb_kills_player(player)
        bomb.bomb_kills_monster(my_monsters, my_bombs)
        print('bombs', bomb.y, bomb.x, bomb.bomb_exist, bomb.explosion_area, 'refr', player.refractory_period)

    #    bomb.bomb_circular_explosion()

    # определение координат монстров, ход монстра и проверка на сьедение игрока

    for monster in my_monsters:
        monster_movement(monster, lines)
        player.if_player_eaten(monster)
        # cюда взорван ли монстр = if alive = False = > = а если фолс монстр то монстер в му монстер - ремув
    for bomb in my_bombs:
        bomb.bomb_is_not_passable(lines)

    # bomb kills player, player dead
# появление портала
    portal.portal_appearance(lines, my_monsters, player)
  #  player.is_player_win(lines, portal)
    lines.field = lines.playfield_update(player, my_monsters, my_bombs, bomb)
    lines.playfield_visualization()
    lines.step = lines.step + 1
    time.sleep(0.1)
