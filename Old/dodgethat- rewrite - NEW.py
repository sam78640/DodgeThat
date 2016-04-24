import pygame, pygame.mixer, random, time, csv, math,sys,os
import sqlite3 as db
from ftplib import FTP as ftp
from pygame.locals import *

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (0, 0, 255)
yellow = (200, 200, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)
light_yellow = (255, 255, 0)
light_red = (255, 0, 0)
display_width = 800
display_height = 600
bg_image = "images/bg.jpg"
random_ball_pos = [30, 130, 230, 330, 430, 530]

points = 0

colours = [black, red, blue, green, light_red, light_yellow]

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Dodge That!')
bg = pygame.image.load(bg_image).convert()
clock = pygame.time.Clock()
multiples_list = []
twenty_list = []
barr = "images/bar.png"
image_file = pygame.image.load(barr).convert_alpha()


class ConnectServer:
    def __init__(self,hostname,username,password):
        self.hostname = hostname
        self.username = username
        self.password = password
    def connection(self):
        self.ftp = ftp(self.hostname)
        self.ftp.login(self.username,self.password)
        self.ftp.cwd('/public_html/')
    def get_file(self):
        self.connection()
        self.file = open('scores.txt','wb')
        self.ftp.retrbinary('RETR scores.txt',self.file.write,1024)
        self.ftp.quit()
        self.file.close()
    def write_file(self):
        self.connection()
        self.ftp.storbinary('STOR scores.txt',open('scores.txt','rb'))
        self.ftp.quit()

class GetServerScores:
    def __init__(self):
        self.server = ConnectServer("server27.000webhost.com","a5332880","sameer123")
        self.server.get_file()

    def add_data(self,score):
        self.server.get_file()
        self.file_open = open('scores.txt','wt')
        self.file_open.write(str(score))
        self.file_open.close()
        self.server.write_file()
    def read_data(self):
        self.file_read = open('scores.txt','rt')
        for lines in self.file_read:
            return lines
        self.file_read.close()
try:
    server = GetServerScores()
    global_high_score = server.read_data()
except:
    print ("cannot connect to server")
    global_high_score = "Cannot Connect"

class Dodge_bar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = "images/bar.png"

    def render(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        self.display_image = pygame.transform.scale(self.display_image,(self.width,self.height))
        gameDisplay.blit(self.display_image, (self.x, self.y))

class Ball_falling(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = "images/ball.png"

    def render(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        gameDisplay.blit(self.display_image, (self.x, self.y))

class PowerUps:
    def __init__(self):
        self.variable = 0

    def short_bar(current_height):
        current_bar_height = current_height
        if current_height == 300:
            return True
        else:
            return False

    def life(current_life):
        if current_life != 0:
            return True
        else:
            return False

def message_to_screen(msg, color, position, fontsize):
    font = pygame.font.Font("fonts/gamee.ttf", fontsize)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [position, position])

def multiples(m, count1, count2,list1):
    for i in range(count1, count2):
        value = i * m
        list1.append(value)
run_multiples = multiples(4, 0, 100,multiples_list)
twenty_run_multiples = multiples(20, 0, 100,twenty_list)

def compare(global_score,current_score):
    if global_score < current_score:
        return True
    else:
        return False

def Game_Over():
    gameover = True
    global points
    high_score = False
    try:
        compare1 = compare(int(global_high_score),points)
        if compare1 == True:
            server.add_data(points)
            high_score = True
        else:
            print ("Compare False")
    except:
        print ("cannot connect")
        
    while gameover == True:
        gameDisplay.fill(white)
        message_to_screen("GAME OVER!", red, [195, 180], 60)
        message_to_screen("Score: " + str(points), black, [320, 90], 40)
        message_to_screen("Press R to play again", black, [200, 290], 25)
        message_to_screen("Press M for main menu", black, [200, 320], 25)
        message_to_screen("Press Q to Quit", black, [200, 350], 25)
        if high_score == True:
            message_to_screen("You beated the global high score of: " + str(global_high_score), red, [195, 240], 20)
            
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    gameLoop()
                if event.key == pygame.K_m:
                    gameover = False
                    game_Menu()


def game_Menu():
    try:
        server = GetServerScores()
        global_high_score = server.read_data()
    except:
        print ("cannot connect")
        global_high_score = "Cannot Connect"
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
        message_to_screen("Dodge That", green, [200, 100], 50)
        message_to_screen("Can you beat global high score: "+str(global_high_score), black, [200, 150], 20)
        message_to_screen("Press C to Start", black, [220, 250], 25)
        message_to_screen("Press Q to Quit", black, [220, 300], 25)

        pygame.display.update()
        clock.tick(10)

def gameLoop():
    global points
    wait_time = True
    points = 0
    bary = 560
    barx = 300
    bar_width = 10
    bar_height = 300
    ball_speed = 2
    bar_speed = 3
    ballx = random.choice(random_ball_pos)
    bally = 50
    ball1 = Ball_falling(ballx, bally)
    bar = Dodge_bar(barx, bary, bar_height,bar_width)
    game_loop = True
    pressed_right = False
    pressed_left = False
    game_over = False
    previous_position = []
    time = 0
    lifes = 3
    power_ups = PowerUps
    screenoff = 0
    short_bar = power_ups.short_bar(bar_height)

    while game_loop == True:
        ##Time functionality starts here
        displayclock = clock  # Getting the value of pygame clock as string
        displayclock = str(displayclock)
        displayclock = displayclock.split('=')  # Splitting the string to get the clock value
        displayclock = displayclock[1]  # Selecting the second part of string
        displayclock = displayclock.split(')')  # Splitting furthur
        displayclock = displayclock[0]  # The value in pygame clock
        displayclock = float(displayclock)  # Converting the value to float
        if displayclock > 0:  # Checking weather the value is above 0
            timecal = 1 / displayclock  # Dividing the value by 1 to get the time in milliseconds
            time += timecal  # Subtrating that time from original 300 seconds
        ##Time functionality ends here

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pressed_right = True
                if event.key == pygame.K_LEFT:
                    pressed_left = True
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
        if ball1.y > display_width - 200:
            ball1 = Ball_falling(ballx, bally)
            ball1.y = 0
            try:
                ball1.x = random.choice(random_ball_pos)
                if previous_position[-1] == ball1.x:
                    ball1.x = random.choice(random_ball_pos)
                    previous_position.append(ball1.x)
            except:
                ball1.x = random.choice(random_ball_pos)
                previous_position.append(ball1.x)
            points += 1
            for value in multiples_list:
                if value == points:
                    if ball_speed >= 5.4:
                        bar_speed = 4
                    if ball_speed >= 5.6:
                        print('Highest Speed Reached')
                    else:
                        ball_speed += 0.2
                        print(ball_speed)

        if ball1.y >= bar.y and ball1.x > bar.x - 50 and ball1.x <= bar.x + bar_height - 10:
            lifes -= 1
            ball1.y = 0
            ball1.x = random.choice(random_ball_pos)

        if lifes <= 0:
            game_loop = False
            Game_Over()
        if bar_height == 300:
            screenoff = 500
        if bar_height == 200:
            screenoff = 600
        if bar.x >= screenoff:
            bar.x += -40
        if bar.x <= 0:
            bar.x += 40
        if ball_speed >= 3.6:
            bar_speed = 6
        extra_life = power_ups.life(lifes)
        
        #if extra_life == True:
         #   lifes += 1

        

        # gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        message_to_screen(str(points), red, [740, 565], 25)
        message_to_screen("Lifes: " + str(lifes), red, [50, 565], 25)
        ball1.render()
        bar.render()

        pygame.display.update()
        clock.tick(200)


game_Menu()
