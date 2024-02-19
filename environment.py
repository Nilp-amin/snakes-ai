#!/usr/bin/env python3
import pygame
import numpy as np

from snakes import World, ScoreManager, SnakeChunk, Wall

from typing import Tuple
from enum import IntEnum

class Move(IntEnum):
    UP = pygame.K_w
    DOWN = pygame.K_s
    LEFT = pygame.K_a
    RIGHT = pygame.K_d
    NONE = -1 

class State(object):
    X_AXIS = np.array([1, 0])
    Y_AXIS = np.array([0, 1])
    Q0 = np.array([1, 1])
    Q1 = np.array([-1, 1])
    Q2 = np.array([1, -1])
    Q3 = np.array([-1, -1])
    def __init__(self, world: World):
        self.edible_position = None
        self.obstacle_positons = [] 

        # obtain position of edible as represented by one a cell around the head of the snake
        head_position = world.get_snake_head_position()
        head_edible_vector = world.get_edible_position() - head_position 
        head_edible_angle = self.X_AXIS.angle_to(head_edible_vector) 

        if head_edible_angle == 0.0:
            self.edible_position = self.X_AXIS 
        elif head_edible_angle > 0.0 and head_edible_angle < 90.0:
            self.edible_position = self.Q0
        elif head_edible_angle == 90.0:
            self.edible_position = self.Y_AXIS
        elif head_edible_angle > 90.0 and head_edible_angle < 180.0:
            self.edible_position = self.Q1
        elif head_edible_angle == 180.0:
            self.edible_position = -self.X_AXIS
        elif head_edible_angle < 0.0 and head_edible_angle > -90.0:
            self.edible_position = self.Q2
        elif head_edible_angle == -90.0:
            self.edible_position = -self.Y_AXIS
        elif head_edible_angle < -90.0:
            self.edible_position = self.Q3

        # obtain the obstacle positions one block around the head of the snake
        offset_around = [self.X_AXIS,
                         self.Y_AXIS,
                         self.Q0,
                         self.Q1,
                         self.Q2,
                         self.Q3]

        for offset in offset_around:
            cell_position = head_position + pygame.Vector2(offset[0], offset[1])
            for sprite in world.collidable.sprites():
                if not isinstance(sprite, type(world.edible.sprite)):
                    sprite_position = sprite.get_grid_position()
                    if sprite_position == cell_position:
                        self.obstacle_positons.append(np.array[sprite_position.x, 
                                                               sprite_position.y])

    def __key(self):
        return (self.edible_position, self.obstacle_positons)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.__key() == __value.__key()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__key)

class Environment(object):
    CELL_NUMBER = 15
    CELL_SIZE = 120
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.CELL_NUMBER * self.CELL_SIZE, 
                                               self.CELL_NUMBER * self.CELL_SIZE + ScoreManager.SCORE_CARD_HEIGHT), 
                                               pygame.SCALED)

        self.world = World(self.CELL_NUMBER, self.CELL_SIZE)
        self.manager = ScoreManager(self.CELL_NUMBER, self.CELL_SIZE)

        # show game to user immediatly
        self.show(self.world.draw(), self.manager.update(0, 0))

    def show(self, world: pygame.Surface, ui: pygame.Surface) -> None:
        self.screen.blit(world, (0, 0))
        self.screen.blit(ui, (0, self.CELL_NUMBER * self.CELL_SIZE))
        pygame.display.flip()

    def get_reward(self) -> float:
        head_position = self.world.get_snake_head_position()
        edible_position = self.world.get_edible_position()

        return -1 * (edible_position - head_position).length_squared()

    def perform_move(self, move: Move, graphics: bool=True) -> Tuple[State, float]:
        # TODO: write code to apply move and return requried information
        if move is not Move.NONE: self.world.set_direction(move.value)

        score, deaths, game_over = self.world.update()

        if graphics: self.show(self.world.draw(), self.manager.update(score, deaths))

        return State(self.world), self.get_reward()
