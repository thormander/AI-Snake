import pygame
import random

from enum import Enum
from collections import namedtuple # usefule for points

pygame.init() # initilize modules

# CONSTANTS
SIZE = 20

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Psuedo Class
Point = namedtuple('Point','x','y')

class SnakeMain:
    # pass window size of game
    def __init__(self,h=600,w=600):
        self.h = h
        self.w = w

        # window of game
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AI - Snake', icontitle=None)
        self.clock = pygame.time.Clock()

        # initial game state
        self.dir = Direction.LEFT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head, Point(self.head.x-SIZE,self.head.y),Point(self.head.x-(2*SIZE),self.head.y)]

        self.points = 0
        self.food = None
        self.generateFood()
    
    def generateFood(self):
        x = random.randint(0, (self.w-SIZE)//SIZE) * SIZE
        y = random.randint(0, (self.h-SIZE)//SIZE) * SIZE
        self.food = Point(x,y)
        
        # check if food is in snake (regenerate if it is)
        if self.food in self.snake:
            self.generateFood()

    def play(self):
        # Get user input

        # move snake

        

    
    
if __name__ == '__main__':
    game = SnakeMain()

    # Run game (ie. infinite loop until game over)
    while True:
        game.play()
        
        # game over condition
    
    pygame.quit()


