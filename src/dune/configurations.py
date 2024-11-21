from enum import Enum, auto


LEVEL_CONSTANTS = {
    'size': 9,               # field size: odd number,
    'p_walls': 0.2,          # p_wall: 0.1-0.3,
    'init_monster_number': 3,
    'max_bomb_num': 3,
    'bomb_lifetime': 5,      # min_bomb_lifetime: 1,
    'explosion_power': 3,    # min_explosion_explosion_power: 2
    'portal_monster_number': 3,
}


class ObjectId(Enum):
    PortalDeactivated = auto()
    Bomb = auto()
    Player = auto()
    Portal = auto()
    IntermediateWall = auto()
    BoundaryWall = auto()
    BreakableWall = auto()
    MonsterHexamoebo = auto()
    MonsterDog = auto()
    Explosion = auto()


SYMBOLS = {
     0: ' ',  # empty_cell
    'BoundaryWall': '□',
    'IntermediateWall': '□',
    'BreakableWall': '#',
    'Player': 'Ꙋ',
    'Grave': 'ⴕ',
    'MonsterDog': 'Ɣ',
    'MonsterHexamoebo': 'ꙮ',
    'Bomb': 'Ѳ',
    'Explosion': '✷', # explosion
    'ExplosionBeam': '✶',  # explosion: center, corners
    'Destroying': '҉',
    'Portal': '∩',
    'UsedPortal': '֍',
}

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
