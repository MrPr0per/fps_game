from ctypes import *
# game settings
WIDTH = int(windll.user32.GetSystemMetrics(0) * 0.8)
HEIGHT = int(windll.user32.GetSystemMetrics(1) * 0.8)


HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
DEBUG = False
# minimap
# MINIMAP_SCALE = 10
# MINIMAP_LINE_SCALE = 10
# MINIMAP_WIDTH = 200
# MINIMAP_HEIGHT = 200
# MINIMAP_CENTER_W = MINIMAP_WIDTH / 2
# MINIMAP_CENTER_H = MINIMAP_HEIGHT / 2
# MAP_POS = (0, HEIGHT - MINIMAP_HEIGHT)
# raycast
FOW_W = 120
FOW_H = int(FOW_W * HEIGHT / WIDTH)
SCALE_N_RAYS = 1/7
N_RAYS = int(WIDTH * SCALE_N_RAYS)
DELTA_ANGLE = FOW_W / N_RAYS
MAX_DIST_RAY = 100

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
