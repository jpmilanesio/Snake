import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import copy
import general_games as gg

g_points = 0

class Apple:
    def __init__(self):
        """
        Apples are squares, when the snake's head touch any of the apple's borderlines,
        the apple disappears and the player gets a "point"
        """
        self.apple_possibilities = []
        for x in range(-10, 12):
            for y in range(-10, 12):
                self.apple_possibilities.append([[x - 1, y, 0.0], [x, y, 0.0], [x, y - 1, 0.0], [x - 1, y - 1, 0.0]])

        self.len_possibilities = len(self.apple_possibilities)
        self.pos_index = random.randint(0, self.len_possibilities)
        self.position = self.apple_possibilities[self.pos_index]


    def update_position(self, snake_body, snake_head):
        """
        Generates an apple in a position,
        this position can't be the same as the snake
        """
        self.apple_possibilities = []
        for x in range(-10, 12):
            for y in range(-10, 12):
                self.apple_possibilities.append([[x - 1, y, 0.0], [x, y, 0.0], [x, y - 1, 0.0], [x - 1, y - 1, 0.0]])
        for s in snake_body:
            self.apple_possibilities.remove(s)
        self.apple_possibilities.remove(snake_head)

        self.len_possibilities = len(self.apple_possibilities)

        self.pos_index = random.randint(0, self.len_possibilities)
        self.position = self.apple_possibilities[self.pos_index]


    def draw_apple(self):
        """
        Draws an apple
        """
        inside_pos = []

        v = self.position[0]
        inside_pos.append([v[gg.X]+0.1, v[gg.Y]-0.1, v[gg.Z]])
        v = self.position[1]
        inside_pos.append([v[gg.X]-0.1, v[gg.Y]-0.1, v[gg.Z]])
        v = self.position[2]
        inside_pos.append([v[gg.X]-0.1, v[gg.Y]+0.1, v[gg.Z]])
        v = self.position[3]
        inside_pos.append([v[gg.X]+0.1, v[gg.Y]+0.1, v[gg.Z]])

        gg.draw_square(self.position[0], self.position[1], self.position[2], self.position[3], (0, 0, 0))
        gg.draw_square(inside_pos[0], inside_pos[1], inside_pos[2], inside_pos[3], (1, 0, 0))


class Snake:
    def __init__(self):
        """
        Snake is a rectangle composed by a head(square) and a body (body starts with two squares and gets one everytime
        the head "eats" an apple). Player controls the head and the body follows it.
        If snake's head "touches" a borderline or any part of the body, the player lose.
        """
        self.head_position = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [0.0, -1.0, 0.0]]
        self.body_position = []
        self.body_position.insert(0, [[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [-1.0, -1.0, 0.0]])
        self.body_position.insert(0, [[-2.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [-1.0, -1.0, 0.0], [-2.0, -1.0, 0.0]])
        self.moving_to = [False, False, False, False]
        self.draw_snake()

    def draw_snake(self):
        """
        Draws the snake, first the head (grey), and then the body (black)
        """
        gg.draw_square(self.head_position[0], self.head_position[1], self.head_position[2], self.head_position[3],
                       (0.0, 0.6, 0.0))
        for s in self.body_position:
            gg.draw_square(s[0], s[1], s[2], s[3], (0.0, 0.3, 0.0))


    def update_body_position(self, last_head):
        """
        Updates snake's body
        First square takes the last position of snake's head and the others take the last position of the next one,for example:
        self.body_position[0] will be self.body_position[1] and self.body_position[len(body_position)-1] will be last_head
        """
        new_body_position = copy.deepcopy(self.body_position)
        for s in range(len(self.body_position) - 1):
            new_body_position[s] = new_body_position[s + 1]
        new_body_position[len(new_body_position) - 1] = copy.deepcopy(last_head)
        self.body_position = copy.deepcopy(new_body_position)


    def update_and_check_head_position(self):
        """
        Updates snake's head only if it is not touching any border or any part of the body
        """

        last_head_pos = copy.deepcopy(self.head_position)
        if self.moving_to[gg.UP]:
            for i in range(len(self.head_position)):
                self.head_position[i][gg.Y] += 1.0

            if self.head_position not in self.body_position and self.head_position[0][gg.Y] <= gg.PARED_ALTO:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False

        elif self.moving_to[gg.DOWN]:
            for i in range(len(self.head_position)):
                self.head_position[i][gg.Y] -= 1.0

            if self.head_position not in self.body_position and self.head_position[2][gg.Y] >= gg.PARED_ABAJO:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False

        elif self.moving_to[gg.RIGHT]:
            for i in range(len(self.head_position)):
                self.head_position[i][gg.X] += 1.0

            if self.head_position not in self.body_position and self.head_position[1][gg.X] <= gg.PARED_DER:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False

        elif self.moving_to[gg.LEFT]:
            for i in range(len(self.head_position)):
                self.head_position[i][gg.X] -= 1.0

            if self.head_position not in self.body_position and self.head_position[0][gg.X] >= gg.PARED_IZQ:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False
        return True

    def add_body(self):
        """
        Adds a square to the body
        """
        body_to_add = copy.deepcopy(self.body_position[len(self.body_position) - 1])
        if self.moving_to[gg.UP]:
            for i in range(len(body_to_add)):
                body_to_add[i][gg.Y] -= 1.0

        elif self.moving_to[gg.DOWN]:
            for i in range(len(body_to_add)):
                body_to_add[i][gg.Y] += 1.0

        elif self.moving_to[gg.LEFT]:
            for i in range(len(body_to_add)):
                body_to_add[i][gg.Y] += 1.0

        elif self.moving_to[gg.RIGHT]:
            for i in range(len(body_to_add)):
                body_to_add[i][gg.Y] -= 1.0
        self.body_position.insert(0, body_to_add)

