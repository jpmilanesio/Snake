import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import copy

import game_1_original as g1
import game_2_hard as g2
import game_3_fast as g3
import general_games as gg

def draw_prev_snake(current_games):
    """
    Displays the snake from each game (one snake per function)
    :param current_games: list of games to play and who is the actual [True, False, False]
    """

    if current_games[0]:
        body_color = (0.1, 0.1, 0.1)
        head_color = (0.5, 0.5, 0.5)
    elif current_games[1]:
        body_color = (0.0, 0.0, 0.1)
        head_color = (0.0, 0.0, 0.5)
    elif current_games[2]:
        body_color = (0.0, 0.1, 0.0)
        head_color = (0.0, 0.5, 0.0)

    head_position = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [0.0, -1.0, 0.0]]
    body_position = []
    body_position.insert(0, [[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [-1.0, -1.0, 0.0]])
    body_position.insert(0, [[-2.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [-1.0, -1.0, 0.0], [-2.0, -1.0, 0.0]])
    gg.draw_square(head_position[0], head_position[1], head_position[2], head_position[3], head_color)
    for s in body_position:
        gg.draw_square(s[0], s[1], s[2], s[3], body_color)


display = (800, 800)
pygame.init()
pygame.display.set_mode(display, DOUBLEBUF | HWSURFACE | OPENGL | RESIZABLE)

gluPerspective(100, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)

running = False
start = False
last_game = 1
current_game = 0
game_1 = True
game_2 = False
game_3 = False
games = [game_1, game_2, game_3]

while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               running = True
               if games[0]:
                    apple = g1.Apple()
                    snake = g1.Snake()
               elif games[1]:
                   apple = g2.Apple()
                   snake = g2.Snake()
               elif games[2]:
                   apple = g3.Apple()
                   snake = g3.Snake()

            elif event.key == K_RIGHT:
                games[current_game % 3] = False
                current_game += 1
                games[current_game % 3] = True
            elif event.key == K_LEFT:
                games[current_game % 3] = False
                current_game -= 1
                games[current_game % 3] = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    draw_prev_snake(games)

    pygame.display.flip()
    pygame.time.wait(150)



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake.moving_to[gg.DOWN]:
                    snake.moving_to = [True, False, False, False]

                elif event.key == pygame.K_DOWN and not snake.moving_to[gg.UP]:
                    snake.moving_to = [False, True, False, False]

                elif event.key == pygame.K_RIGHT and not snake.moving_to[gg.LEFT]:
                    snake.moving_to = [False, False, True, False]

                elif event.key == pygame.K_LEFT and not snake.moving_to[gg.RIGHT] and not snake.moving_to == [False, False, False, False]:
                    snake.moving_to = [False, False, False, True]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        gg.draw_background()

        if snake.head_position == apple.position:
            apple.update_position(snake.body_position, snake.head_position)
            snake.add_body()

        running = snake.update_and_check_head_position()
        apple.draw_apple()
        snake.draw_snake()
        pygame.display.flip()

        if games[0]:
            pygame.time.wait(150)
        elif games[1]:
            if g2.g_points > 35:
                pygame.time.wait(70)
            else:
                pygame.time.wait(150-g2.g_points*2)
        elif games[2]:
            pygame.time.wait(70)

    glClear(GL_COLOR_BUFFER_BIT)
    draw_prev_snake(games)

pygame.quit()
