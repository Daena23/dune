SYMBOLS = {0: ' ', 1: '□', 2: '□', 3: '#',
           4: 'Ꙫ', 5: 'ꙮ', 6: 'Ɣ', 7: 'Ѳ',
           8: '҉', 9: 'ⴕ', 10: 'ↂ', 11: 'T', 12: '҉'
           }
# 0 - empty cell, 1 - boundary wall, 2 - intermediate wall, 3 - breakable wall,
# 4 - player, 5 - Hexamebeo, 6 - dogMonster, 7 - bomb,
# 8 - explosion, 9 - grave, 10 - portal, 11 ?, 12 - player_dying

PENETRABLE_OBJECTS = [0, 4, 5, 6, 8, 9, 10, 12]
OBJECTS_TO_STOP_EXPLOSION = [1, 2]
NON_EXPLOSIBLE_OBJECTS = [1, 2, 7] # todo 7 потом убрать
# 3 - breakable wall, 4, 5 - monsters, 6 - bomb,  9 - player, 10 - portal
EXPLOSIBLE_OBJECTS = [3, 4, 5, 6, 7, 10]
OBJECTS_PASSED_BY_THE_EXPLOSION_BEAM = [0, 3, 4, 5, 6, 8, 9, 10, 12]
# SYMBOLS

PLAYER_INIT_POSITIONS = [[1, 1], [2, 1], [1, 2]]


PLAYER_CV = [
    [-1, 0, 'up', 'w', 't'],
    [0, -1, 'left', 'a', 'f'],
    [1, 0, 'down', 's', 'g'],
    [0, 1, 'right', 'd', 'h'],
    [0, 0, 'stay', 'z', 'x'],
]

sumb = '(´ᴥ`)'

EVENTS_JUST_WALK = 'wasdzWASDZ'
EVENTS_PUT_BOMB = 'tfghxTFGHX'

COORD_VARS = [[-1, 0], [0, -1], [1, 0], [0, 1], [0, 0], [0, 0]]
# 0 - up, 1 - left, 2 - down, 3 - right, 4 - noway, 5 - und

# CV = [[-1, 0, 'up'], [0, -1, 'left'],
#       [1, 0, 'down'], [0, 1, 'right'],
#       [1, 0, 'no-way'], [0, 1, 'undefied']
#       ]

# lst = ['up', 'left', 'down', 'right', 'noway', 'und']

