import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import copy
import general_games as gg
from game_base import Apple, Snake

# Game-specific colors
HEAD_COLOR = (0.0, 0.0, 0.5)  # Blue
BODY_COLOR = (0.0, 0.0, 0.1)  # Dark blue

def create_snake():
    """Create a snake with the game-specific colors"""
    return Snake(head_color=HEAD_COLOR, body_color=BODY_COLOR)

def create_apple():
    """Create an apple"""
    return Apple()
