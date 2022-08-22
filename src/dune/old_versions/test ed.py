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
for t in range(size):
    for m in range(size):
        if lines[t][m] == 0:
            empty_cell_coordinates.append([t, m])
        if lines[t][m] == 0 or lines[t][m] == 3 or lines[t][m] == 4:
            penetratable_cell_coordinates.append([t, m])
# здесь вопрос - почему мы создаем лист с тройками и четверками, если они еще не вводились в программу

# лист с координатами монстров
monster_available_cells = empty_cell_coordinates.copy()
remove_init_position = [[1, 1], [2, 1], [1, 2]]
for i in range(len(remove_init_position)):
    if remove_init_position[i] in monster_available_cells:
        monster_available_cells.remove(remove_init_position[i])

# Checking
# monster_available_cells.sort
# empty_cell_coordinates.sort
# print(empty_cell_coordinates,'gyuj')
# print()
# print(monster_available_cells)

# количество доступных для монстров клеток и их процент в поле
n_empty = len(monster_available_cells)
# print('число доступных для посадки монстров клеток', n_empty)
# print('доля доступных для посадки монстров клеток', n_empty / size ** 2)

monster_list = []
n_monster = random.randint(3, 8)
print('число монстров равно', n_monster)
for i in range(n_monster):
    monster_location = random.randint(0, n_empty)
    x_monster, y_monster = monster_available_cells[monster_location - 1]
    lines[x_monster][y_monster] = 3
    monster_list.append([x_monster, y_monster])  # создаем лист с координатами монстров
print()
# print(list_monster, 'list c монстрами')
monster_list.sort()
print(monster_list, 'list c монстрами сортированный')
print()

# Types of monstres
# lines[t][m] = 3
# list_mostr.append(3)
# print(list_mostr)
# print(len(list_mostr))
# monstr1 = Monstr('1', t1, m1, False)
# monstr2 = Monstr('2', t2, m2, False)
# monstr3 = Monstr('3', t3, m3, False)
# monstr4 = Monstr('4', t4, m4, False)

lines[1][1] = 4
# lines[2][1] = 0
# lines[1][2] = 0

# вывести карту
for t in range(size):
    print(lines[t])
print()

monstr_new_coord = 0
monster_list_ed = []
                #  alg движение
# создаем массив с новыми координатами для каждого монстра - вверх, вниз, вправо, влево
# в зависимости от сисла направлений ставим рандом на движежние
print(monster_list, 'monster_list')
for i in range(10):
    for i in range(n_monster):
        direction_variants = []
        x_monster, y_monster = monster_list[i]
        print(x_monster, y_monster, ' - первоначальные координаты, ', end='')
        # old_coord.append([x_monster, y_monster])
        # движение вверх
        if [x_monster - 1, y_monster] in penetratable_cell_coordinates:
            direction_variants.append([x_monster - 1, y_monster])
            print([x_monster - 1], [y_monster], ' - можно двигать вверх, ', end='')
        elif lines[x_monster - 1][y_monster] in NOT_TO_MOVE_OBJECTS:
            print('нельзя двигать вверх, ', end='')
        else:
            raise RuntimeError('хуйня кокаято')
        # движение вниз
        if [x_monster + 1, y_monster] in penetratable_cell_coordinates:
            direction_variants.append([x_monster + 1, y_monster])
            print([x_monster + 1], [y_monster], ' - можно двигать вниз, ', end='')
        elif lines[x_monster + 1][y_monster] in NOT_TO_MOVE_OBJECTS:
            print('нельзя двигать вниз, ', end='')
        else:
            raise RuntimeError('хуйня кокаято')
        # движение вправо
        if [x_monster, y_monster + 1] in penetratable_cell_coordinates:
            direction_variants.append([x_monster, y_monster + 1])
            print([x_monster], [y_monster + 1], ' - можно двигать вправо,', end='')
        elif lines[x_monster][y_monster + 1] in NOT_TO_MOVE_OBJECTS:
            print('нельзя двигать вправо, ', end='')
        else:
            raise RuntimeError('хуйня кокаято')
        # движение влево
        if [x_monster, y_monster - 1] in penetratable_cell_coordinates:
            direction_variants.append([x_monster, y_monster - 1])
            print([x_monster], [y_monster - 1], ' - можно двигать влево', end='')
            print()
        elif lines[x_monster][y_monster - 1] in NOT_TO_MOVE_OBJECTS:
            print(' нельзя двигать влево', end='')
            print()
        else:
            raise RuntimeError('хуйня кокаято')
        print('direction_variants=', direction_variants)

        if len(direction_variants) > 0:
            monstr_new_coord = choice(direction_variants)
            monster_list.append(monstr_new_coord)
        elif len(direction_variants) == 0:
            monster_list_ed.append([x_monster, y_monster])
        print(monstr_new_coord, ' monstr_new_coord')
        x1_monster, y1_monster = monstr_new_coord
        lines[x1_monster][y1_monster] = 3
        lines[x_monster][y_monster] = 0
        # ЗАЦИКЛИТЬ ЧТОБЫ КООРД ОБНОВЛЯЛИСЬ
        # Класс монстров
        # print(monster_list_ed, 'monstr_new_coord')
        x_monster = x1_monster
        y_monster = y1_monster

    print()
    print(monster_list,'монстр лист пусть пока лежит там инфа про старые коорд. ')

    print()
    for t in range(size):
        print(lines[t])
    print()


# ВЫБОР НАПРАВЛЕНИЯ

    # lines[x_monster + 1][y_monster] = 3
    #         lines[x_monster][y_monster] = 0
    # lines[x_monster][y_monster + 1] = 3
    #         lines[x_monster][y_monster] = 0
    #        lines[x_monster - 1][y_monster] = 3
    #       lines[x_monster][y_monster] = 0

# ДВИГАЕМ





# for t in range(size):
#     for m in range(size):
#         if lines[t][m] == 3 and lines[t - 1][m] not in NOT_TO_MOVE_OBJECTS:  # вверх
#             lines[t - 1][m] = 3
#             lines[t][m] = 0
#             new_coord.append([t - 1, m])
#             # print(t - 1, m, 'new koord')
#             break
#         elif lines[t][m] == 3 and lines[t][m + 1] not in NOT_TO_MOVE_OBJECTS: # впрво
#             lines[t][m + 1] = 3
#             lines[t][m] = 0
#             new_coord.append([t, m + 1])
#             # print(t, m + 1, 'new koord')
#             break
#         elif lines[t][m] == 3 and lines[t][m - 1] not in NOT_TO_MOVE_OBJECTS:  # влево
#             lines[t][m - 1] = 3
#             lines[t][m] = 0
#             new_coord.append([t, m - 1])
#             # print(t, m - 1, 'new koord')
#             break
#         elif lines[t][m] == 3 and lines[t + 1][m] not in NOT_TO_MOVE_OBJECTS:  # влево
#             lines[t + 1][m] = 3
#             lines[t][m] = 0
#             new_coord.append([t + 1, m])
#             # print(t + 1, m, 'new koord')
#             break
#         elif lines[t][m] == 3 and lines[t + 1][m] not in NOT_TO_MOVE_OBJECTS and lines[t - 1][m] not in NOT_TO_MOVE_OBJECTS and lines[t][m + 1] not in NOT_TO_MOVE_OBJECTS and lines[t][m - 1] not in NOT_TO_MOVE_OBJECTS:
#             print('заперт, коорд: ', t, m)
#             new_coord.append([t, m])
#             break

# # вывести новые сортир коорд
# print(new_coord)
# new_coord.sort()
# print(new_coord,' новые сортировнные коорд')
#
# # вывести карту c переместившимися монстрами
# for t in range(size):
#     print(lines[t])
# print()









        # for i in range(n_monstr):
        #     if t == list_monstr[i][0] and m == list_monstr[i][1]:
        #         print('jr')
        #
        #             list_monstr[i][0] = t - 1
        #             list_monstr[i][1] = m

            #     break
            # if found_monstr:
            #     break

print()

# ДВИЖЕНИЕ МОНСТРОВ
# found_monstr = False
# for t in range(size):
#     for m in range(size):
#       for i in range(size):
#
# print()
# for t in range(size):
#     print(lines[t])


# y = 0
# for x in range(5):
#     for z in range(4):
#         print(y, end='')
#         print(' ', end='')
#     print(y)

# y[2][2] = 1


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
#                 break
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




