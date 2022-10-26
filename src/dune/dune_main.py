import time
from dune import wall
from field import Field
from player import Player
from monster import monster_movement
from bomb import Bomb
from portal import Portal
from wall import Boundary_Wall
from wall import Unbreakable_Wall
from wall import Breakable_Wall
from explosion import Explosion


def main():
    # initial field
    field = Field(size=13, p_walls=0.3)
    field.monster_list_init = field.monster_coord_ident_init()  # выбор начальных координат всех монстров
    all_monsters = field.create_monsters()  # создаем лист монстров

    # initial parameters
    player = Player()
    portal = Portal()
    all_bombs = []
    all_explosions = []

    # засаживаем монстрами и игроком пустое поле
    field.field = field.field_player_and_monsters_placement_init(player, all_monsters)
    field.playfield_visualization()
    field.penetrable_cells_coord = field.penetrable_cells_coord_ident()
    while field.postmortem_steps < 8 and not player.is_player_win(portal):
        field.penetrable_cells_coord = [list(x) for x in sorted(set([tuple(y) for y in field.penetrable_cells_coord]))]
        player.player_turn(field, all_bombs)
        # определение координат монстров, ход монстра и проверка на сьедение игрока
        for monster in all_monsters:
            monster_movement(monster, field)
            # monster.monster_reproduction()
            player.if_player_eaten(field, monster)
        player.player_cooldown_switch(all_bombs)
        portal.portal_appearance(field, all_monsters)
        for bomb in all_bombs.copy():
            bomb.explosions_list_update(field, all_bombs, all_explosions)
            bomb.timer += 1
        for explosion in all_explosions.copy():  # копия чтобы не укорачивался список по ходу выполнения функции
            alive = explosion.explosion_update(field, all_explosions)
            if not alive:
                continue
            explosion.kills_player(field, player)
            explosion.kills_monster(field, all_monsters)
            explosion.wall(field)
            # explosion.bomb_explodes_bomb(field, bomb, all_bombs, all_explosions)
            explosion.portal(field, all_monsters, portal)

        player.is_player_win(portal)
        field.playfield_visualization()
        field.step += 1
        if not player.is_alive:
            field.postmortem_steps += 1
            time.sleep(0.5)
    # Final
    if player.is_player_win(portal):
        print('you win')
    if not player.is_alive:
        print('you loose')


if __name__ == '__main__':  # Вызывается только если мы напрямую вызываем данный файл (python dune_main_re.py)
    main()
