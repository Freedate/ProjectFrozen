#! /usr/bin/env python

import sys
from random import choice
import pygame
from pygame.locals import *
from block import O, I, S, Z, L, J, T

COLS = 10
ROWS = 20
CELLS = COLS * ROWS
CELLPX = 16
POS_FIRST_APPEAR = 5
SCREEN_SIZE = (COLS*CELLPX, ROWS*CELLPX)
COLOR_BG = (0,0,0)

def draw(grid, pos=None):
    if pos: # 6x5
        s = pos - 3 - 2 * COLS # upper left position
        for p in range(0, 5):
            q = s + p * COLS
            for i in range(q, q+6):
                if 0 <= i < CELLS:
                    c = eval(grid[i]+".color") if grid[i] else COLOR_BG
                    screen.fill(c, (i%COLS*CELLPX, i/COLS*CELLPX, CELLPX, CELLPX))
    else: # all
        screen.fill(COLOR_BG)
        for i, occupied in enumerate(grid):
            if occupied:
                c = eval(grid[i]+".color")
                screen.fill(c, (i%COLS*CELLPX, i/COLS*CELLPX, CELLPX, CELLPX))
    pygame.display.flip()

def phi(grid1, grid2, pos): # 4x4
    s = pos - 2 - 1 * COLS # upper left position
    for p in range(0, 4):
        q = s + p * COLS
        for i in range(q, q+4):
            try:
                if grid1[i] and grid2[i]:
                    return False
            except:
                pass
    return True

def merge(grid1, grid2):
    grid = grid1[:]
    for i,c in enumerate(grid2):
        if c:
            grid[i] = c
    return grid

def complete(grid):
    n = 0
    for i in range(0, CELLS, COLS):
        if not None in grid[i:i+COLS]:
            grid = [None]*COLS + grid[:i] + grid[i+COLS:]
            n += 1
    return grid, n

def max_pos(grid, block, pos):
    while True:
        grid_block = block.grid(pos+COLS)
        if grid_block and phi(grid, grid_block, pos+COLS):
            pos += COLS
        else:
            return pos

pygame.init()
pygame.event.set_blocked(None)
pygame.event.set_allowed((KEYDOWN, QUIT))
pygame.key.set_repeat(75, 0)
pygame.display.set_caption('Tetris')
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.update()

while True: # start(restart) game
    grid = [None] * CELLS
    speed = 500
    screen.fill(COLOR_BG)
    while True: # spawn a block
        block = choice([O, I, S, Z, L, J, T])()
        pos = POS_FIRST_APPEAR
        if not phi(grid, block.grid(pos), pos): break # you lose
        pygame.time.set_timer(KEYDOWN, speed)
        while True: # move the block
            draw(merge(grid, block.grid(pos)), pos)
            event = pygame.event.wait()
            if event.type == QUIT: sys.exit()
            try:
                aim = {
                    K_UNKNOWN: pos+COLS,
                    K_UP: pos,
                    K_DOWN: pos+COLS,
                    K_LEFT: pos-1,
                    K_RIGHT: pos+1,
                    K_SPACE: None,
                }[event.key]
            except KeyError:
                continue
            if event.key == K_UP:
                block.rotate()
            elif event.key in (K_LEFT, K_RIGHT) and pos / COLS <> aim / COLS:
                continue
            elif event.key == K_SPACE:
                pos_old = pos
                pos = max_pos(grid, block, pos)
                draw(grid, pos_old)
                draw(merge(grid, block.grid(pos)), pos)
                break
            grid_aim = block.grid(aim)
            if grid_aim and phi(grid, grid_aim, aim):
                pos = aim
            else:
                if event.key == K_UP:
                    block.rotate(times=3)
                elif not event.key in (K_LEFT, K_RIGHT):
                    break
        grid = merge(grid, block.grid(pos))
        grid, n = complete(grid)
        if n:
            draw(grid)
            speed -= 5 * n
            if speed < 75: speed = 75
