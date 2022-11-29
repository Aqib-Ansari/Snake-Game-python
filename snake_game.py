from cgitb import text
from time import time
from tkinter import font
import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()
font = pygame.font.SysFont("arial",25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x, y')

WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,10,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)
BLOCKSIZE = 20
SPEED = 10 


class SnakeGame:
    def __init__(self,w = 960,h = 720):
        self.w = w
        self.h = h
        # init Display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        #init game State
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head , 
            Point(self.head.x-BLOCKSIZE,self.head.y),
            Point(self.head.x-(2*BLOCKSIZE),self.head.y)]

        self.score = 0
        self.food = None 
        self._place_food()

    def _place_food(self):
        x = random.randint(0+BLOCKSIZE,(self.w-BLOCKSIZE-BLOCKSIZE )//BLOCKSIZE)*BLOCKSIZE
        y = random.randint(0+BLOCKSIZE,(self.h-BLOCKSIZE-BLOCKSIZE )//BLOCKSIZE)*BLOCKSIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self):
        # Collect the key of users
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.QUIT()
                quit()
            
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif events.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif events.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif events.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        

        # move 
        self._move(self.direction)
        self.snake.insert(0, self.head)


        # Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over,self.score

        # place new food
        if self.head == self.food:
            self.score += 2
            self._place_food()
        else:
            self.snake.pop()

        # update the pygame UI and Score
        self._update_UI()
        self.clock.tick(SPEED)

        #REturn Game over and Score
        
        return game_over,self.score

    def _is_collision(self):
        # hits boundary;
        if self.head.x > self.w - BLOCKSIZE or self.head.x < 0 or self.head.y > self.h - BLOCKSIZE or self.head.y < 0:
            return True
        

    def _update_UI(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCKSIZE,BLOCKSIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))

        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCKSIZE,BLOCKSIZE))

        text = font.render("Score = " + str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def _move(self,direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x+= BLOCKSIZE
        elif direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif direction == Direction.UP:
            y-= BLOCKSIZE
        elif direction == Direction.DOWN:
            y += BLOCKSIZE

        self.head = Point(x,y)


if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over,score = game.play_step()

        if game_over == True:
            break
    print('Final Score',score)

    pygame.quit()