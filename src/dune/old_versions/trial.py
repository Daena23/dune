import random
from random import randint
from random import choice
import time

NOT_TO_MOVE_OBJECTS = [1, 2, 5]
# PENETRATABLE_OBJECTS = [0, 3, 4]

size = 13
# нечетное
lines = []
t = 0
m = 0
# нулевой лист
for m in range(size):
    lines.append([0] * size)
    # print(lines[m])
print('a')
t = 0
m = 0
# несбиваемые стены
for m in range(size):
    for t in range(size):
        if m == 0 or m == size - 1 or t == 0 or t == size - 1:
            lines[m][t] = 2
        if t % 2 == 0 and m % 2 == 0:
            lines[m][t] = 2
# сбиваемые стены
t = 0
m = 0
p_walls = 0.3
n_monster_1 = randint(2, 5)
n_monster_2: int = randint(1, 3)
print(n_monster_1, ';', n_monster_2)
for m in range(size):
    for t in range(size):
        if random.random() < p_walls and lines[m][t] == 0:
            lines[m][t] = 1

# расстановка монстров 1 способ
t = 0
m = 0
while n_monster_1 > 0:
    t = randint(0, size - 1)
    m = randint(0, size - 1)
    if lines[m][t] == 0:
        lines[m][t] = 3
        n_monster_1 = n_monster_1 - 1

# расстановка монстров 2 способ
while not n_monster_2 == 0:
    x = randint(0, size - 1)
    y = randint(0, size - 1)
    if lines[y][x] == 0:
        lines[y][x] = 4
        n_monster_2 -= 1

# расстановка игрока - 5 - random coord
bomber = 1
y = 0
x = 0
while not bomber == 0:
    space = False
    x = randint(1, size - 2)
    y = randint(1, size - 2)
    if lines[y][x + 1] == 0 and lines[y + 1][x] == 0 or lines[y][x + 1] == 0 and lines[y - 1][x] == 0 or lines[y - 1][
        x] == 0 and lines[y][x - 1] == 0 or lines[y + 1][x] == 0 and lines[y][x - 1] == 0:
        space = True
    if lines[y][x] == 0 and space:
        lines[y][x] = 5
        bomber = 0
        break
    else:
        m = m + 1

# расстановка игрока - 6
y = 0
x = 0
space = [[0,1], [0,- 1], [1,0][-1,0]]
if lines[y][x]==0


# for y in range(size-1)
# for x in range(size - 1)
#     if lines[m + 1][t + 1] == 0 or lines[m + 1][t - 1] == 0 or lines[m - 1][t + 1] == 0 or lines[m - 1][t - 1] == 0:
#         space = True
#     if lines[m][t] == 0 and space:
#         lines[m][t] = 5
#         bomber = 0
#         break
#     else:
#         m = m + 1


for m in range(size):
    print(lines[m])
