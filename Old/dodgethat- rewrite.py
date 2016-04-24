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
random_ball_pos = [0,100,200,300,400,500]

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

        
def message_to_screen(msg,color,position,fontsize):#Test displaying to the screen
    font = pygame.font.SysFont("comicsansms", fontsize)#Defining font style and font size of the text
    screen_text = font.render(msg, True, color)#Rendering the text
    gameDisplay.blit(screen_text, [position,position])        
def multiples (m,count1,count2):
    for i in range(count1,count2):
        value = i*m
        multiples_list.append(value)

run_multiples = multiples(2,0,100)
def Game_Over():
    gameover = True
    global points
    while gameover==True: #When the games ends
            gameDisplay.fill(white) #Fill the background white
            message_to_screen("GAME OVER!!!", red, [195,180],70) #Text on screen of Game over on 195y and 180x with 70 font-size
            message_to_screen("Score: "+str(points), black, [320,90],40) #Text on screen of Score and displaying final score
            message_to_screen("Press R to play again", black, [200,290],25) #Text on screen which says to play again
            message_to_screen("Press M for main menu", black, [200,320],25) #Text on screen which says to go on main menu
            message_to_screen("Press Q to Quit", black, [200,350],25) #Text on screen which says to quit
            pygame.display.update() #Updates python window
            for event in pygame.event.get(): #Get events from pygame
                if event.type == pygame.QUIT: #If the user clicks the red cross button
                    pygame.quit()#The pygame quits
                    quit()#The whole program quits
                if event.type == pygame.KEYDOWN: #If the user press any key on keyboard
                    if event.key == pygame.K_q: #In this case if the user press q
                        pygame.quit#The game exit becomes true and game quits
                        quit()
                    if event.key == pygame.K_r: #If the key pressed is R
                        gameLoop() #The game loop is ran again
                    if event.key == pygame.K_m: #If the key pressed is M
                        gameover = False #Game over becomes false and exits it's loop
                        game_Menu()
def game_Menu():#Game menu which lets user choose what to do
    game_menu = True#This whole loop will run while this variable stays true

    while game_menu == True: #While this game menu varible is true, these statements will executes
        for event in pygame.event.get(): #Getting the events from pygame
            if event.type == pygame.QUIT: #If the user clicks the red cross button at to
                pygame.quit() #pygame will quit
                quit() #the whole program will quit
            if event.type == pygame.KEYDOWN: #If the user press any key on key
                if event.key == pygame.K_c: #in this case if the key pressed is c
                    game_menu = False #The game menu will go false and quit the menu loop
                    gameLoop() #Then it will start the game loop
                if event.key == pygame.K_q: #If the button pressed is Q
                    pygame.quit() #The pygame will quit
                    quit() #The whole program will quit
        gameDisplay.fill(white)
        #gameDisplay.blit(bg,(0,0))#Background of pygame window   
        message_to_screen("Dodge That",green,[200,100],70) #Calling the function defined previously to display text on screen and in this case Displaying the name of game
        message_to_screen("Press C to Start",black,[220,250],25)#Displaying menu options
        message_to_screen("Press Q to Quit",black,[220,300],25)##########################
        
        pygame.display.update()#Updating the screen of pygame window to keep track of any changes.
        clock.tick(10)
def gameLoop():
    global points
    points = 0
    bary = 560
    barx = 300
    ball_speed = 2
    bally = random.randint(0,display_width-10)
    ballx = 50
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
                    pressed_right = True
                if event.key == pygame.K_LEFT:
                    pressed_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pressed_right = False
                if event.key == pygame.K_LEFT:
                    pressed_left = False

        if pressed_right == True:
            bar.x += 3
        if pressed_left == True:
            bar.x += -3
        
        ball1.y += ball_speed
        if ball1.y > display_width -200:
            balls_x = random.randrange (0,display_width)
            ball_color = random.choice(colours)
            balls_y = 50
            ball1 = Ball_falling(ballx,bally)
            ball1.y = 0
            ball1.x = random.randrange (0,display_width-10)
            points += 1
            for value in multiples_list:
                if value==points:
                    if ball_speed >= 5.6:
                        print ('Highest Speed Reached')
                    else:
                        ball_speed += 0.4
                        print (ball_speed)
            
        if ball1.y >= bar.y and ball1.x > bar.x-50 and ball1.x <= bar.x+290 :
            
            game_loop = False
            Game_Over ()
            
        if bar.x >= 500:
            bar.x += -40
        if bar.x <= 0:
            bar.x += 40
        

        gameDisplay.fill(white)
        gameDisplay.blit(bg,(0,0))
        message_to_screen("Points: "+str(points), red, [30,30],25)
        ball1.render()
        bar.render()
        
        pygame.display.update()
    clock.tick(30)
    
game_Menu()
