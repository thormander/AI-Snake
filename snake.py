import os
import time
import pygame
import random
import numpy as np  # For Q-Table save/load functionality

from enum import Enum
from collections import namedtuple # usefule for points

pygame.init() # initilize modules

# CONSTANTS
SIZE = 20
SPEED = 200

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

# Q-Learning Agent
class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.actions = actions
        self.q_table = {}  # State-action Q-value table
        self.learning_rate = learning_rate  # Alpha
        self.discount_factor = discount_factor  # Gamma
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def getStateKey(self, state):
        """
        Convert state into a hashable key for the Q-table.
        """
        return tuple(state)

    def chooseAction(self, state):
        """
        Choose an action based on the epsilon-greedy strategy.
        """
        state_key = self.getStateKey(state)
        if np.random.rand() < self.epsilon:
            # Explore: random action
            return random.choice(self.actions)
        else:
            # Exploit: best action from Q-Table
            q_values = self.q_table.get(state_key, [0] * len(self.actions))
            return self.actions[np.argmax(q_values)]

    def updateQValue(self, state, action, reward, next_state):
        """
        Update the Q-value for the given state and action using the Bellman equation.
        """
        state_key = self.getStateKey(state)
        next_state_key = self.getStateKey(next_state)
        action_index = self.actions.index(action)

        # Current Q-value
        current_q = self.q_table.get(state_key, [0] * len(self.actions))[action_index]

        # Max Q-value for the next state
        next_max_q = max(self.q_table.get(next_state_key, [0] * len(self.actions)))

        # Update Q-value
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        if state_key not in self.q_table:
            self.q_table[state_key] = [0] * len(self.actions)
        self.q_table[state_key][action_index] = new_q

    def decayEpsilon(self):
        """
        Gradually reduce the exploration rate (epsilon).
        """
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def saveQTable(self, filename):
        """
        Save the Q-table to a file.
        """
        np.save(filename, self.q_table)

    def loadQTable(self, filename):
        """
        Load the Q-table from a file.
        """
        self.q_table = np.load(filename, allow_pickle=True).item()


class SnakeMain:
    # pass window size of game
    def __init__(self,w=600,h=600):
        # AI agent
        self.agent = QLearningAgent(
            actions=[Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT],
            learning_rate=0.1,
            discount_factor=0.9,
            epsilon=1.0,
            epsilon_decay=0.997,
            epsilon_min=0.15
        )

        # Load Q-Table if it exists
        if os.path.exists("q_table.npy"):
            self.agent.q_table = np.load("q_table.npy", allow_pickle=True).item()
            print("Loaded existing Q-Table.")
        else:
            print("No Q-Table found. Starting with an empty Q-Table.")

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
        
        self.head_up = pygame.transform.scale(self.head_up, (20,20))
        self.head_down = pygame.transform.scale(self.head_down, (20,20))
        self.head_left = pygame.transform.scale(self.head_left, (20,20))
        self.head_right = pygame.transform.scale(self.head_right, (20,20))

        # snake body
        self.body_horizontal = pygame.image.load('assets/body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('assets/body_vertical.png').convert_alpha()    
        self.body_bottomleft = pygame.image.load('assets/body_bottomleft.png').convert_alpha()
        self.body_bottomright = pygame.image.load('assets/body_bottomright.png').convert_alpha()
        self.body_topleft = pygame.image.load('assets/body_topleft.png').convert_alpha()
        self.body_topright = pygame.image.load('assets/body_topright.png').convert_alpha()

        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (20,20))
        self.body_vertical = pygame.transform.scale(self.body_vertical, (20,20))
        self.body_bottomleft = pygame.transform.scale(self.body_bottomleft, (20,20))
        self.body_bottomright = pygame.transform.scale(self.body_bottomright, (20,20))
        self.body_topleft = pygame.transform.scale(self.body_topleft, (20,20))
        self.body_topright = pygame.transform.scale(self.body_topright, (20,20))

        # snake tail
        self.tail_up = pygame.image.load('assets/tail_up.png').convert_alpha()
        self.tail_down  = pygame.image.load('assets/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/tail_right.png').convert_alpha()

        self.tail_up = pygame.transform.scale(self.tail_up, (20,20))
        self.tail_down = pygame.transform.scale(self.tail_down, (20,20))
        self.tail_left = pygame.transform.scale(self.tail_left, (20,20))
        self.tail_right = pygame.transform.scale(self.tail_right, (20,20))

        # -----------------------

        # initial game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head, Point(self.head.x-SIZE,self.head.y),Point(self.head.x-(2*SIZE),self.head.y)]

        self.score = 0
        self.food = None
        self.generateFood()
    
    def getState(self):
        """
        Enhanced state representation with food and border awareness.
        """
        # Distance to food
        food_dir_x = 1 if self.food.x > self.head.x else -1 if self.food.x < self.head.x else 0
        food_dir_y = 1 if self.food.y > self.head.y else -1 if self.food.y < self.head.y else 0

        # Danger detection
        danger_up = self.head.y - SIZE < 0 or Point(self.head.x, self.head.y - SIZE) in self.snake
        danger_down = self.head.y + SIZE >= self.h or Point(self.head.x, self.head.y + SIZE) in self.snake
        danger_left = self.head.x - SIZE < 0 or Point(self.head.x - SIZE, self.head.y) in self.snake
        danger_right = self.head.x + SIZE >= self.w or Point(self.head.x + SIZE, self.head.y) in self.snake

        # Border awareness
        near_border_up = self.head.y < SIZE
        near_border_down = self.head.y >= self.h - SIZE
        near_border_left = self.head.x < SIZE
        near_border_right = self.head.x >= self.w - SIZE

        # Food near borders
        food_near_border_up = self.food.y < SIZE
        food_near_border_down = self.food.y >= self.h - SIZE
        food_near_border_left = self.food.x < SIZE
        food_near_border_right = self.food.x >= self.w - SIZE

        return (
            danger_up, danger_down, danger_left, danger_right,
            near_border_up, near_border_down, near_border_left, near_border_right,
            food_near_border_up, food_near_border_down, food_near_border_left, food_near_border_right,
            food_dir_x, food_dir_y
        )


    def play(self):
        # Get the current state before the move
        current_state = self.getState()

        # Let the AI choose the next action
        new_direction = self.agent.chooseAction(current_state)

        # Ensure the chosen direction is valid (doesn't reverse direction)
        if (
            (self.direction == Direction.RIGHT and new_direction != Direction.LEFT) or
            (self.direction == Direction.LEFT and new_direction != Direction.RIGHT) or
            (self.direction == Direction.UP and new_direction != Direction.DOWN) or
            (self.direction == Direction.DOWN and new_direction != Direction.UP)
        ):
            self.direction = new_direction

        # Calculate Manhattan distance to food before moving
        dist_before = abs(self.food.x - self.head.x) + abs(self.food.y - self.head.y)

        # Move the snake
        self.moveSnake(self.direction)
        self.snake.insert(0, self.head)

        # Calculate Manhattan distance to food after moving
        dist_after = abs(self.food.x - self.head.x) + abs(self.food.y - self.head.y)

        # Base rewards
        reward = 0  # Default reward
        if self.head == self.food:
            reward += 25 # Reward for eating food
            self.score += 1
            self.generateFood()
        else:
            self.snake.pop()

            # Moving closer to food
            if dist_after < dist_before:
                reward += 2  # Reward for approaching food
            else:
                reward -= 1  # Penalty for moving away from food

        # Add penalties for border proximity
        if self.head.x < SIZE or self.head.x >= self.w - SIZE or self.head.y < SIZE or self.head.y >= self.h - SIZE:
            reward -= 2  # Penalty for being near the border

        # Check for collisions
        if self.collision():
            reward = -50  # Big penalty for hitting the border or itself
            return True, self.score

        # Update Q-values
        next_state = self.getState()
        self.agent.updateQValue(current_state, self.direction, reward, next_state)
        self.agent.decayEpsilon()

        self.updateUI()
        self.clock.tick(SPEED)

        return False, self.score




    def generateFood(self):
        """
        Generate a new food position that does not overlap with the snake.
        """
        x = random.randint(0, (self.w - SIZE) // SIZE) * SIZE
        y = random.randint(0, (self.h - SIZE) // SIZE) * SIZE
        self.food = Point(x, y)

        # Ensure the food does not overlap with the snake
        if self.food in self.snake:
            self.generateFood()

    def collision(self):
        # Check if the head collides with the borders
        if self.head.x < 0 or self.head.x >= self.w or self.head.y < 0 or self.head.y >= self.h:
            return True

        # Check if the head collides with its body
        if self.head in self.snake[1:]:
            return True

        return False


    def moveSnake(self, direction):
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

        self.head = Point(x, y)

    def updateUI(self):
        # draw background
        self.display.fill(BG)

        # draw snake
        for index, point in enumerate(self.snake):
            segment_rect = pygame.Rect(point.x, point.y, SIZE, SIZE)
            
            # head
            if index == 0:
                head_sprite = self.getHead()
                self.display.blit(head_sprite, segment_rect)
            # Tail
            elif index == len(self.snake) - 1:  
                tail_sprite = self.getTail(index)
                self.display.blit(tail_sprite, segment_rect)
            # Body
            else:  
                body_sprite = self.getBody(index)
                self.display.blit(body_sprite, segment_rect)            

        # draw food
        self.display.blit(self.appleIMG, (self.food.x, self.food.y))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip() # updates the screen user sees

    def getHead(self):
        if self.direction == Direction.UP:
            return self.head_up
        elif self.direction == Direction.DOWN:
            return self.head_down
        elif self.direction == Direction.LEFT:
            return self.head_left
        elif self.direction == Direction.RIGHT:
            return self.head_right

    def getTail(self, index):
        tail_segment = self.snake[-1]
        last_body_segment = self.snake[-2]

        if tail_segment.x == last_body_segment.x:
            # if snake going up
            if tail_segment.y > last_body_segment.y:
                return self.tail_down
            # if snake going down
            else:
                return self.tail_up
        else:
            # snake going left
            if tail_segment.x < last_body_segment.x:
                return self.tail_left
            # snake going right
            else:
                return self.tail_right

    def getBody(self, index):
        current_segment = self.snake[index]
        previous_segment = self.snake[index - 1]
        next_segment = self.snake[index + 1]

        # body is horizontal
        if current_segment.y == previous_segment.y == next_segment.y:
            return self.body_horizontal

        # body is vertical
        if current_segment.x == previous_segment.x == next_segment.x:
            return self.body_vertical
        
        # handle body corners
        if previous_segment.x == current_segment.x:
            # snake moving left
            if next_segment.x > current_segment.x:
                if previous_segment.y < current_segment.y:
                    return self.body_topright  # left -> up
                else:
                    return self.body_bottomright # left -> down
            # snake moving right
            else:
                if previous_segment.y < current_segment.y:
                    return self.body_topleft # right -> up
                else:
                    return self.body_bottomleft  # right -> down
        elif previous_segment.y == current_segment.y:
            # snake moving up
            if next_segment.y > current_segment.y:
                if previous_segment.x < current_segment.x:
                    return self.body_bottomleft  # up to left
                else:
                    return self.body_bottomright  # up to right
            # snake moving down
            else:
                if previous_segment.x < current_segment.x:
                    return self.body_topleft  # down to left
                else:
                    return self.body_topright # down to right

    def gameOverText(self):
        endText = font.render("Game Over! Your final score is: " + str(self.score), True, WHITE)
        endPosition = endText.get_rect(center=(self.w/2, self.h/2))
        self.display.blit(endText, endPosition)
        
        pygame.display.flip()
        pygame.time.wait(5000)


if __name__ == '__main__':
    game = SnakeMain()

    # Timer for saving Q-Table
    save_interval = 60  # Save Q-Table every 60 seconds
    last_save_time = time.time()  # Track last save time

    print("Starting the game. Watch the snake learn in real-time!")
    while True:
        game_over, score = game.play()

        if game_over:
            print(f"Game Over! Score: {score}, Epsilon: {game.agent.epsilon:.3f}")
            
            # Reset the game while continuing training
            game = SnakeMain()
            if os.path.exists("q_table.npy"):
                game.agent.loadQTable("q_table.npy")

        # Save Q-Table periodically
        if time.time() - last_save_time >= save_interval:
            game.agent.saveQTable("q_table.npy")
            print(f"Q-Table auto-saved at {time.strftime('%Y-%m-%d %H:%M:%S')}.")
            last_save_time = time.time()