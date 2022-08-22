import random
import time
from copy import deepcopy
from dune.classes_and_functions_monsters import random_action, direction_variants_identification, playfield_creation, MonsterCat, MonsterDog

NOT_TO_MOVE_OBJECTS = [1, 2, 5]  # 1 - unbreakable walls, 2 - breakable wall, 5 - boundary wall
# PENETRATABLE_OBJECTS = [0, 3, 4, 9]


size = 19
p_walls = 0.3
p_monster = 5 / ((size - 1) ** 2 * 3 // 4)  # (size ** 2 - (size // 2) ** 2)


# создаем нулевой лист в листе
x = 0
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
penetratable_cell_coordinates = []
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
n_monster = random.randint(5, 15)
while n_monster > n_empty:
    n_monster = random.randint(3, 8)

# создаем лист с init координатами монстров
print('число монстров равно', n_monster)
for counter in range(n_monster):
    monster_location = random.randint(0, n_empty)
    y_monster, x_monster = monster_available_cells[monster_location]
    monster_list_init.append([y_monster, x_monster, 'undefined'])
monster_list_init.sort()

# Player and its safespace
lines[1][1] = 9
lines[2][1] = 0
lines[1][2] = 0

# penetr cell coord identification
for y in range(size):
    for x in range(size):
        if lines[y][x] == 0 or lines[y][x] == 3 or lines[y][x] == 4 or lines[y][x] == 9:
            penetratable_cell_coordinates.append([y, x])

# ........1.........
# ........|.........
# ........|........x
# 2-------+--------3
# ........|.........
# ........|.........
# ........0.y.......

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
    my_monsters.append(monster)      # ВАЖНО!my_monsters - лист с обьектами monster, monster - обьект, содержащий информацию о координатах и направлении
    print(monster.y_monster, monster.x_monster, '|', monster.name, '')

# создаем копию листа lines и засаживаем монстрами
lines_filled = deepcopy(lines)
for monster in my_monsters:
    lines_filled[monster.y_monster][monster.x_monster] = monster.id

for step in range(100):
    playfield_creation(lines_filled, size)

    for monster in my_monsters:
        y_monster, x_monster, monster_direction, monster_id = monster.y_monster, monster.x_monster, monster.direction, monster.id
        monster_new_coord = monster.move(penetratable_cell_coordinates, step)
 #       y1_monster, x1_monster, new_monster_direction = monster_new_coord
        monster.y_monster, monster.x_monster, monster.direction = monster_new_coord
        time.sleep(0.2)

    lines_filled = deepcopy(lines)
    for monster in my_monsters:
        lines_filled[monster.y_monster][monster.x_monster] = monster.id



# ДВИЖЕНИЕ ИГОРЬКА
# string_which_was_typed = input('wasd')
#
# if string_which_was_typed == 'd':
#     found_player = False
#     for t in range(size):
#         for m in range(size):
#             if lines[t][m] == 9 and (lines[t][m + 1] not in NOT_TO_MOVE_OBJECTS):
#                 lines[t][m] = 0
#                 lines[t][m + 1] = 4
#                 found_player = True
#             if found_player:
#                 break`                                                                    18
#
# if string_which_was_typed == 'a':
#     found_player = False
#     for t in range(size):
#         for m in range(size):
#             if lines[t][m] == 4 and (lines[t][m - 1] not in NOT_TO_MOVE_OBJECTS):
#                 lines[t][m] = 0
#                 lines[t][m - 1] = 4
#                 found_player = True
#                 break
#         if found_player:
#             break
#
# if string_which_was_typed == 's':
#     found_player = False
#     for t in range(size):
#         for m in range(size):
#             if lines[t][m] == 4 and (lines[t + 1][m] not in NOT_TO_MOVE_OBJECTS):
#                 lines[t][m] = 0
#                 lines[t + 1][m] = 4
#                 found_player = True
#                 break
#         if found_player:
#             break
#
# if string_which_was_typed == 'w':
#     found_player = False
#     for t in range(size):
#         for m in range(size):
#             if lines[t][m] == 4 and (lines[t - 1][m] not in NOT_TO_MOVE_OBJECTS):
#                 time.sleep(1)
#                 lines[t][m] = 0
#                 lines[t - 1][m] = 4
#                 found_player = True
#                 break
#         if found_player:
#             break
