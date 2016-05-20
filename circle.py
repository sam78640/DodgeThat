import pygame
from pygame.locals import *
import math
pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)

def game_loop():
    game_over = False
    circle_x = 250
    circle_y = 250
    new_value_x = 50
    new_value_y = 50
    start = True
    
    while not game_over:
        if start == True:
            new_value_x += 5
            new_value_y += 5
        if start == False:
            new_value_x -= 5
            new_value_y -= 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if start:
                        start = False
                    elif not start:
                        start = True
                
        screen.fill(white)

        
        #pygame.draw.circle(screen,black,(circle_x,circle_y),150)
        pygame.draw.circle(screen,black,(new_value_x,new_value_y),20)
        pygame.display.update()
        clock.tick(60)
        
game_loop()
