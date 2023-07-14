import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import copy


UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

X = 0
Y = 1
Z = 2

PARED_IZQ = -11
PARED_ABAJO = -11
PARED_DER = 11
PARED_ALTO = 11

GREEN_BACKGROUND = [[-11.0, 11.0, 0.0], [11.0, 11.0, 0.0], [11.0, -11.0, 0.0], [-11.0, -11.0, 0.0]]
DARK_GREEN_BACKGROUND = [[-23.0, 23.0, 0.0], [23.0, 23.0, 0.0], [23.0, -23.0, 0.0], [-23.0, -23.0, 0.0]]

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
        inside_pos.append([v[X]+0.1, v[Y]-0.1, v[Z]])
        v = self.position[1]
        inside_pos.append([v[X]-0.1, v[Y]-0.1, v[Z]])
        v = self.position[2]
        inside_pos.append([v[X]-0.1, v[Y]+0.1, v[Z]])
        v = self.position[3]
        inside_pos.append([v[X]+0.1, v[Y]+0.1, v[Z]])

        draw_square(self.position[0], self.position[1], self.position[2], self.position[3], (0, 0, 0))
        draw_square(inside_pos[0], inside_pos[1], inside_pos[2], inside_pos[3], (1, 0, 0))


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


    def draw_snake(self):
        """
        Draws the snake, first the head (grey), and then the body (black)
        """
        draw_square(self.head_position[0], self.head_position[1], self.head_position[2], self.head_position[3],
                    (0, 0, 0.5))
        for s in self.body_position:
            draw_square(s[0], s[1], s[2], s[3], (0, 0, 0.1))


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
        if self.moving_to[UP]:
            for i in range(len(self.head_position)):
                self.head_position[i][Y] += 1.0

            if self.head_position not in self.body_position and self.head_position[0][Y] <= PARED_ALTO:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False

        elif self.moving_to[DOWN]:
            for i in range(len(self.head_position)):
                self.head_position[i][Y] -= 1.0

            if self.head_position not in self.body_position and self.head_position[2][Y] >= PARED_ABAJO:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False

        elif self.moving_to[RIGHT]:
            for i in range(len(self.head_position)):
                self.head_position[i][X] += 1.0

            if self.head_position not in self.body_position and self.head_position[1][X] <= PARED_DER:
                self.update_body_position(last_head_pos)
            else:
                self.head_position = copy.deepcopy(last_head_pos)
                return False

        elif self.moving_to[LEFT]:
            for i in range(len(self.head_position)):
                self.head_position[i][X] -= 1.0

            if self.head_position not in self.body_position and self.head_position[0][X] >= PARED_IZQ:
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
        if self.moving_to[UP]:
            for i in range(len(body_to_add)):
                body_to_add[i][Y] -= 1.0

        elif self.moving_to[DOWN]:
            for i in range(len(body_to_add)):
                body_to_add[i][Y] += 1.0

        elif self.moving_to[LEFT]:
            for i in range(len(body_to_add)):
                body_to_add[i][Y] += 1.0

        elif self.moving_to[RIGHT]:
            for i in range(len(body_to_add)):
                body_to_add[i][Y] -= 1.0
        self.body_position.insert(0, body_to_add)

def draw_square(vertice_sup_izq, vertice_sup_der, vertice_inf_der, vertice_inf_izq, color):
    """
    dibuja un cuadrado con las cordenadas de vertices establecidas
    :param vertice_sup_izq: cordenadas del vertice superior izquierdo, formato [x, y, z]
    :param vertice_sup_der: cordenadas del vertice superior derecho, formato [x, y, z]
    :param vertice_inf_der: cordenadas del vertice derecho izquierdo, formato [x, y, z]
    :param vertice_inf_izq: cordenadas del vertice inferior izquierdo, formato [x, y, z]
    :param color: color que tendra el cuadrado
    :return:
    """
    glBegin(GL_QUADS)
    glColor3f(color[0], color[1], color[2])
    glVertex3f(vertice_sup_izq[0], vertice_sup_izq[1], vertice_sup_izq[2])  # arriba izq
    glVertex3f(vertice_sup_der[0], vertice_sup_der[1], vertice_sup_der[2])  # arriba der
    glVertex3f(vertice_inf_der[0], vertice_inf_der[1], vertice_inf_der[2])  # abajo der
    glVertex3f(vertice_inf_izq[0], vertice_inf_izq[1], vertice_inf_izq[2])  # abajo izq
    glEnd()

def draw_bakground():
    """
    Draws a light green background and a dark green border
    """
    draw_square(DARK_GREEN_BACKGROUND[0], DARK_GREEN_BACKGROUND[1], DARK_GREEN_BACKGROUND[2], DARK_GREEN_BACKGROUND[3], (0, 0.1, 0))
    draw_square(GREEN_BACKGROUND[0], GREEN_BACKGROUND[1], GREEN_BACKGROUND[2], GREEN_BACKGROUND[3], (0, 0.5, 0))
