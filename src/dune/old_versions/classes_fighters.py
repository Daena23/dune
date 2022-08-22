import random
from copy import deepcopy

rounds = 1

lister = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
lister_copy = deepcopy(lister)
index = input('index')
index = int(index)
for i in range(len(lister)):
    if index == lister[i][3]:
        lister_copy.remove(lister[i])
print('lister_copy', lister_copy)
print(f'lister: {lister}')


class Monster:
    health = 100
    dead_level = 0

class M1(Monster):
    kick_level = random.randint(3, 8)
    defence_level = 0.95

class M2(Monster):
    kick_level = random.randint(1, 15)
    defence_level = 0.85

m1 = M1()  # переменная содержащая класс
m2 = M2()
print('initial states:', Monster.health)
while m1.dead_level <= m1.health and m2.dead_level <= m2.health:
    m1.kick_level = random.randint(3, 40)
    m2.kick_level = random.randint(3, 50)
    print('round: ', rounds)
    m1.health = int(m1.health - m2.kick_level * m1.defence_level)
    print('Сила удара Монстра 2 равна', m2.kick_level, '; После удара у Монстра 1 осталось здоровья:', m1.health)
    m2.health = int(m2.health - m1.kick_level * m2.defence_level)
    print('Сила удара Монстра 1 равна', m1.kick_level, '; После удара у Монстра 2 осталось здоровья:', m2.health)
    if m1.health <= 0 or m2.health <= 0:  # Делаем проверку на соответствие значению окончания боя
        if m1.health <= 0:
            print('winner is Monster2 ')
        elif m2.health <= 0:
            print('winner is Monster1 ')
        elif m1.health <= 0 and m2.health <= 0:
            print('Лежат как два банана два трупа на песке')
        break
    rounds = rounds + 1
