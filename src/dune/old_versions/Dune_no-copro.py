import os
import random
from random import choice
import time

NOT_TO_MOVE_OBJECTS = [1, 2, 5]    # 1 - unbreakable walls, 2 - breakable wall, 5 - boundary wall
# PENETRATABLE_OBJECTS = [0, 3, 4]

size = 13
p_walls = 0.3
p_monster = 5 / ((size - 1) ** 2 * 3 // 4)  # (size ** 2 - (size // 2) ** 2)
# ?? формула не понятна

# нулевой лист в листе
x = 0
lines = []
for x in range(size):
    lines.append([0] * size)

# unbreakable and boundary walls
for t in range(size):
    for m in range(size):
        if (t % 2 == 0) and (m % 2 == 0):
            lines[t][m] = 2  # unbreakable walls
        if t == 0 or t == size - 1:
            lines[t][m] = 5  # boundary walls
        if m == 0 or m == size - 1:
            lines[t][m] = 5  # boundary walls

# breakable walls
for t in range(size):
    for m in range(size):
        if lines[t][m] != 2 and lines[t][m] != 5:
            if random.random() < p_walls:
                lines[t][m] = 1  # Walls

# делаем лист с координатами пустых ячеек
empty_cell_coordinates = []
penetratable_cell_coordinates = []
monster_list = []
for y in range(size):
    for x in range(size):
        if lines[y][x] == 0:
            empty_cell_coordinates.append([y, x])
        if lines[y][x] == 0 or lines[y][x] == 3 or lines[y][x] == 4:
            penetratable_cell_coordinates.append([y, x])
# здесь вопрос - почему мы создаем лист с тройками и четверками, если они еще не вводились в программу

# лист с координатами монстров
monster_available_cells = empty_cell_coordinates.copy()
remove_init_position = [[1, 1], [2, 1], [1, 2]]
for i in range(len(remove_init_position)):
    if remove_init_position[i] in monster_available_cells:
        monster_available_cells.remove(remove_init_position[i])

# количество доступных для монстров клеток и их процент в поле
n_empty = len(monster_available_cells)
# print('число доступных для посадки монстров клеток', n_empty)
# print('доля доступных для посадки монстров клеток', n_empty / size ** 2)

monster_list = []
n_monster = random.randint(3, 8)
print('число монстров равно', n_monster)
for i in range(n_monster):
    monster_location = random.randint(0, n_empty)
    y_monster, x_monster = monster_available_cells[monster_location]
    lines[y_monster][x_monster] = 3
    monster_list.append([y_monster, x_monster])  # создаем лист с координатами монстров
monster_list.sort()
print(monster_list, 'list c монстрами сортированный')
print()

# Types of monsters
# lines[t][m] = 3
# monstr1 = Monstr('1', t1, m1, False) - простое движение
# monstr2 = Monstr('2', t2, m2, False) - движение по траектории
# monstr3 = Monstr('3', t3, m3, False)
# monstr4 = Monstr('4', t4, m4, False)

# Player location
lines[1][1] = 4
lines[2][1] = 0
lines[1][2] = 0

# вывести карту
for t in range(size):
    print(lines[t])
print()

# choose the initial direction of each monster
coordinates = [[-1, 0, 'up'], [1, 0, 'down'], [0, -1, 'left'], [0, 1, 'right']]

# ........1.........
# ........|.........
# ........|........x
# 2-------+--------3
# ........|.........
# ........|.........
# ........0.y.......

monster_new_coord = 0

for step in range(10):
    # print('current monster coordinates:', monster_list)
    for i in range(n_monster):
        direction_variants = []
        y_monster, x_monster = monster_list[i]
        # print(y_monster, x_monster, '- первоначальные координаты, ', end='')
        # old_coord.append([x_monster, y_monster])
        for direction_id in range(len(coordinates)):
            y_dir, x_dir, dir_name = coordinates[direction_id]
            y_sum, x_sum = y_monster + y_dir, x_monster + x_dir
            if [y_sum, x_sum] in penetratable_cell_coordinates:
                direction_variants.append([y_sum, x_sum])
                print(y_sum, x_sum, dir_name, direction_id, end='; ')

        if len(direction_variants) > 0:
            monster_new_coord = choice(direction_variants)
            monster_list[i] = monster_new_coord
        y1_monster, x1_monster = monster_new_coord
        lines[y1_monster][x1_monster] = 3
        lines[y_monster][x_monster] = 0
        x_monster = x1_monster
        y_monster = y1_monster
        print(monster_new_coord)

#       for the class 2 monster
    # нада два типа монстров и для второго запомнить направление
    #     if A: variant 1
    #     if B: variant 2
    y_sum, x_sum = y_monster + y_dir, x_monster + x_dir

    print()
    for t in range(size):
        print(lines[t])
    print()

    time.sleep(0.5)
    os.system('cls')

# Monster actions

# print(lines)  # very important shit
# print(len(lines))
# print(len(lines[0]))
# print(lines[2][2])
# lines[2][2] = 1
# print(lines)
# print_game_map(lines)

# print('hi')
# print('hello')
# print('b', end='\n')
# print('b')

# print(lines)  # very important shit
# print(len(lines))
# print(len(lines[0]))
# print(lines[2][2])
# lines[2][2] = 1
# print(lines)





# ДВИЖЕНИЕ ИГОРЬКА
# string_which_was_typed = input('wasd')
#
# if string_which_was_typed == 'd':
#     found_player = False
#     for t in range(size):
#         for m in range(size):
#             if lines[t][m] == 4 and (lines[t][m + 1] not in NOT_TO_MOVE_OBJECTS):
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
#
# for t in range(size):
#     print(lines[t])




