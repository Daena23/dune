import random
from random import choice
import time
from copy import deepcopy
from classes_and_functions_monsters_1_08 import Lines, MonsterCat, MonsterDog, Player, Bomb


# penetrable_objects_for_player = [0, 4, 5, 7]

lines = Lines()
zero_field = lines.zero_field_creation() # создаем нулевой лист в листе
empty_field = lines.empty_field_creation()  # unbreakable intermediate and boundary walls
breakable_walls_coord = lines.breakable_walls_list_creation()
field_with_walls = lines.field_with_walls_creation() # заполняем breakable walls
empty_cell_coord_init = lines.empty_cells_identification()  # делаем лист с координатами пустых ячеек
lines.monster_list_init = lines.monster_coord_ident()  # начальные координаты всех монстров
my_monsters = lines.monster_arrangement() # рассаживаем монстров
penetrable_cell_coord = lines.penetrable_cell_coord_ident()  # penetr cell coord identification


player = Player()

bomb_description = []

field = lines.field_creation_init(my_monsters) # Начальное поле: засаживаем монстрами и игроком пустое поле
lines.playfield_creation() #   визуализация

# основной шаг

while lines.postmortem_steps < 50:
# бомба
    event_bomb = player.bomb_creation(bomb)

    if bomb.bomb_exist:
        bomb.bomb_timer += 1
    lines.breakable_walls_coord = lines.wall_explosion(bomb)

#     for bomb in my_bombs:
#        bomb.timer += 1
#         y_monster, x_monster, monster_direction, monster_id = bomb.y_bomb_coord, monster.y_bomb_coord, monster.direction, monster.id
#         monster_old_coord = [y_monster, x_monster]
# bomb = [bomb_number, y_bomb_coord, x_bomb_coord, bomb_timer, bomb_exist, explosion_area, breakable_walls_for_removal_coord]
    # print('bt', bomb.bomb_timer, 'bomb.breakable_walls_for_removal_coord', bomb.breakable_walls_for_removal_coord)


# движение игрока
    y_player = player.y_player
    x_player = player.x_player
    player_coord = player.player_move(lines.penetrable_cell_coord)
# определение координат монстров и проверка на сьедение игрока
    for monster in my_monsters:
        y_monster, x_monster, monster_direction, monster_id = monster.y_monster, monster.x_monster, monster.direction, monster.id
        monster_old_coord = [y_monster, x_monster]
        monster_new_coord = monster.move(penetrable_cell_coord, lines.step)
        monster.y_monster, monster.x_monster, monster.direction = monster_new_coord
        time.sleep(0.01)
        player.if_player_eaten(monster_new_coord, monster_old_coord)

    # заполнение ИГРОВОГО поля
    field = lines.playfield_update(bomb, player, my_monsters)
    lines.playfield_creation()
    if not player.player_alive:
        lines.postmortem_steps = lines.postmortem_steps + 1
    lines.step = lines.step + 1