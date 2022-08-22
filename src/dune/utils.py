PENETRABLE_OBJECTS = [0, 4, 5, 7, 8, 9]

OBJECTS_TO_STOP_EXPLOSION = [1, 2]
# 1 - boundary wall, 2 - unbreakable intermediate walls, 7 - burst, 8 - grave
NON_EXPLOSIBLE_OBJECTS = [1, 2, 7, 8]
# 3 - breakable wall, 4, 5 - monsters, 6 - bomb,  9 - player, 10 - portal
EXPLOSIBLE_OBJECTS = [0, 3, 4, 5, 6, 7, 8, 9, 10]
OBJECTS_PASSED_BY_THE_EXPLOSION_BEAM = [0, 4, 5, 6, 7, 8, 9]

COORDINATE_VARIANTS = [[-1, 0, 'up'], [0, -1, 'left'], [1, 0, 'down'], [0, 1, 'right']]
PLAYER_COORDINATE_VARIANTS = [
    [-1, 0, 'up', 'w', 't'],
    [0, -1, 'left', 'a', 'f'],
    [1, 0, 'down', 's', 'g'],
    [0, 1, 'right', 'd', 'h'],
    [0, 0, 'stay', 'z', 'x'],
]
INIT_POSITIONS = [[1, 1], [2, 1], [1, 2]]
