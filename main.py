import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import copy
import game_1_original as g1
import game_2_hard as g2

running = False
display = (1900, 1000)
pygame.init()
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | HWSURFACE | RESIZABLE)
gluPerspective(100, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)
start = False
game_1 = True
game_2 = True

while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               running = True
               if game_1:
                    apple = g1.Apple()
                    snake = g1.Snake()
               elif game_2:
                   apple = g2.Apple()
                   snake = g2.Snake()                
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake.moving_to[g1.DOWN]:
                    snake.moving_to = [True, False, False, False]

                elif event.key == pygame.K_DOWN and not snake.moving_to[g1.UP]:
                    snake.moving_to = [False, True, False, False]

                elif event.key == pygame.K_RIGHT and not snake.moving_to[g1.LEFT]:
                    snake.moving_to = [False, False, True, False]

                elif event.key == pygame.K_LEFT and not snake.moving_to[g1.RIGHT]:
                    snake.moving_to = [False, False, False, True]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if snake.head_position == apple.position:
            apple.update_position(snake.body_position, snake.head_position)
            snake.add_body()

        if game_1:
            running = snake.update_and_check_head_position()
            g1.draw_bakground()
            apple.draw_apple()
            snake.draw_snake()
        elif game_2:
            running = snake.update_and_check_head_position()
            g1.draw_bakground()
            apple.draw_apple()
            snake.draw_snake()

        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.wait(150)

pygame.quit()
