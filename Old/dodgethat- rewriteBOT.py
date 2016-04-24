import pygame, pygame.mixer, random, time, csv, math
from pygame.locals import *

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue = (0,0,255)
yellow = (200,200,0)
green = (0,155,0)
light_green = (0,255,0)
light_yellow = (255,255,0)
light_red = (255,0,0)
display_width = 800
display_height = 600
bg_image = "images/bg.jpg"
random_ball_pos = [30,130,230,330,430,530]

points = 0

colours = [black,red,blue,green,light_red,light_yellow]

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Dodge That!')
bg = pygame.image.load(bg_image).convert()
clock = pygame.time.Clock()
multiples_list = []
barr = "images/bar.png"
image_file = pygame.image.load(barr).convert_alpha()
class Dodge_bar(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = "images/bar.png"
    def render(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        gameDisplay.blit(self.display_image,(self.x,self.y))

class Ball_falling(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = "images/ball.png"
    def render(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        gameDisplay.blit(self.display_image,(self.x,self.y))

        
def message_to_screen(msg,color,position,fontsize):
    font = pygame.font.Font("fonts/gamee.ttf", fontsize)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [position,position])        
def multiples (m,count1,count2):
    for i in range(count1,count2):
        value = i*m
        multiples_list.append(value)

run_multiples = multiples(4,0,19)
def Game_Over():
    gameover = True
    global points
    while gameover==True:
            gameDisplay.fill(white) 
            message_to_screen("GAME OVER!", red, [195,180],60) 
            message_to_screen("Score: "+str(points), black, [320,90],40) 
            message_to_screen("Press R to play again", black, [200,290],25) 
            message_to_screen("Press M for main menu", black, [200,320],25) 
            message_to_screen("Press Q to Quit", black, [200,350],25) 
            pygame.display.update() 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_q: 
                        pygame.quit
                        quit()
                    if event.key == pygame.K_r: 
                        gameLoop() 
                    if event.key == pygame.K_m: 
                        gameover = False 
                        game_Menu()
def game_Menu():
    game_menu = True

    while game_menu == True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                quit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: 
                    game_menu = False 
                    gameLoop() 
                if event.key == pygame.K_q: 
                    pygame.quit() 
                    quit() 
        gameDisplay.fill(white)
        message_to_screen("Dodge That",green,[200,100],50) 
        message_to_screen("Press C to Start",black,[220,250],25)
        message_to_screen("Press Q to Quit",black,[220,300],25)
        
        pygame.display.update()
        clock.tick(10)
def gameLoop():
    global points
    wait_time = True
    previous_ball_x= []
    points = 0
    bary = 560
    barx = 300
    ball_speed = 2
    bar_speed = 3
    ballx = random.choice(random_ball_pos)
    bally = 50
    ball1 = Ball_falling(ballx,bally)
    bar = Dodge_bar(barx,bary)
    game_loop = True
    pressed_right = False
    pressed_left = False
    game_over = False

    while game_loop == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print ('Its just a bot')
                if event.key == pygame.K_LEFT:
                    print ('Its just a bot')
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pressed_right = False
                if event.key == pygame.K_LEFT:
                    pressed_left = False

        if pressed_right == True:
            bar.x += bar_speed
        if pressed_left == True:
            bar.x += -bar_speed
        
        ball1.y += ball_speed
        if ball1.y > display_width -200:
            balls_x = random.choice(random_ball_pos)
            ball_color = random.choice(colours)
            balls_y = 50
            ball1 = Ball_falling(balls_x,balls_y)
            ball1.y = 0
            points += 1
            for value in multiples_list:
                if value==points:
                    if ball_speed >= 5.4:
                        bar_speed = 4
                    if ball_speed >= 5.6:
                        print ('Highest Speed Reached')
                    else:
                        ball_speed += 0.2
                        print (ball_speed)
            
        if ball1.y >= bar.y and ball1.x > bar.x-50 and ball1.x <= bar.x+290 :
            
            game_loop = False
            Game_Over ()
        if ball_speed >= 3.6:
            bar_speed = 6
        #Bot Settings Start   
        if ball1.x == 30:
            if bar.x != 460:
                if bar.x > 460:
                    bar.x += -bar_speed
                if bar.x < 460:
                    bar.x += bar_speed
        if ball1.x == 130:
            if bar.x != 470:
                if bar.x > 470:
                    bar.x += -bar_speed
                if bar.x < 490:
                    bar.x += bar_speed
        if ball1.x == 230:
            if bar.x != 420:
                if bar.x > 420:
                    bar.x += -bar_speed
                if bar.x < 420:
                    bar.x += bar_speed
        if ball1.x == 330:
            if bar.x != 30:
                if bar.x > 30:
                    bar.x += -bar_speed
                if bar.x < 30:
                    bar.x += bar_speed
        if ball1.x == 430:
            if bar.x != 120:
                if bar.x > 120:
                    bar.x += -bar_speed
                if bar.x < 120:
                    bar.x += bar_speed
        if ball1.x == 530:
            if bar.x != 120:
                if bar.x > 120:
                    bar.x += -bar_speed
                if bar.x < 120:
                    bar.x += bar_speed
        #Bot settings end
        if bar.x >= 500:
            bar.x += -40
        if bar.x <= 0:
            bar.x += 40
        gameDisplay.fill(white)
        gameDisplay.blit(bg,(0,0))
        message_to_screen(str(points), red, [740,565],25)
        ball1.render()
        bar.render()
        pygame.display.update()
        if wait_time == True:
            pygame.time.wait(1000)
            wait_time = False
    clock.tick(30)
game_Menu()
