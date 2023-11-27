import pygame
import random

from enum import Enum
from collections import namedtuple # usefule for points

pygame.init() # initilize modules

# CONSTANTS
SIZE = 20
SPEED = 10

# COLOR CONSTANTS
BLACK = (0,0,0)
WHITE = (255,255,255)
FOOD = (255,0,0)
SNAKE_COLOR1 = (0,100,255)
SNAKE_COLOR2 = (0,20,255)

# FONTS
font = pygame.font.SysFont('arial', 25, bold=False, italic=False)


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
        self.direction = Direction.LEFT
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
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move snake
        self.moveSnake(self.direction) # update head
        self.snake.insert(0,self.head) 

        # game over? (hit itself or border)
        gameOver = False
        if self.collision():
            gameOver = True
            return gameOver, self.score

        # generate new food
        if self.head == self.food:
            self.score += 1
            self.generateFood()
        else:
            self.snake.pop()

        # update
        self.updateUI()
        self.clock.tick(SPEED)

        # return score after game over
        return gameOver, self.score

    def collision(self):
        # hit boundary
        if self.head.x > self.w - SIZE or self.head.x < 0 or self.head.y > self.h - SIZE or self.head.y < 0:
            return True

        # hit self
        if self.head in self.snake[1:]: # do not include head
            return True
        
        return False

    def moveSnake(self,direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += SIZE
        elif direction == Direction.LEFT:
            x -= SIZE
        elif direction == Direction.UP:
            y -= SIZE
        elif direction == Direction.DOWN:
            y += SIZE
        
        self.head = Point(x,y)

    # drawing the items for the game
    def updateUI(self):
        self.display.fill(BLACK)

        # draw snake
        for point in self.snake:
            pygame.draw.rect(self.display,SNAKE_COLOR1,pygame.Rect(point.x,point.y,SIZE,SIZE))
            pygame.draw.rect(self.display,SNAKE_COLOR2,pygame.Rect(point.x+4,point.y+4,12,12))
        
        # draw food
        pygame.draw.rect(self.display, FOOD, pygame.Rect(self.food.x,self.food.y,SIZE,SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip() # updates the screen user sees

    
if __name__ == '__main__':
    game = SnakeMain()

    # Run game (ie. infinite loop until game over)
    while True:
        gameOver, score = game.play()
        
        # game over condition
        if gameOver == True:
            pygame.time.wait(5000)  # Wait for 5 seconds
            break
            
    print('Your score: ', score)
    
    pygame.quit()


