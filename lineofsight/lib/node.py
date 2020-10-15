from lineofsight.lib.edge import Edge
from lineofsight.res.glob import *
import pygame


class Node(pygame.Rect):
    def __init__(self, state, *a, **kw):
        super().__init__(*a, **kw)

        self.edge_ids = {}
        for direction in directions:
            self.edge_ids[direction] = -1

        self.color = None
        self.state = state
        # print(self.topleft, self.bottomleft,
        #       self.bottomright, self.topright)

    @property
    def state(self):
        return states.wall if self.color == colors.green else states.empty

    @state.setter
    def state(self, value):
        self.color = colors.green if value == states.wall else colors.black

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, self)

    def __repr__(self):
        return f"{self.state}"