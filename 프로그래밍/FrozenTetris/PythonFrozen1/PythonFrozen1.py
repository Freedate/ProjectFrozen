from myHeader import *
import pygame, sys
from pygame.locals import *

## functions
def initProcess():
    initMap()
    return     
   
def inputProcess():
    checkForQuit()
    global  fezJump, fezMoveLeft, fezMoveRight, fezFall

    # block move
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
    
    elif pygame.key.get_pressed()[pygame.K_SPACE] != 0:
        print("space")
        fullDown()

    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_UP] != 0:
            print("up")
            maxRot = len(PIECES[m_fallingTetris['shape']])-1
            if m_fallingTetris['rotation']+1 > maxRot:
                m_fallingTetris['rotation'] = 0
            else:
                m_fallingTetris['rotation'] += 1
        # fez move
        if event.type == KEYDOWN:
            if event.key == K_w:
                if fezJump == False and fezFall == False:
                    global c_time
                    c_time = g_time
                    fezJump = True
            if event.key == K_a:
                fezMoveRight = False
                fezMoveLeft = True
                if fez['dir'] != 'left':
                    fez['dir'] = 'left'
                    fez['img'] = FEZ_IMG_LEFT
            if event.key == K_d:
                fezMoveLeft = False
                fezMoveRight = True
                if fez['dir'] != 'right':
                    fez['dir'] = 'right'
                    fez['img'] = FEZ_IMG_RIGHT
        elif event.type == KEYUP:
            if event.key == K_a:
                fezMoveLeft = False
            if event.key == K_d:
                fezMoveRight = False
            if event.key == K_w:
                fezJump = False
    return

fez_time = time.time()
tetris_time = time.time()
tetris_new_gap = 0
def dataProcess():
    global m_GameStep
    global m_fallingTetris
    global tetris_time, fez_time, f_time
    
    curTime = time.time()

    moveComponents()

    # fez
    if curTime-fez_time >= 0.1:
        fez_time = time.time()
        imgSprite()

    moveFez()
    jumpFez()
    if collisionBlockDown(fez['leftLegX'],fez['rightLegX'],fez['botY']+5) == False:
       fallFez()


    # tetris
    if curTime-tetris_time >= 0.3:
        tetris_time = time.time()
        if m_GameStep == STEP.ready.value:
            m_fallingTetris = newTetris()
            if m_fallingTetris != None:
                m_newTetris = newTetris()
            m_GameStep = STEP.input.value
        elif m_GameStep == STEP.input.value:
            if isBlocked():
                setOnMap()
                m_GameStep = STEP.ready.value
            else:
                m_fallingTetris['y'] += 1

        elif m_GameStep == STEP.gameover.value:
            m_GameStep = STEP.ready.value

    return

def renderProcess():
    DISPLAYSURF.fill(BLACK)
    drawMovingTetris()
    drawBoard()
    drawFez()
    drawBound()

    pygame.display.update()
    FPSCLOCK.tick(FPS)
    return

def releaseProcess():
    return

def mainLoop():
    global g_time
    curTime = time.time()
    inputProcess()
    if curTime - g_time >= 0.0001:
        dataProcess()
        g_time = time.time()
    renderProcess()

# init
def initMap():
    for i in range(MAP_HEIGHT_CNT):
        for j in range(MAP_WIDTH_CNT):
            m_Map[i][j] = myMap(BLANK,0,0,0)

    for i in range(MAP_HEIGHT_CNT):
        for j in range(MAP_WIDTH_CNT):
            m_Map[i][j].x = TETRIS_LEFT_GAP+j*BOXSIZE
            m_Map[i][j].y = TETRIS_TOP_GAP+i*BOXSIZE

    # 밑바닥 맵 랜덤
    for i in range(MAP_WIDTH_CNT):
        m_Map[MAP_HEIGHT_CNT-1][i].type = 2
    for i in range(MAP_WIDTH_CNT):
        m_Map[MAP_HEIGHT_CNT-2][i].type = 2


    # 밑바닥-2 맵 랜덤
    for i in range(MAP_WIDTH_CNT):
        ranNum = random.randint(0,5)
        if ranNum == 0:
            (m_Map[MAP_HEIGHT_CNT-3][i]).type = BLANK
        elif ranNum == 1:
            (m_Map[MAP_HEIGHT_CNT-3][i]).type = 0
        elif ranNum == 2:
            (m_Map[MAP_HEIGHT_CNT-3][i]).type = 1
        elif ranNum == 3:
            (m_Map[MAP_HEIGHT_CNT-3][i]).type = 2
        elif ranNum == 4:
            (m_Map[MAP_HEIGHT_CNT-3][i]).type = 3


    for i in range(MAP_WIDTH_CNT-1,int(MAP_WIDTH_CNT/2),-1):
        m_Map[MAP_HEIGHT_CNT-8][i].type = 3
# input

def checkDown():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X, map_Y = convertBlockIdxToMapIdx(x,y,m_fallingTetris)
                if map_Y+1 >= BOARD_HEIGHT_CNT:
                    return False
                if m_Map[map_Y+1][map_X].type != BLANK:
                    return False
    return True

def checkLeftRight(num):
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X, map_Y = convertBlockIdxToMapIdx(x,y,m_fallingTetris)
                if m_Map[map_Y][map_X+num].type != BLANK:
                    return False
                if map_X+num<0 or map_X+num>=BOARD_WIDTH_CNT-1:
                    return False
    return True

def fullDown():
    while True:
        for x in range(TETRIS_WIDTH_CNT):
            for y in range(TETRIS_HEIGHT_CNT):
                if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                    map_X, map_Y = convertBlockIdxToMapIdx(x,y,m_fallingTetris)
                    if map_Y+1 >= BOARD_HEIGHT_CNT:
                        setOnMap()
                        m_GameStep = STEP.check_erase.value
                        return
                    if m_Map[map_Y+1][map_X].type != BLANK:
                        setOnMap()
                        m_GameStep = STEP.check_erase.value
                        return
        m_fallingTetris['y'] += 1
        
# data
def resetMap():
    # 사라진 맵 pop
    for i in range(MAP_HEIGHT_CNT):
        for j in range(MAP_BOARD_GAP):
            m_Map[i].pop(0)
    
    # new 맵 extend
    for i in range(MAP_HEIGHT_CNT):
        m_Map[i].extend([0,0,0,0])
    for i in range(MAP_WIDTH_CNT-MAP_BOARD_GAP,MAP_WIDTH_CNT,1):
        for j in range(MAP_HEIGHT_CNT):
            if j >= MAP_HEIGHT_CNT-2:
                m_Map[j][i] = myMap(2,TETRIS_LEFT_GAP+i*BOXSIZE,TETRIS_TOP_GAP+j*BOXSIZE,0)
            else:
                m_Map[j][i] = myMap(BLANK,TETRIS_LEFT_GAP+i*BOXSIZE,TETRIS_TOP_GAP+j*BOXSIZE,0)

def moveComponents():
    for x in range(MAP_WIDTH_CNT):
        for y in range(MAP_HEIGHT_CNT):
            m_Map[y][x].x -= SCREEN_SPEED
    fez['topX'] -= SCREEN_SPEED
    fez['rightLegX'] -= SCREEN_SPEED
    fez['leftLegX'] -= SCREEN_SPEED
    global MOVEBLOCK, MOVECNT
    MOVEBLOCK += SCREEN_SPEED
    if MOVEBLOCK % BOXSIZE == 0 :
        MOVECNT += 1
        if MOVECNT >= 4:
            resetMap()
            if m_GameStep == STEP.input.value:
                m_fallingTetris['x'] -= MAP_BOARD_GAP
            MOVECNT = 0


def newTetris():
    global MOVECNT
    shape = random.choice(list(PIECES.keys()))
    newBox = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARD_WIDTH_CNT / 2 + MOVECNT),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(BLOCKTYPE)-1)}
    return newBox

def isBlocked():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X, map_Y = convertBlockIdxToMapIdx(x,y,m_fallingTetris)
                if map_Y+1 >= BOARD_HEIGHT_CNT-1:
                    return True
                if m_Map[map_Y+1][map_X].type != BLANK:
                    return True
    return False

def setOnMap():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_X, map_Y = convertBlockIdxToMapIdx(x,y,m_fallingTetris)
                m_Map[map_Y][map_X].type = m_fallingTetris['color']

def convertBlockIdxToMapIdx(x, y, tetris):
    # 테트리스 블럭 인덱스를 맵의 인덱스로 변환
    map_X = tetris['x']
    map_Y = tetris['y']
    map_X += x
    map_Y += y
    return map_X, map_Y

def convertMapIdxToPixel(mapx, mapy):
    x = TETRIS_LEFT_GAP+mapx*BOXSIZE
    y = TETRIS_TOP_GAP+mapy*BOXSIZE
    return x, y

def convertBlockIdxToPixel():
    i=0
def convertPixelToMapIdx(x,y):
    # 화면의 좌표를 맵의 인덱스로 변환
    mapIdxX=0
    mapIdxY=0
    for i in range(BOARD_HEIGHT_CNT):
        for j in range(BOARD_WIDTH_CNT):
            if x >= m_Map[i][j].x and x < m_Map[i][j].x+BOXSIZE:
                if y >= m_Map[i][j].y and y < m_Map[i][j].y+BOXSIZE:
                    mapIdxX = j
                    mapIdxY = i
                    break
    return mapIdxX, mapIdxY

#def collisionBlockDown(leftx, rightx, y):
#    global fezFall, f_time

#    fez_leftX, fez_legY = convertPixelToMapIdx(fez['leftLegX']-5, fez['botY']+5)
#    fez_rightX, fez_legY = convertPixelToMapIdx(fez['rightLegX']-5, fez['botY']+5)
    
#    if fez_legY != 0 and fez_legY<BOARD_HEIGHT_CNT:
#        if m_Map[fez_legY][fez_leftX] == BLANK and m_Map[fez_legY][fez_rightX] == BLANK:
#            fezFall = False
#            return False
#    if fezFall == False:
#        f_time = time.time()
#        fezFall = True
#    return True

def collisionUp():
    fezHeadRect = pygame.Rect(fez['topX']+10,fez['topY'],fez['width']-20,fez['width']-10)
    for i in range(BOARD_HEIGHT_CNT-1,0,-1):
        for j in range(BOARD_WIDTH_CNT):
            if m_Map[i][j].type != BLANK:
                # x,y = convertMapIdxToPixel(j,i)
                blockRect = pygame.Rect(m_Map[i][j].x,m_Map[i][j].y,BOXSIZE,BOXSIZE)
                if fezHeadRect.colliderect(blockRect):
                    return j,i
    return -1,-1

def collisionBlockDown(leftx, rightx, y):
    global f_time, fezFall
    charMapX_l, charMapY = convertPixelToMapIdx(leftx-5,y)
    charMapX_r, charMapY = convertPixelToMapIdx(rightx-5,y)
    
    legRect = pygame.Rect(leftx,y-16,10,16)           # fez 하체 직사각형
         
    # leftMapX, leftMapY = convertMapIdxToPixel(charMapX_l,charMapY)
    leftMapX = m_Map[charMapY][charMapX_l].x
    leftMapY = m_Map[charMapY][charMapX_l].y
    leftMapRect = pygame.Rect(leftMapX-3,leftMapY-3,BOXSIZE+6,BOXSIZE+6)
    # rightMapX, rightMapY = convertMapIdxToPixel(charMapX_r,charMapY)
    rightMapX = m_Map[charMapY][charMapX_r].x
    rightMapY = m_Map[charMapY][charMapX_r].y
    rightMapRect = pygame.Rect(rightMapX-3,rightMapY-3,BOXSIZE+6,BOXSIZE+6)

    # 바닥에 닿은 경우
    if m_Map[charMapY][charMapX_l].type != BLANK and legRect.colliderect(leftMapRect):
        fez['botY'] = leftMapY
        fez['topY'] = fez['botY']-fez['height']
        fez['jump'] = 9999
        fezFall = False
        return True
    if m_Map[charMapY][charMapX_r].type != BLANK and legRect.colliderect(rightMapRect):
        fez['botY'] = rightMapY
        fez['topY'] = fez['botY']-fez['height']
        fez['jump'] = 9999
        fezFall = False
        return True
    # 바닥이 없는 경우
    if fezFall == False:
        f_time = time.time()
        fezFall = True
    return False


def moveFez():
    if fezMoveLeft == True:
        #print("fezleft")
        fez_topX, fez_topY = convertPixelToMapIdx(fez['topX']-fez['speed'], fez['topY'])
        fez_faceX, fez_faceY = convertPixelToMapIdx(fez['topX']-fez['speed'], fez['topY']+FEZ_FACE_HEIGHT)
        fez_legX, fez_legY = convertPixelToMapIdx(fez['leftLegX']-5-fez['speed'], fez['botY']-5)
        if m_Map[fez_topY][fez_topX].type == BLANK and m_Map[fez_faceY][fez_faceX].type == BLANK and m_Map[fez_legY][fez_legX].type == BLANK:
            fez['topX'] -= fez['speed']
            fez['leftLegX'] = fez['topX'] + FEZ_LEG_RIGHT_GAP
            fez['rightLegX'] = fez['topX'] + (FEZ_WIDTH_SIZE-FEZ_LEG_LEFT_GAP)

    elif fezMoveRight == True:
        #print("fezright")
        fez_topX, fez_topY = convertPixelToMapIdx(fez['topX']+fez['speed']+fez['width']/2, fez['topY'])
        fez_faceX, fez_faceY = convertPixelToMapIdx(fez['topX']+fez['speed']+fez['width']/2, fez['topY']+FEZ_FACE_HEIGHT)
        fez_legX, fez_legY = convertPixelToMapIdx(fez['rightLegX']-5+fez['speed'], fez['botY']-5)
        if m_Map[fez_topY][fez_topX].type == BLANK and m_Map[fez_faceY][fez_faceX].type == BLANK and m_Map[fez_legY][fez_legX].type == BLANK:
            fez['topX'] += fez['speed']
            fez['leftLegX'] = fez['topX'] + FEZ_LEG_LEFT_GAP
            fez['rightLegX'] = fez['topX'] + (FEZ_WIDTH_SIZE-FEZ_LEG_RIGHT_GAP)


def fallFez():
    global g_time, f_time
    if fezJump == False:
        if collisionBlockDown(fez['leftLegX'],fez['rightLegX'],fez['botY']) == True:
            fez['jump'] = 9999
        vel = g_time - f_time
        v = -vel*20
        print(v)
        
        fez['jump'] = v
        fez['topY'] = fez['topY'] - v
        fez['botY'] = fez['topY'] + fez['height']

def jumpFez():
    global fezJump, g_time, c_time, f_time
    if fezJump:
        mapX, mapY = collisionUp()
        if mapX == -1:
            # 부딪친 블럭이 없을 때
            vel = g_time - c_time
            v = 25 - vel*100
            fez['jump'] = v     # v가 +면 올라가는 중
            fez['topY'] = fez['topY'] - v
            fez['botY'] = fez['topY'] + fez['height']

            if v<=0:
                # 최고점
                fezJump = False
                fezFall = True
        else:
            # 부딪친 블럭이 있을 때
            fezJump = False
            fezFall = True
            f_time = time.time()


# render
def drawBoard():
    for y in range(MAP_HEIGHT_CNT):
        for x in range(MAP_WIDTH_CNT):
            drawBox(m_Map[y][x].y, m_Map[y][x].x, m_Map[y][x].type)
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (TETRIS_LEFT_GAP, TETRIS_TOP_GAP, (BOARD_WIDTH_CNT * BOXSIZE) + 8, (BOARD_HEIGHT_CNT * BOXSIZE) + 8), 5)

def drawBound():
    pygame.draw.rect(DISPLAYSURF, BLACK, (0,TETRIS_TOP_GAP-5,TETRIS_LEFT_GAP-2,BOARD_HEIGHT_CNT*BOXSIZE+30))
    # pygame.draw.rect(DISPLAYSURF, BLACK, (TETRIS_LEFT_GAP+BOARD_WIDTH_CNT*BOXSIZE+5,TETRIS_TOP_GAP-5,0,BOARD_HEIGHT_CNT*BOXSIZE+30))
    pygame.draw.rect(DISPLAYSURF, BLACK, (TETRIS_LEFT_GAP+BOARD_WIDTH_CNT*BOXSIZE+5,TETRIS_TOP_GAP-5,1,BOARD_HEIGHT_CNT*BOXSIZE+30))

def drawBox(y,x,color):
    if color==BLANK:
        return
    blockImg = pygame.image.load(BLOCKTYPE[color])
    # blockRect = pygame.Rect((TETRIS_LEFT_GAP+x*BOXSIZE+6,TETRIS_TOP_GAP+y*BOXSIZE+5,BOXSIZE-1,BOXSIZE-1))
    blockRect = pygame.Rect((x,y,BOXSIZE-1,BOXSIZE-1))
    DISPLAYSURF.blit(blockImg,blockRect)
    # pygame.draw.rect(DISPLAYSURF,COLORS[color],(TETRIS_LEFT_GAP+x*BOXSIZE+6,TETRIS_TOP_GAP+y*BOXSIZE+5,BOXSIZE-1,BOXSIZE-1))

def drawMovingTetris():
    for x in range(TETRIS_WIDTH_CNT):
        for y in range(TETRIS_HEIGHT_CNT):
            if PIECES[m_fallingTetris['shape']][m_fallingTetris['rotation']][y][x] != BLANK:
                map_Xi, map_Yi = convertBlockIdxToMapIdx(x,y,m_fallingTetris)
                #map_X, map_Y = convertMapIdxToPixel(map_X,map_Y)
                map_X = m_Map[map_Yi][map_Xi].x
                map_Y = m_Map[map_Yi][map_Xi].y
                drawBox(map_Y,map_X,m_fallingTetris['color'])

def drawFez():
    fez['rect'] = pygame.Rect((fez['topX'],fez['topY'],fez['width'],fez['height']))
    DISPLAYSURF.blit(fez['img'],fez['rect'])


def imgSprite():
    
    if fezJump == True:
        if fez['jump'] >= 0:
            # 올라가는중
            if fez['dir'] == 'right':
                if fez['img'] == FEZ_IMG_JUMP_RIGHT:
                    fez['img'] = FEZ_IMG_JUMP_RIGHT2
                else:
                    fez['img'] = FEZ_IMG_JUMP_RIGHT
            else:
                if fez['img'] == FEZ_IMG_JUMP_LEFT:
                    fez['img'] = FEZ_IMG_JUMP_LEFT2
                else:
                    fez['img'] = FEZ_IMG_JUMP_LEFT
        else:
            # 내려가는중
            if fez['dir'] == 'right':
                if fez['img'] == FEZ_IMG_JUMP_RIGHT3:
                    fez['img'] = FEZ_IMG_JUMP_RIGHT4
                else:
                    fez['img'] = FEZ_IMG_JUMP_RIGHT3
            else:
                if fez['img'] == FEZ_IMG_JUMP_LEFT3:
                    fez['img'] = FEZ_IMG_JUMP_LEFT4
                else:
                    fez['img'] = FEZ_IMG_JUMP_LEFT3
    elif fezMoveLeft == True:
        if fez['img'] == FEZ_IMG_RUN_LEFT:
            fez['img'] = FEZ_IMG_RUN_LEFT2
        elif fez['img'] == FEZ_IMG_RUN_LEFT2:
            fez['img'] = FEZ_IMG_RUN_LEFT3
        else:
            fez['img'] = FEZ_IMG_RUN_LEFT
    elif fezMoveRight == True:
        if fez['img'] == FEZ_IMG_RUN_RIGHT:
            fez['img'] = FEZ_IMG_RUN_RIGHT2
        elif fez['img'] == FEZ_IMG_RUN_RIGHT2:
            fez['img'] = FEZ_IMG_RUN_RIGHT3
        else:
            fez['img'] = FEZ_IMG_RUN_RIGHT
    else:
        if fez['dir'] == 'right':
            if fez['img'] == FEZ_IMG_RIGHT:
                fez['img'] = FEZ_IMG_RIGHT2
            elif fez['img'] == FEZ_IMG_RIGHT2:
                fez['img'] = FEZ_IMG_RIGHT3
            else:
                fez['img'] = FEZ_IMG_RIGHT

        else:
            if fez['img'] == FEZ_IMG_LEFT:
                fez['img'] = FEZ_IMG_LEFT2
            elif fez['img'] == FEZ_IMG_LEFT2:
                fez['img'] = FEZ_IMG_LEFT3
            else:
                fez['img'] = FEZ_IMG_LEFT
# release

#### other functions
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
    # showTextScreen('EDGE')
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