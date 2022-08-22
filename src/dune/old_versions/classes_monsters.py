from random import choice


class Player:
    health = 0
    dead_level = 0
    speed = 0
    id = 4
    coordinates = [0, 0]

    def be_eaten(self, lines):
        self.speed = 0


class Monster:
    health = 0
    dead_level = 0
    speed = 0
    id = "0.0"
    coordinates = [0, 0]

    def player_die(self, lines):
        lines[self.coordinates[0]][self.coordinates[1]] = 0

    def get_kick_by_bomb(self, lines):
        self.health = self.health - 1
        if self.health <= self.dead_level:
            self.die(lines)


class MonsterCat(Monster):
    health = 5
    speed = 15
    id = "1.0"


class MonsterDog(Monster):
    health = 10
    speed = 12
    id = "1.1"


cat = MonsterCat()
dog = MonsterDog()
print(cat.health)
print(dog.health)

monster_list = [cat, dog]

# cat.get_kick_by_bomb(lines)
cat.coordinates = [1, 0]
print(cat.health)
print(dog.health)


# class Monster:
#     health = 1
#     dead_level = 0
#     coordinates = [0, 0]


# y_monster, x_monster = monster_list[i]


# def direction_choice(lines, coordinate_variants):  # рассадка без цикла - для всех типов монстров
#     for step in range(100):
#         # print('current monster coordinates:', monster_list)
#         for i in range(n_monster):
#             for cat - def direction_choice


def direction_choice(y_monster, x_monster, penetratable_cell_coordinates):
    # Функция поиска направления монстром
    coordinate_variants = [[-1, 0, 'up'], [1, 0, 'down'], [0, -1, 'left'], [0, 1, 'right']]
    direction_variants = []
    for direction_id in range(len(coordinate_variants)):
        y_dir, x_dir, dir_name = coordinate_variants[direction_id]
        y_sum = y_monster + y_dir
        x_sum = x_monster + x_dir
        if [y_sum, x_sum] in penetratable_cell_coordinates:
            direction_variants.append([y_sum, x_sum, dir_name])
            # print(y_sum, x_sum, dir_name, end='; ')
    if len(direction_variants) > 0:
        monster_new_coord = choice(direction_variants)
    else:
        monster_new_coord = [y_monster, x_monster, 'no_way']
    # print('monster new coord =', monster_new_coord)
    return monster_new_coord


def action_straight_1 (game_field, x_monster, y_monster, monster_new_coord, penetratable_cell_coordinates):
    y_dir, x_dir, dir_name = monster_new_coord[0, 1, 2]
    for direction_id in range(len(coordinate_variants)):
        y_sum, x_sum = y_monster + coordinate_variants[direction_id][0], x_monster + coordinate_variants[direction_id][
            1]
        if dir_name == coordinate_variants[direction_id][2] and [y_sum, x_sum] in penetratable_cell_coordinates:
            monster_new_coord = y_sum, x_sum, dir_name
            return monster_new_coord
        else:
            direction_choice(game_field, y_monster, x_monster, penetratable_cell_coordinates)

# action_straight(lines, x_monster, y_monster, monster_new_coord, penetratable_cell_coordinates)
