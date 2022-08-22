import time
# from classes_and_functions_monsters_17_08 import monster_movement, Field, Player, Bomb, Portal

from field import Field
from player import Player
from monster import monster_movement
from bomb import Bomb
from portal import Portal


def main():

    # initial field
    lines = Field(size=13, p_walls=0)
    lines.monster_list_init = lines.monster_coord_ident_init()  # выбор начальных координат всех монстров
    my_monsters = lines.create_monsters()  # определяем id монстров и создаем лист монстров
    lines.penetrable_cell_coord = lines.penetrable_cell_coord_ident()
    # засаживаем монстрами и игроком пустое поле
    lines.field = lines.field_player_and_monsters_placement_init(my_monsters)

    # initial parameters
    player = Player()
    bomb = Bomb()
    portal = Portal()
    my_bombs = []
    player_step_counter = 0
    lines.penetrable_cell_coord.sort()

    lines.playfield_visualization()

    while lines.postmortem_steps < 8 and not player.is_player_win(portal):
        # также надо чтобы монстр не мог ходить в стену
        player.player_turn(lines, my_bombs)
        for bomb in my_bombs:
            # взрыв стены, непроходимость бомбы, счетчик бомбы
            bomb.timer += 1
            bomb.wall_explosion(lines)
            bomb.bomb_kills_player(player)
            bomb.bomb_is_not_passable(lines)
            # print('bomb timer', bomb.timer, bomb.explosion_area)
        # bomb.circular_explosion(lines, my_bombs)
        # определение координат монстров, ход монстра и проверка на сьедение игрока
        for monster in my_monsters:
            monster_movement(monster, lines)
            player.if_player_eaten(monster)
        for bomb in my_bombs:
            bomb.bomb_kills_monster(my_monsters)
            bomb.bomb_explodes_bomb(my_bombs)
        player.player_cooldown_switch(bomb, my_bombs)
        portal.portal_appearance(lines, my_monsters)
        lines.field = lines.playfield_update(player, my_monsters, my_bombs, portal)
        lines.playfield_visualization()
        lines.step = lines.step + 1
        if not player.is_alive:
            lines.postmortem_steps += 1
            time.sleep(0.5)

    if player.is_player_win(portal):
        print('you win')
    if not player.is_alive:
        print('you loose')


if __name__ == '__main__':  # Вызывается только если мы напрямую вызываем данный файл (python dune_main_re.py)
    main()
