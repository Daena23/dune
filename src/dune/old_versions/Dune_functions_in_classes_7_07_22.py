import random
from random import choice
import time
from copy import deepcopy
from dune.classes_and_functions_monsters import playfield_creation, MonsterCat, MonsterDog, Player, Bomb

NOT_TO_MOVE_OBJECTS = [1, 2, 5]  # 1 - unbreakable walls, 2 - breakable wall, 5 - boundary wall
explosible_objects = [0, 2, 3, 4, 9]  # 6 - bomb, 7 - burst, 8 - grave, 9 - player

size = 19
p_walls = 0.3
p_monster = 5 / ((size - 1) ** 2 * 3 // 4)  # (size ** 2 - (size // 2) ** 2)

# создаем нулевой лист в листе
lines = []
for x in range(size):
    lines.append([0] * size)

# unbreakable intermediate and boundary walls
for t in range(size):
    for m in range(size):
        if (t % 2 == 0) and (m % 2 == 0):
            lines[t][m] = 2  # unbreakable intermediate walls
        if t == 0 or t == size - 1:
            lines[t][m] = 5  # boundary walls
        if m == 0 or m == size - 1:
            lines[t][m] = 5  # boundary walls

# breakable walls
for t in range(size):
    for m in range(size):
        if lines[t][m] != 2 and lines[t][m] != 5:
            if random.random() < p_walls:
                lines[t][m] = 1

# делаем лист с координатами пустых ячеек
empty_cell_coordinates = []
penetrable_cell_coord = []
monster_list_init = []
init_position = [[1, 1], [2, 1], [1, 2]]

# empty cells identification
for y in range(size):
    for x in range(size):
        if lines[y][x] == 0:
            empty_cell_coordinates.append([y, x])

# количество доступных для монстров клеток
monster_available_cells = empty_cell_coordinates.copy()
for counter in range(len(init_position)):
    if init_position[counter] in monster_available_cells:
        monster_available_cells.remove(init_position[counter])

# monster number identification
n_empty = len(monster_available_cells)
monster_list_init = []
n_monster = random.randint(30, 50)
while n_monster > n_empty:
    n_monster = random.randint(3, 8)

# создаем лист с init координатами монстров
print('число монстров равно', n_monster)
for counter in range(n_monster):
    monster_new_coord = choice(monster_available_cells)
    y_monster, x_monster = monster_new_coord
    monster_list_init.append([y_monster, x_monster, 'undefined'])
monster_list_init.sort()
# Player and its safespace
lines[1][1] = 0
lines[2][1] = 0
lines[1][2] = 0

# penetr cell coord identification
for y in range(size):
    for x in range(size):
        if lines[y][x] == 0 or lines[y][x] == 3 or lines[y][x] == 4:
            penetrable_cell_coord.append([y, x])
penetrable_cell_coord.append([1, 1])

# ........1.........
# ........|.........
# ........|........x
# 2-------+--------3
# ........|.........
# ........|.........
# ........0.y.......

# рассаживаем монстров
monster_list_curr = monster_list_init.copy()
my_monsters = []
n_monster_types = 2
for i in range(len(monster_list_curr)):
    monster_description = monster_list_curr[i]
    if random.randint(0, 2) > 1 / n_monster_types:
        monster = MonsterDog()
    else:
        monster = MonsterCat()
    monster.y_monster, monster.x_monster, monster.direction = monster_description
    my_monsters.append(monster)
    # ВАЖНО!my_monsters - лист с обьектами monster, monster - обьект, содержащий информацию о координатах и направлении
    # print(monster.y_monster, monster.x_monster, '|', monster.name, '')

player = Player()
bomb = Bomb()
player_new_coord = []
bomb_description = []

# Начальное поле: засаживаем монстрами и игроком пустое поле
lines_filled = deepcopy(lines)
lines_filled[1][1] = 9
for monster in my_monsters:
    lines_filled[monster.y_monster][monster.x_monster] = monster.id
playfield_creation(lines_filled, size)

# основной шаг
step = 0
postmorten_steps = 0
while postmorten_steps < 50:
# бомба
    if not player.refractory_period:
        player.bomb_question()
        y_bomb = player.y_bomb_coord
        x_bomb = player.x_bomb_coord
        # коствли?
        player.bomb_counter = 0
    player.bomb_counter += 1
    if player.bomb_counter == 4:
        y_bomb = 0
        x_bomb = 0
        player.refractory_period = False




# движение игрока
    y_player = player.y_player
    x_player = player.x_player
    player_new_coord = player.player_move(penetrable_cell_coord)
    #    bomb_description = bomb.put_bomb(lines_filled, bomb_description, step, refractory_period)

    # определение координат монстров и проверка на сьедение игрока
    for monster in my_monsters:
        y_monster, x_monster, monster_direction, monster_id = monster.y_monster, monster.x_monster, monster.direction, monster.id
        monster_old_coord = [y_monster, x_monster]
        monster_new_coord = monster.move(penetrable_cell_coord, step)
        monster.y_monster, monster.x_monster, monster.direction = monster_new_coord
        time.sleep(0.01)
        player.if_player_eaten(monster_new_coord, monster_old_coord)

    # заполнение ИГРОВОГО поля
    lines_filled = deepcopy(lines)
    lines_filled[y_bomb][x_bomb] = 6
    lines_filled[player.y_player][player.x_player] = player.id
    for monster in my_monsters:
        lines_filled[monster.y_monster][monster.x_monster] = monster.id
    playfield_creation(lines_filled, size)
    if not player.is_alive:
        postmorten_steps = postmorten_steps + 1
    step = step + 1
y