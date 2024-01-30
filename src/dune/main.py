import time

from field import Field
from player import Player
from monster import monster_movement
from bomb import Bomb
from portal import Portal


def main():
    # initial field
    field = Field(size=13, p_walls=0)
    field.monster_list_init = field.monster_coord_ident_init()  # выбор начальных координат всех монстров
    my_monsters = field.create_monsters()  # определяем id монстров и создаем лист монстров
    field.penetrable_cell_coord = field.penetrable_cell_coord_ident()
    # засаживаем монстрами и игроком пустое поле
    field.field = field.field_player_and_monsters_placement_init(my_monsters)

    # initial parameters
    player = Player()
    bomb = Bomb()
    portal = Portal()
    my_bombs = []
    player_step_counter = 0
    field.penetrable_cell_coord.sort()
    field.playfield_visualization()

    while field.postmortem_steps < 8 and not player.is_player_win(portal):
        # также надо чтобы монстр не мог ходить в стену
        player.player_turn(field, my_bombs)
        for bomb in my_bombs:
            # взрыв стены, непроходимость бомбы, счетчик бомбы
            bomb.timer += 1
            bomb.wall_explosion(field)
            bomb.bomb_kills_player(player)
            bomb.bomb_is_not_passable(field)
            # print('bomb timer', bomb.timer, bomb.explosion_area)
        # bomb.circular_explosion(lines, my_bombs)
        # определение координат монстров, ход монстра и проверка на сьедение игрока
        for monster in my_monsters:
            monster_movement(monster, field)
            player.if_player_eaten(monster)
        for bomb in my_bombs:
            bomb.bomb_kills_monster(my_monsters)
            bomb.bomb_explodes_bomb(my_bombs)
        player.player_cooldown_switch(bomb, my_bombs)
        portal.portal_appearance(field, my_monsters)
        field.field = field.playfield_update(player, my_monsters, my_bombs, portal)
        field.playfield_visualization()
        field.step = field.step + 1
        if not player.is_alive:
            field.postmortem_steps += 1
            time.sleep(0.5)

    if player.is_player_win(portal):
        print('you win ❤')
    if not player.is_alive:
        print('you loose ❤')


if __name__ == '__main__':  # Вызывается только если мы напрямую вызываем данный файл (python main.py)
    main()
