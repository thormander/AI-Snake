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
BG = (72,111, 56)
WHITE = (255,255,255)
SNAKE_COLOR1 = (0,0,255)
SNAKE_COLOR2 = (0,100,255)

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
    def __init__(self,w=600,h=600):
        self.h = h
        self.w = w

        # window of game
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AI - Snake')
        self.clock = pygame.time.Clock()

        
        # Load assets -----------

        # food
        self.appleIMG = pygame.image.load('assets/apple.png').convert_alpha()
        self.appleIMG = pygame.transform.scale(self.appleIMG, (30,30))

        # snake head
        self.head_up = pygame.image.load('assets/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('assets/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('assets/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('assets/head_right.png').convert_alpha()

        # snake body
        self.body_horizontal = pygame.image.load('assets/body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('assets/body_vertical.png').convert_alpha()    
        self.body_bottomleft = pygame.image.load('assets/body_bottomleft.png').convert_alpha()
        self.body_bottomright = pygame.image.load('assets/body_bottomright.png').convert_alpha()
        self.body_topleft = pygame.image.load('assets/body_topleft.png').convert_alpha()
        self.body_topright = pygame.image.load('assets/body_topright.png').convert_alpha()

        # snake tail
        self.tail_up = pygame.image.load('assets/tail_up.png').convert_alpha()
        self.tail_down  = pygame.image.load('assets/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/tail_right.png').convert_alpha()



        # -----------------------


        # initial game state
        self.direction = Direction.RIGHT
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
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
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
        #if self.head.x > self.w - SIZE or self.head.x < 0 or self.head.y > self.h - SIZE or self.head.y < 0:
        #    return True

        # hit self
        if self.head in self.snake[1:]: # do not include head
            return True
        
        return False

    def moveSnake(self,direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x = (x + SIZE) % self.w
        elif direction == Direction.LEFT:
            x = (x - SIZE) % self.w
        elif direction == Direction.UP:
            y = (y - SIZE) % self.h
        elif direction == Direction.DOWN:
            y = (y + SIZE) % self.h
        
        self.head = Point(x,y)

    # drawing the items for the game
    def updateUI(self):
        # draw background
        self.display.fill(BG)

        # draw snake
        for point in self.snake:
            pygame.draw.rect(self.display,SNAKE_COLOR1,pygame.Rect(point.x,point.y,SIZE,SIZE))
            pygame.draw.rect(self.display,SNAKE_COLOR2,pygame.Rect(point.x+4,point.y+4,12,12))
        
        # draw food
        #pygame.draw.rect(self.display, FOOD, pygame.Rect(self.food.x,self.food.y,SIZE,SIZE))
        self.display.blit(self.appleIMG, (self.food.x, self.food.y))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip() # updates the screen user sees

    def gameOverText(self):
        endText = font.render("Game Over! Your final score is: " + str(self.score), True, WHITE)
        endPosition = endText.get_rect(center=(self.w/2, self.h/2))
        self.display.blit(endText, endPosition)
        
        pygame.display.flip()
        pygame.time.wait(5000)


if __name__ == '__main__':
    game = SnakeMain()

    # Run game (ie. infinite loop until game over)
    while True:
        gameOver, score = game.play()
        
        # game over condition
        if gameOver == True:
            game.gameOverText()
            break
            
    print('Your score: ', score)
    
    pygame.quit()


