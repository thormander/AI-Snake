import pygame
import random

from enum import Enum
from collections import namedtuple # usefule for points

pygame.init() # initilize modules

# CONSTANTS
SIZE = 20
SPEED = 30

# COLOR CONSTANTS
BLACK = (0,0,0)
FOOD = (255,0,0)
SNAKE_COLOR1 = (0,100,255)
SNAKE_COLOR2 = (0,20,255)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Psuedo Class
Point = namedtuple('Point','x,y')

class SnakeMain:
    # pass window size of game
    def __init__(self,h=600,w=600):
        self.h = h
        self.w = w

        # window of game
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AI - Snake')
        self.clock = pygame.time.Clock()

        # initial game state
        self.dir = Direction.LEFT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head, Point(self.head.x-SIZE,self.head.y),Point(self.head.x-(2*SIZE),self.head.y)]

        self.score = 0
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

        # game over?

        # generate new food

        # update
        self.updateUI()
        self.clock.tick(SPEED)

        # return score after game over
        gameOver = False
        return gameOver, self.score

    # drawing the items for the game
    def updateUI(self):
        self.display.fill(BLACK)

        # draw snake
        for point in self.snake:
            pygame.draw(self.display,SNAKE_COLOR1,pygame.Rect(point.x,point.y,SIZE,SIZE))
            pygame.draw(self.display,SNAKE_COLOR2,pygame.Rect(point.x+4,point+4.y,12,12))
        
        # draw food
        pygame.draw(self.display, FOOD, pygame.Rect(self.food.x,self.food.y,SIZE,SIZE))
    

    
if __name__ == '__main__':
    game = SnakeMain()

    # Run game (ie. infinite loop until game over)
    while True:
        gameOver, score = game.play()
        
        # game over condition
        if gameOver == True:
            break
            
    print('Your score: ', score)
    
    pygame.quit()


