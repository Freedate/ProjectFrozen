
import time
import random
from enum import Enum
import pygame, sys
from pygame.locals import *     # ���̰��� ��� ����ϱ� ����

## ���
FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARD_WIDTH_CNT = 30
BOARD_HEIGHT_CNT = 20
TETRIS_WIDTH_CNT = 5
TETRIS_HEIGHT_CNT = 5
TETRIS_LEFT_GAP = 20
TETRIS_TOP_GAP = 10
BLANK = '.'
# ONMAP = GRAY


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

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

class CharSprite(pygame.sprite.Sprite):
 
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.user_src_image = pygame.image.load(image)
        self.user_position = position
        self.user_speed = 0
        self.jump_speed = 5
        self.is_jumping = False
        self.on_ground = False
        self.origin_pos = position
        self.highst = False
        self.image = self.user_src_image
        self.rect = self.image.get_rect()

 
    def update(self, Map):
        x, y = self.user_position
        tx, ty = self.origin_pos
        x += self.user_speed

        top = TETRIS_TOP_GAP+BOARD_HEIGHT_CNT*BOXSIZE
        bStop = False
        for map_X in range(BOARD_WIDTH_CNT):
            coordX1 = TETRIS_LEFT_GAP+map_X*BOXSIZE
            coordX2 = TETRIS_LEFT_GAP+(map_X+1)*BOXSIZE
            if x >= coordX1 and x < coordX2:
                # 캐릭터가 있는 맵의 x 인덱스
                for map_Y in range(BOARD_HEIGHT_CNT-1,0,-1):
                    if Map[map_Y][map_X] != BLANK:
                        top = TETRIS_TOP_GAP+(map_Y)*BOXSIZE
                        bStop = True
                        break
                if bStop:
                    break

        if self.rect.bottom >= top:
            self.on_ground = True
            self.origin_pos = self.user_position
        else:
            self.on_ground = False

        if self.on_ground==False:
            y += 2
        

        if self.is_jumping:
            if self.highst==True:
                y += self.jump_speed
                if y >= top:
                    self.is_jumping = False
                    self.highst = False
            else :
                y -= self.jump_speed
            if y < top-40:
                self.highst = True

        self.user_position = (x, y)
 
        self.image = self.user_src_image
        self.rect = self.image.get_rect()
        self.rect.center = self.user_position

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

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
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

# variables
m_GameStep = STEP.input.value
m_Map = []
initShape = random.choice(list(PIECES.keys()))
m_fallingTetris = {'shape': initShape,
                'rotation': random.randint(0, len(PIECES[initShape]) - 1),
                'x': int(BOARD_WIDTH_CNT / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
initShape2 = random.choice(list(PIECES.keys()))
m_nextTetris = {'shape': initShape2,
                'rotation': random.randint(0, len(PIECES[initShape2]) - 1),
                'x': int(BOARD_WIDTH_CNT / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}

char = CharSprite('fez.png', (40,300))
char_group = pygame.sprite.RenderPlain(char)




