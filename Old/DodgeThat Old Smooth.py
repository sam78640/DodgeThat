import pygame, pygame.mixer, random, time, csv, math
from pygame.locals import *

pygame.init()#pygame initialising

#Colours Defining 
black = (0,0,0)
white =(255,255,255)
red = (200,0,0)
blue = (0,0,255)
green = (0,155,0)
yellow = (200,200,0)
light_green = (0,255,0)
light_yellow = (255,255,0)
light_red = (255,0,0)

#Images
bg = pygame.image.load("images/bg.jpg")

#Sounds#
dodged_sound = pygame.mixer.Sound('audio/point.wav')
special_apple_sound = pygame.mixer.Sound('audio/special.wav')
game_over_sound = pygame.mixer.Sound('audio/gameover.wav')
sound_intro = pygame.mixer.Sound('audio/intro.wav')

#Display Size
display_width = 800
display_height = 600

#Points
points = 0

colours =[black, red, blue, green, light_red, light_yellow]

gameDisplay = pygame.display.set_mode([display_width,display_height])

pygame.display.set_caption('Dodge That!')

clock = pygame.time.Clock()
#Defining multiples of 15
multiples_of_fif = []
def multiples(m, count1,count2):
    for i in range(count1,count2):
        value = i*m
        multiples_of_fif.append(value)
        
run  = multiples(2,1,300)
class Wall(pygame.sprite.Sprite):
    def __init__(self,color,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(pygame.color.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def message_to_screen(msg,color,position,fontsize):#Test displaying to the screen
    font = pygame.font.SysFont("comicsansms", fontsize)#Defining font style and font size of the text
    screen_text = font.render(msg, True, color)#Rendering the text
    gameDisplay.blit(screen_text, [position,position])#Displaying the text according to the called positions when running subroutine
    
def random_balls(x,y,colour1):
    pygame.draw.circle(gameDisplay, colour1,[x, y],20)
    #gameDisplay.blit(ball,(x,y))
    
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
                        game_Menu() #It jumps to the main menu by calling the function of game_Menu
                        
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
        gameDisplay.blit(bg,(0,0))#Background of pygame window   
        message_to_screen("Dodge That",green,[200,100],70) #Calling the function defined previously to display text on screen and in this case Displaying the name of game
        message_to_screen("Press C to Start",black,[220,250],25)#Displaying menu options
        message_to_screen("Press Q to Quit",black,[220,300],25)##########################
        
        pygame.display.update()#Updating the screen of pygame window to keep track of any changes.
        clock.tick(10) #Defining how many times this loop will run in a second. Also referred as FPS or Game Clock
        
def gameLoop():
    global points
    
    #Variables
    points = 0
    ball_speed = 10
    timewait = True
    speed_increasing = False
    ball_leady = 50
    leadx = 300
    leady = 500
    height = 300
    width = 10
    gameover = False
    game_loop = True
    pressed_right = False
    pressed_left = False
    balls_x = random.randrange(0, display_width)
    ball_color = random.choice(colours)
    balls_y = 50
    
    #Game Buttons
    while game_loop == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pressed_right = True
                    #leadx += 50
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                    #leadx += -50
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pressed_right = False
                if event.key == pygame.K_LEFT:
                    pressed_left = False

        #Game Logic           
        if pressed_right == True:
            leadx += 11
        if pressed_left == True:
            leadx += -11
        if balls_y > display_width -200:
            balls_x = random.randrange (0,display_width)
            ball_color = random.choice(colours)
            balls_y = 50
            random_balls(balls_x,balls_y,ball_color)
            points += 1
            dodged_sound.play()
            for value in multiples_of_fif:
                if value==points:
                    speed_increasing = True
                    if speed_increasing == True:
                        if ball_speed <= 23:
                            ball_speed += 1
                            speed_increasing = False
                            print ('Current speed: '+str(ball_speed))
                        else:
                            print ('Current speed: '+str(ball_speed))
                            speed_increasing = False
        if balls_y >= leady and balls_x > leadx and balls_x <= leadx+height:
            print ('Crashed')
            game_loop = False
            Game_Over()
        gameDisplay.fill(white)
        
        random_balls(balls_x,balls_y,ball_color)
        balls_y += ball_speed
        if leadx >= 500:
            leadx += -40
        if leadx <= 0:
            leadx += 40
            
        #Game Display    
        message_to_screen("Points: "+str(points), red, [30,30],25)
        pygame.draw.rect(gameDisplay,ball_color,(leadx,leady,height,width))
        pygame.display.update()
        clock.tick(60)
        if timewait==True:
            pygame.time.delay(1000)
            timewait = False

game_Menu()
