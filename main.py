import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

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


class Apple:
    def __init__(self):
        self.apple_possibilities = []
        self.pos_index = 0
        for x in range(-10, 12):
            for y in range(-10, 12):
                self.apple_possibilities.append([[x - 1, y, 0.0], [x, y, 0.0], [x, y - 1, 0.0], [x - 1, y - 1, 0.0]])
        self.position = self.apple_possibilities[self.pos_index]

    def update_position(self):
        self.pos_index = random.randint(0, len(self.apple_possibilities))
        self.position = self.apple_possibilities[self.pos_index]

    def draw_apple(self):
        draw_square(self.position[0], self.position[1], self.position[2], self.position[3], (0, 0, 1))


class Snake:
    def __init__(self):
        self.head_position = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [0.0, -1.0, 0.0]]
        self.body_position = []
        self.body_position.append([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [-1.0, -1.0, 0.0]])
        # self.body_position[0][0][X] -= 1
        self.moving_to = [False, False, False, False]

    def draw_snake(self):
        draw_square(self.head_position[0], self.head_position[1], self.head_position[2], self.head_position[3],
                    (0, 0, 0))
        for s in self.body_position:
            draw_square(s[0], s[1], s[2], s[3], (0, 0, 0))

    def update_body_position(self, last_head):
        new_body_position = [e for e in self.body_position]
        for s in range(len(self.body_position) - 1):
            new_body_position[s] = self.new_body_position[s + 1]

        print(new_body_position[len(new_body_position) - 1])
        new_body_position[len(new_body_position) - 1] = [e for e in last_head]
        self.body_position = [e for e in new_body_position]

    def update_position(self):
        # new_snake_position = [e for e in snake.position]
        self.last_head_pos = [e for e in self.head_position]
        if self.moving_to[UP]:
            for i in range(len(self.head_position)):
                self.head_position[i][Y] += 1.0
            self.update_body_position(self.last_head_pos)

        elif self.moving_to[DOWN]:
            for i in range(len(snake.head_position)):
                self.head_position[i][Y] -= 1.0
            self.update_body_position(last_head_pos)

        elif self.moving_to[RIGHT]:
            for i in range(len(snake.head_position)):
                self.head_position[i][X] += 1.0
            self.update_body_position(last_head_pos)

        elif self.moving_to[LEFT]:
            for i in range(len(snake.head_position)):
                self.head_position[i][X] -= 1.0
            self.update_body_position(last_head_pos)


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
    glColor3f(color[0], color[1], color[2])  # Color rojo
    glVertex3f(vertice_sup_izq[0], vertice_sup_izq[1], vertice_sup_izq[2])  # arriba izq
    glVertex3f(vertice_sup_der[0], vertice_sup_der[1], vertice_sup_der[2])  # arriba der
    glVertex3f(vertice_inf_der[0], vertice_inf_der[1], vertice_inf_der[2])  # abajo der
    glVertex3f(vertice_inf_izq[0], vertice_inf_izq[1], vertice_inf_izq[2])  # abajo izq
    glEnd()


def draw_bakground():
    draw_square(DARK_GREEN_BACKGROUND[0], DARK_GREEN_BACKGROUND[1], DARK_GREEN_BACKGROUND[2], DARK_GREEN_BACKGROUND[3],
                (0, 0.1, 0))
    draw_square(GREEN_BACKGROUND[0], GREEN_BACKGROUND[1], GREEN_BACKGROUND[2], GREEN_BACKGROUND[3], (0, 0.5, 0))


running = True
display = (1900, 1000)
apple = Apple()
snake = Snake()

pygame.init()
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | HWSURFACE | RESIZABLE)
gluPerspective(100, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.moving_to = [True, False, False, False]

            elif event.key == pygame.K_DOWN:
                snake.moving_to = [False, True, False, False]

            elif event.key == pygame.K_RIGHT:
                snake.moving_to = [False, False, True, False]

            elif event.key == pygame.K_LEFT:
                snake.moving_to = [False, False, False, True]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # snake.position[0][x]: x del vertice arriba izq
    if snake.head_position[0][X] <= PARED_IZQ:
        snake.moving_to[3] = False

    if snake.head_position[1][X] >= PARED_DER:
        snake.moving_to[2] = False

    if snake.head_position[2][Y] <= PARED_ABAJO:
        snake.moving_to[1] = False

    if snake.head_position[0][Y] >= PARED_ALTO:
        snake.moving_to[0] = False

    if snake.head_position == apple.position:
        apple.update_position()

    snake.update_position()
    draw_bakground()
    apple.draw_apple()
    snake.draw_snake()

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.wait(150)
pygame.quit()
