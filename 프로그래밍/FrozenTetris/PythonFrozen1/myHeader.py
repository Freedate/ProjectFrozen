import time
import random
from enum import Enum
import pygame, sys
from pygame.locals import *     

FPS = 25
WINDOWWIDTH = 800
WINDOWHEIGHT = 540
SCREEN_SPEED = 2
MOVEBLOCK = 0
MOVECNT = 0
STATE = "GAME"
SCORE = 0

## tetris
BOXSIZE = 16
BOARD_WIDTH_CNT = 48
BOARD_HEIGHT_CNT = 28
MAP_BOARD_GAP = 4
MAP_WIDTH_CNT = BOARD_WIDTH_CNT+MAP_BOARD_GAP
MAP_HEIGHT_CNT = BOARD_HEIGHT_CNT
TETRIS_WIDTH_CNT = 5
TETRIS_HEIGHT_CNT = 5
TETRIS_LEFT_GAP = 20
TETRIS_TOP_GAP = 10
BLANK = '.'

# color
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
# BLOCKTYPE = ('images/block_1.png','images/ground_2.png','images/underground_6.png','images/box.png')
BLOCKTYPE = [('resources/graphics/stage1_sky/tile/ground_1.png','resources/graphics/stage1_sky/tile/ground_2.png','resources/graphics/stage1_sky/tile/ground_3.png','resources/graphics/stage1_sky/tile/ground_4.png','resources/graphics/stage1_sky/tile/ground_5.png','resources/graphics/stage1_sky/tile/ground_6.png','resources/graphics/stage1_sky/tile/underground_1.png','resources/graphics/stage1_sky/tile/underground_2.png','resources/graphics/stage1_sky/tile/underground_3.png','resources/graphics/mainTile/box.png'),
             ('resources/graphics/stage2_desert/tile/ground_1.png','resources/graphics/stage2_desert/tile/ground_2.png','resources/graphics/stage2_desert/tile/ground_3.png','resources/graphics/stage2_desert/tile/ground_4.png','resources/graphics/stage2_desert/tile/ground_5.png','resources/graphics/stage2_desert/tile/ground_6.png','resources/graphics/stage2_desert/tile/underground_1.png','resources/graphics/stage2_desert/tile/underground_2.png','resources/graphics/stage2_desert/tile/underground_3.png','resources/graphics/mainTile/box.png'),
             ('resources/graphics/stage2_desert/tile/ground_1.png','resources/graphics/stage2_desert/tile/ground_2.png','resources/graphics/stage2_desert/tile/ground_3.png','resources/graphics/stage2_desert/tile/ground_4.png','resources/graphics/stage2_desert/tile/ground_5.png','resources/graphics/stage2_desert/tile/ground_6.png','resources/graphics/stage2_desert/tile/underground_1.png','resources/graphics/stage2_desert/tile/underground_2.png','resources/graphics/stage2_desert/tile/underground_3.png','resources/graphics/mainTile/box.png')]
TETRISTYPE = [('resources/graphics/stage1_sky/block/block_1.png','resources/graphics/stage1_sky/block/block_2.png','resources/graphics/stage1_sky/block/block_3.png','resources/graphics/stage1_sky/block/block_4.png','resources/graphics/stage1_sky/block/block_5.png'),
              ('resources/graphics/stage2_desert/block/block_1.png','resources/graphics/stage2_desert/block/block_2.png','resources/graphics/stage2_desert/block/block_3.png','resources/graphics/stage2_desert/block/block_4.png','resources/graphics/stage2_desert/block/block_5.png')]
BACKTYPE = [('resources/graphics/stage1_sky/background/stage_bg1.png','resources/graphics/stage1_sky/background/stage_bg2.png'),
            ('resources/graphics/stage2_desert/background/stage_bg1.png','resources/graphics/stage2_desert/background/stage_bg2.png')]
back1 = {'x':0,'y':0,'width':0,'height':0}
back2 = {'x':0,'y':0,'width':0,'height':0}
backImg1 = pygame.image.load(BACKTYPE[0][0])
backImg2 = pygame.image.load(BACKTYPE[1][1])
BACKIMG = [backImg1,backImg2]

BACK_WIDTH_STAGE2 = 1536
BACK_HEIGHT_STAGE2 = 210
BACK_WIDTH_STAGE2 = 1536
BACK_HEIGHT_STAGE2 = 448

BORDERCOLOR = LIGHTBLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

NETWORK = None

# block type
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '..O..',
                     '..O..',
                     '..O..'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

# step
STEP = Enum('STEP','ready input move check_erase erase check_down gameover gameclear')


# class
class myMap:
    def __init__(self, type, x, y, item):
        self.type = type
        self.x = x
        self.y = y
        self.item = item

class myEnemy:
    def __init__(self,x,y,speed,dir,img,width,height):
        self.x = x
        self.y = y
        self.speed = speed
        self.dir = dir
        self.img = img
        self.width = width
        self.height = height
        self.fall = False
        self.bPop = False

class USER(Enum):
    player0 = 0
    player1 = 1

FEZ_ENEMY_WIDTH1 = 29
FEZ_ENEMY_HEIGHT1 = 25
FEZ_ENEMY_WIDTH2 = 28
FEZ_ENEMY_HEIGHT2 = 37
ENEMY_TYPE = [('resources/graphics/stage1_sky/enemy/enemy_move1.png','resources/graphics/stage1_sky/enemy/enemy_move2.png','resources/graphics/stage1_sky/enemy/enemy_move3.png','resources/graphics/stage1_sky/enemy/enemy_move4.png'),
              ('resources/graphics/stage2_desert/enemy/enemy_move1.png','resources/graphics/stage2_desert/enemy/enemy_move2.png','resources/graphics/stage2_desert/enemy/enemy_move3.png','resources/graphics/stage2_desert/enemy/enemy_move4.png'),
              ('resources/graphics/stage3_parade/enemy/enemy_move1.png','resources/graphics/stage3_parade/enemy/enemy_move2.png','resources/graphics/stage3_parade/enemy/enemy_move3.png','resources/graphics/stage3_parade/enemy/enemy_move4.png')]

# variables
m_GameStep = STEP.ready.value
m_Map = [[0 for col in range(MAP_WIDTH_CNT)] for row in range(MAP_HEIGHT_CNT)]
m_Enemy = []

initShape = random.choice(list(PIECES.keys()))
m_fallingTetris = {'shape': initShape,
                #'rotation': random.randint(0, len(PIECES[initShape]) - 1),
                'rotation': 0,
                'x': int(BOARD_WIDTH_CNT / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(BLOCKTYPE[0])-1)}

#initShape2 = random.choice(list(PIECES.keys()))
#m_nextTetris = {'shape': initShape2,
#                'rotation': random.randint(0, len(PIECES[initShape2]) - 1),
#                'x': int(BOARD_WIDTH_CNT / 2),
#                'y': -2, # start it above the board (i.e. less than 0)
#                'color': random.randint(0, len(BLOCKTYPE[0])-1)}

#### Fez
FEZ_CAMERASLACK = 90
FEZ_MOVERATE = 9
FEZ_BOUNCERATE = 6
FEZ_BOUNCEHEIGHT = 30
FEZ_SPEED = 5
FEZ_WIDTH_SIZE = 27
FEZ_HEIGHT_SIZE = 37
FEZ_START_X = TETRIS_LEFT_GAP+BOXSIZE+30
FEZ_START_Y = TETRIS_TOP_GAP+(BOARD_HEIGHT_CNT-4)*BOXSIZE
FEZ_LEG_LEFT_GAP = 8
FEZ_LEG_RIGHT_GAP = 11
FEZ_FACE_HEIGHT = 14

FEZ_IMG_RIGHT = pygame.image.load('images/char_idle_1.png')
FEZ_IMG_LEFT = pygame.transform.flip(FEZ_IMG_RIGHT,True,False)
FEZ_IMG_RIGHT2 = pygame.image.load('images/char_idle_2.png')
FEZ_IMG_LEFT2 = pygame.transform.flip(FEZ_IMG_RIGHT2,True,False)
FEZ_IMG_RIGHT3 = pygame.image.load('images/char_idle_3.png')
FEZ_IMG_LEFT3 = pygame.transform.flip(FEZ_IMG_RIGHT3,True,False)

FEZ_IMG_RUN_RIGHT = pygame.image.load('images/char_run_1.png')
FEZ_IMG_RUN_LEFT = pygame.transform.flip(FEZ_IMG_RUN_RIGHT,True,False)
FEZ_IMG_RUN_RIGHT2 = pygame.image.load('images/char_run_2.png')
FEZ_IMG_RUN_LEFT2 = pygame.transform.flip(FEZ_IMG_RUN_RIGHT2,True,False)
FEZ_IMG_RUN_RIGHT3 = pygame.image.load('images/char_run_3.png')
FEZ_IMG_RUN_LEFT3 = pygame.transform.flip(FEZ_IMG_RUN_RIGHT3,True,False)

FEZ_IMG_JUMP_RIGHT = pygame.image.load('images/char_jump_1.png')
FEZ_IMG_JUMP_LEFT = pygame.transform.flip(FEZ_IMG_JUMP_RIGHT,True,False)
FEZ_IMG_JUMP_RIGHT2 = pygame.image.load('images/char_jump_2.png')
FEZ_IMG_JUMP_LEFT2 = pygame.transform.flip(FEZ_IMG_JUMP_RIGHT2,True,False)
FEZ_IMG_JUMP_RIGHT3 = pygame.image.load('images/char_jump_3.png')
FEZ_IMG_JUMP_LEFT3 = pygame.transform.flip(FEZ_IMG_JUMP_RIGHT3,True,False)
FEZ_IMG_JUMP_RIGHT4 = pygame.image.load('images/char_jump_4.png')
FEZ_IMG_JUMP_LEFT4 = pygame.transform.flip(FEZ_IMG_JUMP_RIGHT4,True,False)

fez = {'img':FEZ_IMG_RIGHT,'dir':'right','width':FEZ_WIDTH_SIZE,'height':FEZ_HEIGHT_SIZE,
       'topX':FEZ_START_X,'topY':FEZ_START_Y,
       'leftLegX':FEZ_START_X+FEZ_LEG_LEFT_GAP,'rightLegX':FEZ_START_X+FEZ_WIDTH_SIZE-FEZ_LEG_RIGHT_GAP,
       'botY':FEZ_START_Y+FEZ_HEIGHT_SIZE,'jump':9999,'speed':FEZ_SPEED,'stage':1}

fezMoveLeft = False
fezMoveRight = False
fezJump = False
fezFall = False

g_time = time.time()
f_time = time.time()
c_time = time.time()