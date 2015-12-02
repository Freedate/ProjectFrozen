# -*- coding: utf-8 -*-
from myHeader import *
import pygame, sys
from pygame.locals import *     # 파이게임 상수 사용하기 위해

## functions
def checkDown():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X = m_fallingTetris['x']
                map_Y = m_fallingTetris['y']
                map_X += x
                map_Y += y
                if map_Y+1 >= BOARD_HEIGHT_CNT: # 맵의 바닥이면
                    return False
                if m_Map[map_Y+1][map_X] != BLANK:    # 이미 쌓인 블럭이 있으면
                    return False
    return True

def checkLeftRight(num):
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X = m_fallingTetris['x']
                map_Y = m_fallingTetris['y']
                map_X += x
                map_Y += y
                if m_Map[map_Y][map_X+num] != BLANK:    # 이미 쌓인 블럭이 있으면
                    return False
    return True

def fullDown():
    while True:
        for x in range(TETRIS_WIDTH_CNT):
            for y in range(TETRIS_HEIGHT_CNT):
                if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                    map_X = m_fallingTetris['x']
                    map_Y = m_fallingTetris['y']
                    map_X += x
                    map_Y += y
                    if map_Y+1 >= BOARD_HEIGHT_CNT: # 맵의 바닥이면
                        setOnMap()
                        m_GameStep = STEP.check_erase.value
                        return
                    if m_Map[map_Y+1][map_X] != BLANK:    # 이미 쌓인 블럭이 있으면
                        setOnMap()
                        m_GameStep = STEP.check_erase.value
                        return
        m_fallingTetris['y'] += 1
                

def initProcess():
    initMap()

    

    return

def inputProcess():
    checkForQuit()

    if pygame.key.get_pressed()[pygame.K_DOWN] != 0:
        if checkDown() == True:
            print("down")
            m_fallingTetris['y'] += 1

    elif pygame.key.get_pressed()[pygame.K_LEFT] != 0:
        if checkLeftRight(-1) == True:
            print("left")
            m_fallingTetris['x'] -= 1

    elif pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
        if checkLeftRight(1) == True:
            print("right")
            m_fallingTetris['x'] += 1


    else:
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_UP] != 0:
                print("up")
                maxRot = len(PIECES[m_fallingTetris['shape']])-1
                if m_fallingTetris['rotation']+1 > maxRot:
                    m_fallingTetris['rotation'] = 0
                else:
                    m_fallingTetris['rotation'] += 1
            elif pygame.key.get_pressed()[pygame.K_SPACE] != 0:
                print("space")
                fullDown()
            elif pygame.key.get_pressed()[pygame.K_w] != 0:
                print(char.on_ground)
                if char.on_ground:
                    char.is_jumping = True
            elif pygame.key.get_pressed()[pygame.K_d] != 0:
                char.user_speed = 10
            elif pygame.key.get_pressed()[pygame.K_a] != 0:
                char.user_speed = -10
            else:
                char.user_speed = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
 
            

    
    return

g_time = time.time()
def dataProcess():
    global m_GameStep, m_fallingTetris, g_time
    curTime = time.time()
    if curTime - g_time >= 0.5:
        if m_GameStep == STEP.ready.value:
            m_fallingTetris = newTetris()
            m_newTetris = newTetris()
            m_GameStep = STEP.input.value
        elif m_GameStep == STEP.input.value:
            if isBlocked():
                setOnMap()
                m_GameStep = STEP.check_erase.value
            else:
                m_fallingTetris['y'] += 1
        elif m_GameStep == STEP.check_erase.value:
            m_GameStep = STEP.erase.value
        
        elif m_GameStep == STEP.erase.value:
            m_GameStep = STEP.gameover.value
        
        elif m_GameStep == STEP.gameover.value:
            m_GameStep = STEP.ready.value
        curTime = time.time()
    char_group.update(m_Map)

    return

def renderProcess():
    global char, char_group
    DISPLAYSURF.fill(BLACK)
    drawBoard()
    drawMovingTetris()

    #char_group.clear(DISPLAYSURF, background)

    char_group.draw(DISPLAYSURF)
    pygame.display.flip()

    pygame.display.update()
    FPSCLOCK.tick(FPS)


    return

def releaseProcess():
    return

def mainLoop():
    inputProcess()
    dataProcess()
    renderProcess()

# init
def initMap():
    for i in range(BOARD_HEIGHT_CNT):
        m_Map.append([BLANK]*BOARD_WIDTH_CNT)
    for i in range(BOARD_WIDTH_CNT):
        m_Map[BOARD_HEIGHT_CNT-1][i] = 3
# input

# data
def newTetris():
    shape = random.choice(list(PIECES.keys()))
    newBox = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARD_WIDTH_CNT / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return newBox

def isBlocked():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                # 그 조각이 blank가 아니면
                # 맵에서의 좌표를 가져온다.
                map_X = m_fallingTetris['x']
                map_Y = m_fallingTetris['y']
                map_X += x
                map_Y += y
                if map_Y+1 >= BOARD_HEIGHT_CNT: # 맵의 바닥이면
                    return True
                if m_Map[map_Y+1][map_X] != BLANK:    # 이미 쌓인 블럭이 있으면
                    return True
    return False

def setOnMap():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X = m_fallingTetris['x']
                map_Y = m_fallingTetris['y']
                map_X += x
                map_Y += y
                m_Map[map_Y][map_X] = m_fallingTetris['color']

# Fez Data Process
#def charUpdate():
#    global char
#    x,y = char.user_position
#    x += char.user_speed

#    if char.rect.bottom >= ground[1].rect.top:
#        char.on_ground = True
#        char.origin_pos = char.user_position
#    else:
#        char.on_ground = False


# render
def drawBoard():
    # 테두리 그리기
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (TETRIS_LEFT_GAP, TETRIS_TOP_GAP, (BOARD_WIDTH_CNT * BOXSIZE) + 8, (BOARD_HEIGHT_CNT * BOXSIZE) + 8), 5)
    # 맵 그리기
    for y in range(BOARD_HEIGHT_CNT):
        for x in range(BOARD_WIDTH_CNT):
            drawBox(y, x, m_Map[y][x])
def drawBox(y,x,color):
    if color==BLANK:
        return
    pygame.draw.rect(DISPLAYSURF,COLORS[color],(TETRIS_LEFT_GAP+x*BOXSIZE+6,TETRIS_TOP_GAP+y*BOXSIZE+5,BOXSIZE-1,BOXSIZE-1))

def drawMovingTetris():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X = m_fallingTetris['x']
                map_Y = m_fallingTetris['y']
                map_X += x
                map_Y += y
                drawBox(map_Y,map_X,m_fallingTetris['color'])
# release

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def checkForKeyPress():
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

#### main
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('EDGE')
    # showTextDISPLAYSURF('EDGE')
    # pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (TETRIS_LEFT_GAP, TETRIS_TOP_GAP, (TETRIS_LEFT_GAP * BOXSIZE) + 8, (BOARD_HEIGHT_CNT * BOXSIZE) + 8), 5)

    #while checkForKeyPress() == None:
    #    pygame.display.update()
    #    FPSCLOCK.tick()


    # start game
    initProcess()
    while True:
        mainLoop()

    releaseProcess()






## function calls
main()
