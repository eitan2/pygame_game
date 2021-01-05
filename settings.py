# game settings

TITLE = "My Game"

# General
WIDTH = 720
HEIGHT = 400
FPS = 60
FONT_NAME = "arial"

# Player
P_SIZE_X = 30
P_SIZE_Y = 30
P_ACC = 0.5
P_FRICTION = -0.12
P_GRAVITY = 0.5
P_JUMP = -11

# Bullet
B_SIZE_X = 15
B_SIZE_Y = 15
B_COLLIDE = True
B_SPEED = 8
B_LIFETIME = 7 # in seconds

# starting platforms
PLATFORM_LIST = [
(-WIDTH*4, HEIGHT - 40, WIDTH * 8, 40),
(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
(125, HEIGHT - 350, 100, 20),
(350, 200, 100, 20),
(175, 100, 50, 20),
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
YELLOWISH = (255, 200, 25)
LIGHTBLUE = (0, 155, 155)