from lineofsight.lib.board import Board
from lineofsight.res.glob import *
from time import time
import pygame


def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption(TITLE)

    screen_size = (WIDTH + 1, HEIGHT + 1) if DRAW_GRID else (WIDTH, HEIGHT)

    if FULLSCREEN:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(screen_size)

    # def __init__(self, screen, size, pixelWidth, drawGrid=0):
    board = Board(screen, (WIDTH, HEIGHT), (PIXEL_WIDTH, PIXEL_HEIGHT),
                  draw_grid=DRAW_GRID,
                  draw_edges=DRAW_EDGES)

    while True:
        if not runTime(board):
            break
    pygame.quit()


def runTime(board):
    startTime = time()
    m_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.toggle_switch()

        if pygame.mouse.get_pressed()[0]:
            pos = board.get_clicked_pos(pygame.mouse.get_pos())
            board.set_node_state(pos, states.wall)

        elif pygame.mouse.get_pressed()[2]:
            pos = board.get_clicked_pos(pygame.mouse.get_pos())
            board.set_node_state(pos, states.empty)

    update(board, startTime, FPS, m_pos)
    return True


def update(board, start_time, fps, *a, **kw):
    board.update(*a, **kw)
    # fps düzenlemesi
    while time() - start_time < (1 / fps):
        pass

    pygame.display.update()


if __name__ == "__main__":
    main()
