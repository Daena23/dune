import random
import time
from dune.classes_and_functions_monsters import random_action, direction_variants_identification, action_straight, direction_choice, MonsterCat, MonsterDog

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
    monster_location = random.randint(0, n_empty - 1)
    y_monster, x_monster = monster_available_cells[monster_location]
#    lines[y_monster][x_monster] = 3
    monster_list_init.append([y_monster, x_monster, 'undefined'])  # создаем лист с координатами монстров
monster_list_init.sort()
print(monster_list_init, 'monster_list_init_sorted')
print()


# Player location
lines[1][1] = 9
lines[2][1] = 0
lines[1][2] = 0


# ........1.........
# ........|.........
# ........|........x
# 2-------+--------3
# ........|.........
# ........|.........
# ........0.y.......


monster_list_curr = monster_list_init.copy()

my_monsters = []
for i in range(len(monster_list_curr)):
    monster_description = monster_list_curr[i]
    if random.randint(0, 2) == 0:
        monster = MonsterDog() # переменная содержащая класс
    else:
        monster = MonsterCat()
    monster.y_monster = monster_description[0]
    monster.x_monster = monster_description[1]
    monster.direction = monster_description[2]
    my_monsters.append(monster)
    print('information about monster', monster.y_monster, monster.x_monster, monster.id)

# ВАЖНО!my_monsters - лист с обьектами, monster - обьект, содержащий информацию о координатах и направлении

for counter in range(n_monster):
    if my_monsters[counter].id == "Cat":
        lines[my_monsters[counter].y_monster][my_monsters[counter].x_monster] = 3
    else:
        lines[my_monsters[counter].y_monster][my_monsters[counter].x_monster] = 4

print('init_playfield')
for t in range(size):
    print(lines[t])
print()

for step in range(10):
    for monster in my_monsters:
        y_monster, x_monster, monster_direction, monster_id = monster.y_monster, monster.x_monster, monster.direction, monster.id
        monster_new_coord = monster.move(penetratable_cell_coordinates)

        y1_monster, x1_monster, new_monster_direction = monster_new_coord
        a = lines[y_monster][x_monster]
        lines[y_monster][x_monster] = 0

        lines[y1_monster][x1_monster] = monster_id

        x_monster = x1_monster
        y_monster = y1_monster

        monster.y_monster, monster.x_monster, monster.direction = y1_monster, x1_monster, monster_new_coord[2]
        time.sleep(0.2)
        print('current monster coordinates:', monster.y_monster, monster.x_monster, monster.direction, monster.id)

    for t in range(size):
        print(lines[t])
    print()









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
