from OpenGL.GL import *
from OpenGL.GLU import *
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

def draw_background():
    """
    Draws a light green background and a dark green border
    """
    draw_square(DARK_GREEN_BACKGROUND[0], DARK_GREEN_BACKGROUND[1], DARK_GREEN_BACKGROUND[2], DARK_GREEN_BACKGROUND[3], (0, 0.1, 0))
    draw_square(GREEN_BACKGROUND[0], GREEN_BACKGROUND[1], GREEN_BACKGROUND[2], GREEN_BACKGROUND[3], (0, 0.5, 0))

