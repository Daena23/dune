import time
from classes_and_functions_monsters_2_08 import monster_one_step, Field, Player, Bomb, Portal

# penetrable_objects_for_player = [0, 4, 5, 7]

lines = Field(size=13, p_walls=0.3)
lines.monster_list_init = lines.monster_coord_ident_init()  # начальные координаты всех монстров
my_monsters = lines.monster_arrangement_init()  # определяем id монстров и рассаживаем монстров
lines.penetrable_cell_coord = lines.penetrable_cell_coord_ident()

player = Player()

# Начальное поле: засаживаем монстрами и игроком пустое поле
lines.field = lines.field_player_and_monsters_arrangement_init(my_monsters)
lines.playfield_creation()  # визуализация
bomb = Bomb()
portal = Portal()
my_bombs = []

while lines.postmortem_steps < 10 and not player.is_player_win:
    #   player_move, bomb creation, bomb_explosion_area_ident, bomb disappearence
    player.player_coord = Bomb.bomb_positioning(player, lines, my_bombs)

    lines.wall_explosion(bomb)

    #   непроходимость бомбы
    if len(my_bombs) > 0:
        for bomb in my_bombs:
            bomb.bomb_is_not_passable(lines)
            if bomb.bomb_exist:
                bomb.timer += 1

    # движение игрока
    # определение координат монстров, ход монстра и проверка на сьедение игрока

    for monster in my_monsters:
        monster_one_step(monster, lines)
        player.if_player_eaten(monster)
        # cюда взорван ли монстр = if alive = False = > = а если фолс монстр то монстер в му монстер - ремув

    # bomb kills player, player dead
    for bomb in my_bombs:
        bomb.bomb_kills_player(player)
        bomb.bomb_kills_monster(my_monsters, my_bombs)
# появление портала
    portal.portal_appearance(lines, my_monsters, player)
    player.is_player_win(lines, portal)


    lines.field = lines.playfield_update(player, my_monsters, my_bombs, bomb)
    lines.playfield_creation()
    lines.step = lines.step + 1
    time.sleep(0.1)
