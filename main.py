from lineofsight.lib.board import Board
from lineofsight.res.glob import *
from time import time
import pygame


def main():
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if pygame.mouse.get_pressed()[0]:
            pos = board.get_clicked_pos(pygame.mouse.get_pos())
            board.set_node_state(pos, states.wall)

        elif pygame.mouse.get_pressed()[1]:
            print("toggle")

        elif pygame.mouse.get_pressed()[2]:
            pos = board.get_clicked_pos(pygame.mouse.get_pos())
            board.set_node_state(pos, states.empty)

    update(board, startTime, FPS)
    return True


def update(board, startTime, fps):
    board.update()
    # ekrana yazıldı
    pygame.display.update()
    # fps düzenlemesi
    while time() - startTime < (1 / fps):
        pass


if __name__ == "__main__":
    main()
