LEVEL_CONSTANTS = {'size': 9,             # size - odd,
                   'p_walls': 0.2,        # p_wall - 0.1-0.3,
                   'n_mon': 1,
                   'max_bomb_num': 3,     # min_explosion_power = 2,
                   'bomb_lifetime': 6,    # min_bomb_lifespan = *,
                   'power': 3,            # min_explosion_power = 2
                   'n_mon_from_portal': 3}


ID_DICT = {'PortalDeactivated': -1, 'Bomb': 0, 'Player': 1, 'Portal': 2, 'IntermediateWall': 3, 'BoundaryWall': 4, 'BreakableWall': 5,
           'MonsterHexamoebo': 6, 'MonsterDog': 7,
           'Explosion': 8,
           }

SYMBOLS = {0: ' ',  # empty_cell
           'BoundaryWall': '□', 'IntermediateWall': '□', 'BreakableWall': '#',  # walls
           'Player': 'Ꙋ', 'Grave': 'ⴕ',                 # player
           'MonsterDog': 'Ɣ', 'MonsterHexamoebo': 'ꙮ',  # monsters
           'Bomb': 'Ѳ',                                 # bombs
           'Explosion': '✷', 'ExplosionBeam': '✶',  # explosion: center, corners
           'Destroying': '҉',   # destroying
           'Portal': '∩',       # portal
           'UsedPortal': '',  # used portal
           }
# ▯▮ ꙱⌤ (´ᴥ`)⮟⮞⮜⮝

PLAYER_INIT_COORD = [[1, 1], [2, 1], [1, 2], [3, 1], [1, 3]]

COORD_VARS = [[-1, 0], [0, -1], [1, 0], [0, 1], [0, 0], [0, 0]]
DIR_VARS = {'up': 0, 'left': 1, 'down': 2, 'right': 3, 'no_way': 4, 'undefined': 5}

PLAYER_VARS = [
    [-1, 0, 'up', 'w', 't'],
    [0, -1, 'left', 'a', 'f'],
    [1, 0, 'down', 's', 'g'],
    [0, 1, 'right', 'd', 'h'],
    [0, 0, 'stay', 'z', 'x'],
]

EVENTS_JUST_WALK = 'wasdzWASDZ'
EVENTS_PUT_BOMB = 'tfghxTFGHX'
