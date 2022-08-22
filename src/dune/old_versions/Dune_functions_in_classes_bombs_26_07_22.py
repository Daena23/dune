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
bomb = Bomb()


field = lines.field_creation_init(my_monsters) # Начальное поле: засаживаем монстрами и игроком пустое поле
lines.playfield_creation() #   визуализация

# основной шаг

while lines.postmortem_steps < 50:
# bomb quest, bomb creation, bomb_explosion_area_ident + disap
    bomb.bomb_positioning(player, lines)

# for bomb in my_bombs:
    if bomb.bomb_exist:
        bomb.bomb_timer += 1
# движение игрока
    player_coord = player.player_move(lines)
# определение координат монстров, ход монстра и проверка на сьедение игрока
    for monster in my_monsters:
        y_monster, x_monster, monster_direction, monster_id, if_monster_alive = monster.y_monster, monster.x_monster, monster.direction, monster.id, monster.if_monster_alive
        monster_old_coord = [y_monster, x_monster]
        monster_new_coord = monster.monster_move(lines)
        monster.y_monster, monster.x_monster, monster.direction = monster_new_coord
        time.sleep(0.01)
        player.if_player_eaten(monster_new_coord, monster_old_coord)

# bomb kills player, player dead
    if player.player_alive:
        bomb.bomb_kills_player(player)
# bomb kills monster, monster dead
#    bomb.bomb_kills_monster(monster)

    # заполнение ИГРОВОГО поля
    lines.breakable_walls_coord = lines.wall_explosion(bomb)
    field = lines.playfield_update(bomb, player, my_monsters)
    lines.playfield_creation()
    if not player.player_alive:
        lines.postmortem_steps = lines.postmortem_steps + 1
    lines.step = lines.step + 1