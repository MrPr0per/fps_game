from ctypes import *
import math

# screen
# WIDTH = int(windll.user32.GetSystemMetrics(0) * 0.8)
# HEIGHT = int(windll.user32.GetSystemMetrics(1) * 0.8)
screen_size_scale = 100
WIDTH = 16 * screen_size_scale
HEIGHT = 9 * screen_size_scale
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# game settings
DEBUG = False
VERTICAL_MOVE_HEAD = True
COLLISION = True
FLY_MOD = False

# math
ALMOST_ZERO = 10 ** -5
ALMOST_INFINITY = 10 ** 5

# raycast
FOW_W = 90
FOW_H = int(FOW_W * HEIGHT / WIDTH)
SCALE_N_RAYS = 1/10
NUM_RAYS = int(WIDTH * SCALE_N_RAYS)
COLUMN_WIDTH = WIDTH / NUM_RAYS
DELTA_ANGLE = FOW_W / NUM_RAYS
MAX_DIST_RAY = ALMOST_INFINITY
DIST_TO_SCREEN = NUM_RAYS / (2 * math.tan(math.radians(FOW_W / 2)))
DRAW_ALL_WALS = False
DRAW_ALL_OBJECTS = False
FISH_EYE = False
TEXTURING = True
SHADE_TEXTURES = True
SHADE_OBJECTS = True

# боевка
ATTACK_DIST = 4
ENABLE_AI_ENEMIES = True

# minimap
MINIMAP_SCALE = 5

# костыли
COLLIDE_SCALE = 10000000

# horizon
MAX_DIST_HORIZON = 100
SMOOTHING_HORIZON = 5

# fps
FPS_POS = (WIDTH - 65, 5)
FPS = 120

# const
FORWARD = 'forward'
LEFT = 'left'
RIGHT = 'right'
BACK = 'back'
UP = 'up'
DOWN = 'down'

# phy6
g_const = 9.8
# g_const = 1.6
# g_const = 1

# moving
SPEED = 5
JUMP_SPEED = 4