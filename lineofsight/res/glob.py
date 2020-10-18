PIXEL_WIDTH, PIXEL_HEIGHT = 50, 50
WIDTH, HEIGHT = 1600, 900
FULLSCREEN = 0

TITLE = "LINE OF SIGHT"
DRAW_EDGES = 1
DRAW_GRID = 0
FPS = 500


class colors:
    red = (255, 0, 0)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    lime = (0, 255, 0)
    turq = (64, 224, 208)
    orange = (255, 69, 0)
    white = (255, 255, 255)
    green = (34, 139, 34)
    gray = (128, 128, 128)


class states:
    empty = 0
    wall = 1


UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3
directions = [UP, DOWN, LEFT, RIGHT]