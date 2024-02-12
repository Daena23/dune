SYMBOLS = {0: ' ', 1: '□', 2: '□', 3: '#',  # walls
           4: 'Ꙋ', 5: 'ⴕ',                  # players
           6: 'ꙮ', 7: 'Ɣ',                  # monsters
           8: 'Ѳ',                          # bombs
           9: '✷', 10: '✶', 11: '҉',        # explosion: center, corners, destroying
           12: '🌕',                         # portal
           13: '',                         # used portal
           }
# ▯▮ ꙱⌤   sumb = '(´ᴥ`)' ⮟⮞⮜⮝
PENETRABLE_OBJECTS = [0, 4, 5, 6, 7, 9, 10, 11, 12]
OBJECTS_TO_STOP_EXPLOSION = [1, 2]
NON_EXPLOSIBLE_OBJECTS = [1, 2, 5, 8]  # todo 7 потом убрать
EXPLOSIBLE_OBJECTS = [3, 4, 6, 7, 8]
OBJECTS_PASSED_BY_THE_EXPLOSION_BEAM = [0, 4, 5, 6, 7, 9, 10, 11, 12]

PLAYER_INIT_POSITIONS = [[1, 1], [2, 1], [1, 2]]

COORD_VARS = [[-1, 0], [0, -1], [1, 0], [0, 1], [0, 0], [0, 0]]
# lst = ['up', 'left', 'down', 'right', 'noway', 'und']

PLAYER_COORD_VARS = [
    [-1, 0, 'up', 'w', 't'],
    [0, -1, 'left', 'a', 'f'],
    [1, 0, 'down', 's', 'g'],
    [0, 1, 'right', 'd', 'h'],
    [0, 0, 'stay', 'z', 'x'],
]

EVENTS_JUST_WALK = 'wasdzWASDZ'
EVENTS_PUT_BOMB = 'tfghxTFGHX'


