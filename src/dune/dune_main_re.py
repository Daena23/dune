import time
# from classes_and_functions_monsters_17_08 import monster_movement, Field, Player, Bomb, Portal

from field import Field
from player import Player
from monster import monster_movement
from bomb import Bomb
from portal import Portal


def main():

    # initial field
    field = Field(size=13, p_walls=0.3)
    field.monster_list_init = field.monster_coord_ident_init()  # выбор начальных координат всех монстров
    all_monsters = field.create_monsters()  # определяем id монстров и создаем лист монстров
    field.penetrable_cells_coord = field.penetrable_cells_coord_ident()
    # засаживаем монстрами и игроком пустое поле
    field.field = field.field_player_and_monsters_placement_init(all_monsters)

    # initial parameters
    player = Player()
    bomb = Bomb()
    portal = Portal()
    all_bombs = []
    player_step_counter = 0
    field.penetrable_cells_coord.sort()

    field.playfield_visualization()
    while field.postmortem_steps < 8 and not player.is_player_win(portal):
        # также надо чтобы монстр не мог ходить в стену
        player.player_turn(field, all_bombs)
        for bomb in all_bombs:
            # взрыв стены, непроходимость бомбы, счетчик бомбы
            bomb.timer += 1
            bomb.wall(field)
            bomb.bomb_kills_player(player)
            bomb.bomb_is_not_passable(field)
            # print('bomb timer', bomb.timer, bomb.explosion_area)
        # bomb.circular_explosion(field, all_bombs)
        # определение координат монстров, ход монстра и проверка на сьедение игрока
        for monster in all_monsters:
            monster_movement(monster, field)
            player.if_player_eaten(monster)
        for bomb in all_bombs:
            bomb.bomb_kills_monster(all_monsters)
            bomb.bomb_explodes_bomb(all_bombs)
        player.player_cooldown_switch(bomb, all_bombs)
        portal.portal_appearance(field, all_monsters)
        field.field = field.playfield_update(player, all_monsters, all_bombs, portal)
        field.playfield_visualization()
        field.step = field.step + 1
        if not player.is_alive:
            field.postmortem_steps += 1
            time.sleep(0.5)

    if player.is_player_win(portal):
        print('you win')
    if not player.is_alive:
        print('you loose')


if __name__ == '__main__':  # Вызывается только если мы напрямую вызываем данный файл (python dune_main_re.py)
    main()
