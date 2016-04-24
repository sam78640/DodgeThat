import pygame
import pygame.mixer
import random
import ServerManager as Scores
import UserManager as User
import LeaderBoardManager as Leaderboard
import urllib.request
import urllib.response
import zipfile
from tkinter import *

pygame.init()

# #Defining Colours For Game In RGB Mode
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (0, 0, 255)
yellow = (200, 200, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)
light_yellow = (255, 255, 0)
light_red = (255, 0, 0)
light_blue = (102,169,230)
# #Colours ENDS Here

current_version = "2.0.2"

def get_latest_version():
    url = "http://dodgethat.co.uk/version.php"
    urlr = urllib.request.Request(url)
    urls = urllib.request.urlopen(urlr)
    url_read = urls.read()
    url_read = str(url_read)
    url_read = url_read.split("'")
    url_read = url_read[1].split("'")
    url_read = url_read[0]
    return url_read

latest_version = get_latest_version()



display_width = 800  # Width of Screen
display_height = 600  # Height of Screen
bg_image = "images/bg.jpg"  # Background image file
random_ball_pos = [30, 130, 230, 330, 430, 530]  # Ball positions randomly selected from these
random_ball_pos_right = [330, 430, 530]  # Positions on the right side of screen
random_ball_pos_left = [30, 130, 230]  # Positions on the left side of screen

points = 0  # Global variable for points so it can be initialised for the whole session

colours = [black, red, blue, green, light_red, light_yellow]  # All the colours in an array, not in use at the moment

gameDisplay = pygame.display.set_mode((display_width, display_height))  # Setting the pygame window

pygame.display.set_caption('Dodge That!')  # Setting the window title bar
bg = pygame.image.load(bg_image).convert()  # Loading the background and converting it to optimize it
clock = pygame.time.Clock()  # Loading pygame clock
multiples_list = []  # Empty list for multiples which gets stored from a function
twenty_list = []
barr = "images/bar.png"  # Image location of bar image used in game
image_file = pygame.image.load(barr).convert_alpha()  # Loading the bar image and
#  converting it to alpha so alpha channel gets used for background transparency
user_points = 0
try:
    leaderboard = Leaderboard.LeaderBoardManager()
    scores = leaderboard.run()
except:
    print ("Can't connect to server")

class Xp:
    def write_xp(self, points):
        self.file_write = open("xp.txt", "wt")
        self.file_write.write(str(points * 5))
        self.file_write.close()

    def read_xp(self):
        self.file_read = open("xp.txt", "rt")
        for line in self.file_read:
            return line[0]


def download_file():
    url = "http://dodgethat.co.uk/download/dodgethat.zip"
    filed = urllib.request.Request(url)
    filea = urllib.request.urlopen(filed)
    fileb = filea.read()
    files = open("dodgethat.zip","wb")
    files.write(fileb)
    files.close()
    return True

def unzip():
    zip = zipfile.ZipFile("dodgethat.zip")
    zip.extractall()
    return True


def online_update(username):
        url = "http://dodgethat.co.uk/update_online.php?username="+str(username)+"&password=sameer123&action=online";
        urllib.request.urlopen(url);
        return True
def offline_update(username):
    url = "http://dodgethat.co.uk/update_online.php?username="+str(username)+"&password=sameer123&action=offline";
    urllib.request.urlopen(url);
    return True
def get_coin_value(username):
    url = "http://dodgethat.co.uk/coins.php?username="+str(username)+"&action=show"
    content = urllib.request.Request(url)
    coins = urllib.request.urlopen(content)
    coins_r = str(coins.read())
    coins_r = coins_r.split("'")
    coins_r = coins_r[1].split("'")
    coins_r = coins_r[0]
    return coins_r
def update_coins(username,coins):
    url = "http://dodgethat.co.uk/coins.php?username="+str(username)+"&coins="+str(coins)+"&password=sameer123"
    urllib.request.urlopen(url)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = x

    def shoot(self):
        return True

    def render(self):
        pygame.draw.rect(gameDisplay, red, (self.x, self.y, 100, 100))


##Class for general image loading
class Image:
    def __init__(self, x, y, width, height, location):  # Building a class constructor
        self.x = x  # storing x-axis value
        self.y = y  # Storing y-axis value
        self.width = width  # Storing image width value
        self.height = height  # Storing image height value
        self.image_location = location  # Storing the image location
        self.image = "images/" + image_location  # Finalising the image location

    def load(self):
        self.display_image = pygame.image.load(
            self.image).convert_alpha()  # Loading the image assuming it would be a png file
        self.display_image = pygame.transform.scale(self.display_image, (
        self.width, self.height))  # Transforming image to correct width and height

    def render(self):
        self.load()  # Call the function above
        gameDisplay.blit(self.display_image, (self.x, self.y))  # Displaying image on the screen


try:
    server = Scores.Scores()  # Creating a Server Instance
    global_high_score = server.get_num_score()  # Getting Global High Score From Server

except:
    print("cannot connect to server")  # If No Internet Connection
    global_high_score = "Cannot Connect"


# Health Management
class Health:
    def __init__(self, x, y, width, height):
        self.x = x  # x-axis of health image
        self.y = y
        self.width = width
        self.height = height
        self.image = "images/health.png"

    def load(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        self.display_image = pygame.transform.scale(self.display_image, (self.width, self.height))

    def render(self):
        self.load()
        gameDisplay.blit(self.display_image, (self.x, self.y))


class Dodge_bar():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = "images/bar.png"

    def render(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        self.display_image = pygame.transform.scale(self.display_image, (self.width, self.height))
        gameDisplay.blit(self.display_image, (self.x, self.y))


class Ball_falling():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = "images/ball.png"

    def render(self):
        self.angle = 0
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

    def life():
        return True

    def gun(self):
        return False


##Function to display text on screen
def message_to_screen(msg, color, position, fontsize):
    font = pygame.font.Font("fonts/3" + str(2 + 2) + ".ttf", fontsize)  # Rendering font
    screen_text = font.render(msg, True, color)  # Inserting message into font and rendering colour
    gameDisplay.blit(screen_text, [position, position])  # Displaying text on the screen


def multiples(m, count1, count2, list1):
    for i in range(count1, count2):
        value = i * m
        list1.append(value)
    return True


run_multiples = multiples(4, 0, 100, multiples_list)  # Generating multiples from the function above to adjust speed in game
twenty_run_multiples = multiples(20, 0, 100, twenty_list)
name = 0
def enter_Name():
    global name
    global user_points
    offline_update(name)
    name = ""
    enter_name = True
    name_entered = False
    name = ""
    login_image = pygame.image.load("images/login.jpg").convert()

    while enter_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                offline_update(name)
                pygame.quit()
        if name != "":
            name_entered = True
        gameDisplay.fill(white)
        gameDisplay.blit(login_image,(0,0))
        #message_to_screen("Waiting For Username", red, [200, 100], 35)
        #message_to_screen("Enter The Username You Previously Used", black, [120, 200], 30)
        #message_to_screen("OR", black, [380, 250], 35)
        #message_to_screen("Choose any username to create a new account", black, [90, 300], 30)
        pygame.display.update()
        clock.tick(10)
        if name_entered:
            name = name.lower()
            name = name.replace(' ', '')
            if name == "global" or name == "blank":
                name_entered = False
                name = ""
            try:
                user_details = User.Get_Details(name)
                user_ex = user_details.get_points()
                if user_ex == "false":
                    user_details.register_user()
                    print("Account Created! Always use this name to access your score")
                user_points = user_details.get_points()
            except:
                user_points = "Can't Connect To Server"
            print(user_points)
            print("Continue to game...")
            if name_entered:
                enter_name = False
                game_Menu()

        box = DialogBox()
        box.box()




def leader_board():
    global scores
    leaderboard_menu = True
    global leaderboard
    global scores
    leaderboard_image = pygame.image.load("images/leaderboard.jpg").convert()
	
    try:
        leaderboard = Leaderboard.LeaderBoardManager()
        scores = leaderboard.run()
    except:
        print ("Can't Connect to server")

    while leaderboard_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                offline_update(name)
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    leaderboard_menu = False
                    game_Menu()


        try:
            gameDisplay.fill(white)
            score1 = scores[0]
            score1_split = score1.split(",")
            score1_name = score1_split[0]
            score1_score = score1_split[1]

            score2 = scores[1]
            score2_split = score2.split(",")
            score2_name = score2_split[0]
            score2_score = score2_split[1]

            score3 = scores[2]
            score3_split = score3.split(",")
            score3_name = score3_split[0]
            score3_score = score3_split[1]

            score4 = scores[3]
            score4_split = score4.split(",")
            score4_name = score4_split[0]
            score4_score = score4_split[1]

            score5 = scores[4]
            score5_split = score5.split(",")
            score5_name = score5_split[0]
            score5_score = score5_split[1]

            gameDisplay.fill(white)
            gameDisplay.blit(leaderboard_image,(0,0))
            #message_to_screen("Leaderboard", black, [200, 100], 35)

            message_to_screen(score1_name,white,[130,130],30)
            message_to_screen(str(score1_score),white,[630,130],30)

            message_to_screen(score2_name,white,[130,215],30)
            message_to_screen(str(score2_score),white,[630,215],30)

            message_to_screen(score3_name,white,[130,310],30)
            message_to_screen(str(score3_score),white,[630,310],30)

            message_to_screen(score4_name,white,[130,400],30)
            message_to_screen(str(score4_score),white,[630,400],30)

            message_to_screen(score5_name,white,[130,490],30)
            message_to_screen(str(score5_score),white,[630,490],30)

        except:
            gameDisplay.fill(white)
            message_to_screen("Can't Connect To Server",red,[200,200],30)
            message_to_screen("Press B to go back",red,[200,350],30)


        #message_to_screen("Press B To Go Back",black,[200,500],25)
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= 275 and mouse_pos[0] < 507 and mouse_pos[1] >= 548 and mouse_pos[1] < 585:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                leaderboard_menu = False
                game_Menu()
        pygame.display.update()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        clock.tick(10)

class DialogBox:
    def box(self):
        global name
        self.master = Tk()
        self.master.title("Login Or Create Account / Enter Username")
        Label(self.master, text="Username").grid(row=0)
        self.e1 = Entry(self.master)
        self.e1.grid(row=0, column=1)
        Button(self.master, text='Login/Register', command=self.login_user).grid(row=3, column=0, sticky=W, pady=4)
        self.e1.bind('<Return>', self.login_user)
        mainloop()

    def login_user(self, callback=False):
        global name
        name = self.e1.get()
        self.master.destroy()


def game_Menu():
    global name
    global user_points

    online_update(name)


    menu_image = "images/menu.jpg"
    image_menu = pygame.image.load(menu_image).convert()

    
    try:
        global_high_score = server.get_num_score()
        if global_high_score == "":
            global_high_score = "Scores Not Found"
    except:
        print("cannot connect")
        global_high_score = "Cannot Connect"

    try:
        user_update = User.Get_Details(name)
        user_points = user_update.get_points()
    except:
        user_points = "Can't Connect To Server"
    game_menu = True
    while game_menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                offline_update(name)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game_menu = False
                    gameLoop()
                if event.key == pygame.K_q:
                    offline_update(name)
                    quit()
                if event.key == pygame.K_l:
                    name = ""
                    game_menu = False
                    enter_Name()
                if event.key == pygame.K_o:
                    game_menu = False
                    leader_board()

        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 240 and mouse_pos[1]  < 302:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                gameLoop()
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 316 and mouse_pos[1] < 375:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                leader_board()
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 400 and mouse_pos[1] < 458:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                enter_Name()
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 486 and mouse_pos[1] < 545:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                offline_update(name)
                quit()

        coins = get_coin_value(name)

        gameDisplay.fill(white)
        gameDisplay.blit(image_menu,(0,0))
        message_to_screen(str(global_high_score), white, [520, 170], 27)
        message_to_screen(str(name), white, [150, 12], 27)
        message_to_screen(str(user_points), white, [725, 15], 25)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        pygame.display.update()
        clock.tick(1000)


def no_repeats(last_pos, new_pos):
    last_pos_li = last_pos
    if last_pos_li[-1] == new_pos:
        return True
    else:
        return False

def Game_Over():
    gameover = True
    global points
    global user_points
    global name

    gameover_image = pygame.image.load("images/gameover.jpg").convert()

    points_display = 0
    try:
        user_update = User.Get_Details(name)
        user_points = user_update.get_points()
        user_update.upload_score(points)
        coins = get_coin_value(name)
        coins = int(coins)

        coin_new = points * 5

        coin_n = coin_new + coins
        update_coins(name,coin_n)



        if int(user_points) < points:
            user_update.update_score(points)

        user_high_score = user_update.get_points()
    except:
        global_high_score = "Can't Connect To Internet"
        user_high_score = "Can't Connect To Server"
    try:
        global_high_score = int(server.get_num_score())
        server.run(points)
    except:
        print("cannot connect")

    while gameover == True:

        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] >= 175 and mouse_pos[0] < 550 and mouse_pos[1] >= 275 and mouse_pos[1] < 345:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                gameLoop()
        if mouse_pos[0] >= 175 and mouse_pos[0] < 550 and mouse_pos[1] >= 360 and mouse_pos[1] < 427:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                gameover = False
                game_Menu()
        if mouse_pos[0] >= 175 and mouse_pos[0] < 550 and mouse_pos[1] >= 445 and mouse_pos[1] < 510:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                offline_update(name)
                quit()
        if points_display < points:
            points_display += 1

        gameDisplay.fill(white)
        gameDisplay.blit(gameover_image,(0,0))
        #message_to_screen("GAME OVER!", red, [195, 180], 60)
        message_to_screen(str(points_display), white, [440, 31], 60)
        message_to_screen(str(user_high_score), white, [370, 566], 30)
        #message_to_screen("Press R to play again", black, [200, 290], 25)
        #message_to_screen("Press M for main menu", black, [200, 320], 25)
        #message_to_screen("Press Q to Quit", black, [200, 350], 25)
        try:
            if server.compare_scores(int(global_high_score), points):
                #message_to_screen(str(global_high_score), light_blue, [235, 170], 30)
                print ("Not Connected")

            if not server.compare_scores(int(global_high_score), points):
                #message_to_screen("Global High Score: " + str(global_high_score), red, [200, 240], 20)
                message_to_screen(str(global_high_score), light_blue, [555, 200], 30)

        except:
            message_to_screen("Can't Connect To Server", red, [200, 240], 20)

        pygame.display.update()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                offline_update(name)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
                if event.key == pygame.K_r:
                    gameLoop()
                if event.key == pygame.K_m:
                    gameover = False
                    game_Menu()



def gameLoop():
    global points
    wait_time = True
    points = 0
    bary = 530
    barx = 300
    bar_width = 10
    bar_height = 300
    ball_speed = 3.8
    bar_speed = 3
    ballx = random.choice(random_ball_pos)
    bally = 50
    ball1 = Ball_falling(ballx, bally)
    bar = Dodge_bar(barx, bary, bar_height, bar_width)
    game_loop = True
    pressed_right = False
    pressed_left = False
    time = 0
    screenoff = 0
    health_width = 150
    health_height = 15
    health_num = 150
    heart = False
    heart_x = random.choice(random_ball_pos)
    heart_y = 0
    heart_time = random.randint(20, 40)
    heart_image = pygame.image.load("images/heart.png").convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (50, 50))
    last_pos = []
    ball2 = False
    ball2x = random.choice(random_ball_pos)
    ball2y = 50
    while game_loop == True:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        # Health bar functionality
        health = Health(150, 575, health_width, health_height)
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
                offline_update(name)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pressed_right = True
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                    # if event.key == pygame.K_SPACE:
                    #   shoot = bullet.shoot()
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
        if ball1.y > display_width - 200:  # When the ball is dodged
            ball1.y = 0
            ball1.x = random.choice(random_ball_pos)
            try:
                compare_last_pos = no_repeats(last_pos, ball1.x)
                if compare_last_pos == True:
                    ball1.x = random.choice(random_ball_pos)
                    last_pos.append(ball1.x)
                elif compare_last_pos == False:
                    ball1.x = ball1.x
                    last_pos.append(ball1.x)
            except:
                ball1.x = random.choice(random_ball_pos)
                last_pos.append(ball1.x)
            points += 1
            for value in multiples_list:
                if value == points:
                    if ball_speed >= 5.4:
                        bar_speed = 4

                    if ball_speed >= 6.6:
                        print('Highest Speed Reached')

                    else:
                        ball_speed += 0.2
                        print(ball_speed)

        if ball1.y >= bar.y and ball1.x > bar.x - 50 and ball1.x <= bar.x + bar_height - 10:
            health_num -= 50
            ball1.y = 0
            ball1.x = random.choice(random_ball_pos)
            last_pos.append(ball1.x)

        if round(ball_speed, 1) >= 4.8:
            ball2 = True

        if ball2 == True:
            ball2_f = Ball_falling(ball2x, ball2y)
            ball2y += ball_speed
            if ball2y >= bar.y and ball2x > bar.x - 50 and ball2x <= bar.x + bar_height - 10:
                health_num -= 50
                ball2y = 0
                ball2x = random.choice(random_ball_pos)
            if ball2y > display_width - 200:
                points += 1
                ball2y = 0
                ball2x = random.choice(random_ball_pos)

        if health_width <= 0:
            game_loop = False
            Game_Over()

        if heart_y > display_width - 200:
            heart_y = 0
            heart_x = random.choice(random_ball_pos)
            heart = False

        if health_width > health_num:
            health_width -= 1

        if health_width < health_num:
            health_width += 1

        if bar_height == 300:
            screenoff = 500

        if bar_height == 200:
            screenoff = 600

        if bar.x >= screenoff:
            bar.x -= 6

        if bar.x <= 0:
            bar.x += 6

        if ball_speed >= 3.6:
            bar_speed = 6

        if heart == True:
            heart_y += 3
            if heart_y >= bar.y and heart_x > bar.x - 50 and heart_x <= bar.x + bar_height - 10:
                health_num += 50
                heart_y = 0
                heart_time = round(time) + 30
                heart = False
        if round(time) == heart_time:
            if health_num < 300:
                heart = True
            else:
                heart = False
                heart_time = round(time) + 30

        # gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        message_to_screen(str(points), red, [740, 565], 25)
        message_to_screen("Health ", red, [50, 569], 25)
        ball1.render()
        bar.render()
        health.render()
        if heart == True:
            gameDisplay.blit(heart_image, (heart_x, heart_y))
        if ball2 == True:
            ball2_f.render()

        pygame.display.update()
        clock.tick(120)
        if wait_time==True:
            pygame.time.delay(1000)
            wait_time = False

def update_screen():
    updating = True
    download_update = False
    extract_update = False
    while updating:
        message_to_screen("Please Wait While Updating Game",red,[100,100],30)

        if download_update == True:
            message_to_screen("Update Downloaded... Updating...",red,[100,100],30)
        if extract_update == True:
            message_to_screen("Game Updated... Please Restart Your Game",red,[100,100],30)
            pygame.quit()
            quit()
        gameDisplay.fill(white)
        clock.tick(10)
        download_update = download_file()
        extract_update = unzip()
if current_version != latest_version:
    update_screen()
enter_Name()
