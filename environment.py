#!/usr/bin/env python3
import pygame

from snakes import World
from snakes import ScoreManager

class Environment(object):
    CELL_NUMBER = 15
    CELL_SIZE = 120
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.CELL_NUMBER * self.CELL_SIZE, 
                                               self.CELL_NUMBER * self.CELL_SIZE + ScoreManager.SCORE_CARD_HEIGHT), 
                                               pygame.SCALED)
        self.world = World(self.CELL_NUMBER, self.CELL_SIZE)

