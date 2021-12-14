from ctypes import *
import math

# game settings
WIDTH = int(windll.user32.GetSystemMetrics(0) * 0.8)
HEIGHT = int(windll.user32.GetSystemMetrics(1) * 0.8)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
DEBUG = False
VERTICAL_MOVE_HEAD = True

# raycast
FOW_W = 90
FOW_H = int(FOW_W * HEIGHT / WIDTH)
SCALE_N_RAYS = 1/7
NUM_RAYS = int(WIDTH * SCALE_N_RAYS)
DELTA_ANGLE = FOW_W / NUM_RAYS
MAX_DIST_RAY = 100
DIST_TO_SCREEN = NUM_RAYS / (2 * math.tan(math.radians(FOW_W / 2)))

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

# math
ALMOST_ZERO = 10 ** -10
ALMOST_INFINITY = 10 ** 10
