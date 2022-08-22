import os
import random
from random import choice
import time
from classes_monsters import direction_choice
from dune.classes_and_functions_monsters import random_action, direction_variants_identification, action_straight, direction_choice

NOT_TO_MOVE_OBJECTS = [1, 2, 5]  # 1 - unbreakable walls, 2 - breakable wall, 5 - boundary wall
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
monster_list_init = []
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
for counter in range(len(remove_init_position)):
    if remove_init_position[counter] in monster_available_cells:
        monster_available_cells.remove(remove_init_position[counter])


# количество доступных для монстров клеток и их процент в поле

n_empty = len(monster_available_cells)
# print('число доступных для посадки монстров клеток', n_empty)
# print('доля доступных для посадки монстров клеток', n_empty / size ** 2)

monster_list_init = []
n_monster = random.randint(3, 8)
while n_monster > n_empty:
    n_monster = random.randint(3, 8)


print('число монстров равно', n_monster)
for counter in range(n_monster):
    monster_location = random.randint(0, n_empty)
    y_monster, x_monster = monster_available_cells[monster_location]
    lines[y_monster][x_monster] = 3
    monster_list_init.append([y_monster, x_monster, 'indefined'])  # создаем лист с координатами монстров
monster_list_init.sort()
print(monster_list_init, 'monster_list_init_sorted')
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

# ........1.........
# ........|.........
# ........|........x
# 2-------+--------3
# ........|.........
# ........|.........
# ........0.y.......

print('init monster coordinates:', monster_list_init)

monster_list_curr = monster_list_init.copy()


# m1 = MonsterCat()  # переменная содержащая класс
# m2 = MonsterDog()

dir_str = 'no_way'
for step in range(10):
    for counter in range(n_monster):
        y_monster, x_monster = monster_list_curr[counter][0:2]
        y_monster, x_monster = monster_list_curr[counter][0:2]

        # if m1.type == 'cat':
        #     direction_variants = direction_variants_identification(y_monster, x_monster, penetratable_cell_coordinates)
        #     monster_new_coord = random_action(direction_variants)
        # elif m1.type == 'dog':
        if dir_str == 'no_way':
            direction_variants = direction_variants_identification(y_monster, x_monster, penetratable_cell_coordinates)
            monster_new_coord = direction_choice(direction_variants, x_monster, y_monster, penetratable_cell_coordinates)
            monster_dir.append(dir_str)
            print('dir_str =', dir_str)
        else:
            monster_new_coord = action_straight(x_monster, y_monster, penetratable_cell_coordinates, dir_str)

        y1_monster = monster_new_coord[0]
        x1_monster = monster_new_coord[1]
        lines[y_monster][x_monster] = 0
        lines[y1_monster][x1_monster] = 3
        monster_list_curr[counter] = y1_monster, x1_monster
        x_monster \
            = x1_monster
        y_monster = y1_monster
        time.sleep(0.2)
    print('current monster coordinates:', monster_list_curr)
    print()
    for t in range(size):
        print(lines[t])









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
