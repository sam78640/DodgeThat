import pygame
import pygame.mixer
import random
import ServerManager as Scores
import UserManager as User
import LeaderBoardManager as Leaderboard
import urllib.request
import urllib.response
from tkinter import *
import os


#Initialising Pygame
pygame.init()

#Colours Starts Here
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue = (0, 0, 255)
yellow = (200, 200, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)
light_yellow = (255, 255, 0)
light_red = (255, 0, 0)
light_blue = (102,169,230)
game_bg_color = (48,68,88)

#Colours ends here

#Game display configurations starts here
display_width = 800  # Width of Screen
display_height = 600  # Height of Screen
bg_image = "images/bg.jpg"  # Background image file
colours = [black, red, blue, green, light_red, light_yellow]  # All the colours in an array, not in use at the moment
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Setting the pygame window
pygame.display.set_caption('Dodge That!')  # Setting the window title bar
bg = pygame.image.load(bg_image).convert()  # Loading the background and converting it to optimize it
#Game display configuratios ends here

#Gameplay configurations starts here
points = 0 #Global variable for user score
random_ball_pos = [30, 130, 230, 330, 430, 530]  # Ball positions randomly selected from these
random_ball_pos_right = [330, 430, 530]  # Positions on the right side of screen
random_ball_pos_left = [30, 130, 230]  # Positions on the left side of screen
clock = pygame.time.Clock()  # Loading pygame clock
multiples_list = []  # Empty list for multiples which gets stored from a function
twenty_list = []
barr = "images/bar.png"
image_file = pygame.image.load(barr).convert_alpha()  # Loading the bar image and
#  converting it to alpha so alpha channel gets used for background transparency
#Gameplay configurations ends here

#Leaderboard connection to server
try:
    leaderboard = Leaderboard.LeaderBoardManager()
    scores = leaderboard.run()
except:
    print ("Cannot connect to server at this moment")
#Leaderboard connection ends here
#Function to set the user as online
def online_update(username):
        url = "http://dodgethat.co.uk/update_online.php?username="+str(username)+"&password=sameer123&action=online";
        urllib.request.urlopen(url);
        return True
#Functions Online ends here

#Function to set the user as offline when it quits the game
def offline_update(username):
    url = "http://dodgethat.co.uk/update_online.php?username="+str(username)+"&password=sameer123&action=offline";
    urllib.request.urlopen(url);
    return True
#Function Offline ends here

#User coin functionality starts here
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
#User coin functionality ends here

#Server connection starts here
try:
    server = Scores.Scores()
    global_high_score = server.get_num_score()
except:
    print ("Cannot connect to server at this moment")
    global_high_score = "Connection failed"

#Heath Management Starts Here
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
#Health management ends here

#User paddle configurations starts here
class Dodge_bar():
    def __init__(self, x, y, width, height,path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = path

    def render(self):
        self.display_image = pygame.image.load(self.image).convert_alpha()
        self.display_image = pygame.transform.scale(self.display_image, (self.width, self.height))
        gameDisplay.blit(self.display_image, (self.x, self.y))
#User paddle configurations ends here

#Ball configurations starts here
class Ball_falling():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = "images/ball.png"

    def render(self):
        self.angle = 0
        self.display_image = pygame.image.load(self.image).convert_alpha()
        gameDisplay.blit(self.display_image, (self.x, self.y))
#Ball configurations ends here

#Class for PowerUps
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
#PowerUps configurations ends here

#Function to display text on the screen
def message_to_screen(msg, color, position, fontsize):
    font = pygame.font.Font("fonts/3" + str(2 + 2) + ".ttf", fontsize)  # Rendering font
    screen_text = font.render(msg, True, color)  # Inserting message into font and rendering colour
    gameDisplay.blit(screen_text, [position, position])  # Displaying text on the screen
#Funtion to display text ends here

#Generating multiples
def multiples(m, count1, count2, list1):
    for i in range(count1, count2):
        value = i * m
        list1.append(value)
    return True
run_multiples = multiples(4, 0, 100, multiples_list)  # Generating multiples from the function above to adjust speed in game
twenty_run_multiples = multiples(20, 0, 100, twenty_list)
#Generating multiples ends here

#initialising user's name
name = 0
#user's name Initialising ends here


#Downloading images from the server
def download_images_from_server(path):
    url = "http://dodgethat.co.uk/"+path
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    resp = resp.read()
    file = open (path,"wb")
    file.write(resp)
    file.close()


#function for the login screen
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
#Login screen ends here

#DialogBox Functionality starts here
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
#DialogBox functionality ends here

#Leaderboard screen starts here
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
            gameDisplay.blit(leaderboard_image,(0,0))

            ratios = [1,215/130,310/130,400/130,490/130] #Ratio for the text position, done by the image sizing
            starting_value = 130
            i = 0
            for score in scores:
                split_score = score.split(",")
                name = split_score[0]
                points = split_score[1]
                message_to_screen(name,white,[130,starting_value * ratios[i]],30)
                message_to_screen(str(points),white,[630,starting_value * ratios[i]],30)
                i += 1

        except:
            gameDisplay.fill(white)
            message_to_screen("Can't Connect To Server",red,[200,200],30)
            message_to_screen("Press B to go back",red,[200,350],30)

        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= 275 and mouse_pos[0] < 507 and mouse_pos[1] >= 548 and mouse_pos[1] < 585:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                leaderboard_menu = False
                game_Menu()
        pygame.display.update()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        clock.tick(10)
#Leaderboard screen ends here

#Game menu screen starts here
def game_Menu():
    global name
    global user_points


    online_update(name)


    menu_image = "images/menu.jpg"
    image_menu = pygame.image.load(menu_image).convert()

    user_details = get_user_details(name)
    username = user_details[0]
    user_coins = user_details[1]


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
                if event.key == pygame.K_s:
                    game_menu = False
                    shop()

        mouse_pos = pygame.mouse.get_pos()

        #Play Button
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 240 and mouse_pos[1]  < 302:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                set_health()

        #Leaderboard Button
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 316 and mouse_pos[1] < 375:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                leader_board()

        #Logout Button
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 400 and mouse_pos[1] < 458:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                enter_Name()

        #Quit Button
        if mouse_pos[0] >= 185 and mouse_pos[0] < 585 and mouse_pos[1] >= 486 and mouse_pos[1] < 545:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                offline_update(name)
                quit()


        #Shop button
        if mouse_pos[0] >= 624 and mouse_pos[0] <= 784 and mouse_pos[1] >= 519 and mouse_pos[1] <= 585:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                game_menu = False
                shop()

        coins = get_coin_value(name)

        gameDisplay.fill(white)
        gameDisplay.blit(image_menu,(0,0))
        message_to_screen(str(global_high_score), white, [520, 170], 27)
        message_to_screen(str(name), white, [150, 12], 27)
        message_to_screen(str(user_points), white, [725, 15], 25)
        message_to_screen("Cash: $" + str(user_coins),white,(517,46),20)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        pygame.display.update()
        clock.tick(60)
#Game menu screen ends here

#Game over screen starts here
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

        coin_display = coins

        update_coins(name,coin_n)



        if int(user_points) < points:
            user_update.update_score(points)

        user_high_score = user_update.get_points()
    except:
        global_high_score = "Can't Connect To Server"
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
                set_health()
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

        if coin_display < coin_n:
            coin_display += 5

        gameDisplay.fill(white)
        gameDisplay.blit(gameover_image,(0,0))
        message_to_screen(str(points_display), white, [440, 31], 60)
        message_to_screen(str(user_high_score), white, [370, 566], 30)
        message_to_screen("Cash: $"+str(coin_display), white, [550, 46], 30)
        try:
            if server.compare_scores(int(global_high_score), points):
                print ("Not Connected")

            if not server.compare_scores(int(global_high_score), points):
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
#Game over screen ends here

#Getting user details
def get_user_details(username):
    details = []
    url = "http://dodgethat.co.uk/user_details.php?username="+str(username)
    ope = urllib.request.Request(url)
    read = urllib.request.urlopen(ope)
    read = str(read.read())
    spl = read.split("b'")
    spl = spl[1]
    spl = spl.split(",")
    for detail in spl:
        details.append(detail)
    return details
#Getting all the bar details from server
def get_all_bars(page = 1):
    all_bars = []
    load = urllib.request.Request("http://dodgethat.co.uk/bars/bars.php?bars=all&page="+str(page))
    op = urllib.request.urlopen(load)
    read = str(op.read())
    scanned = read.split("b'")
    scanned = scanned[1]
    each_item = scanned.split("\\n")
    looper = 0
    for items in each_item:
        if looper < len(each_item) - 1:
            all_bars.append(items)
        looper += 1
    return all_bars
#Getting bar details ends here

#Buying Bar
def buy_bar(username,bar_name):
    url = "http://dodgethat.co.uk/bars/bars.php?buy=1&username="+str(username)+"&bar="+str(bar_name)
    push = urllib.request.urlopen(url)
#Buying bars ends here

#Get User Owned Bars
def get_user_bars(username):
    owned_bars = []
    url = "http://dodgethat.co.uk/bars/bars.php?get_bar=1&username="+str(username)
    url_open = urllib.request.Request(url)
    url_read = urllib.request.urlopen(url_open)
    res = str(url_read.read())
    spl = res.split("b'")
    spl = spl[1]
    spl = spl.split("\\n")
    for bars in spl:
        owned_bars.append(bars)
    del owned_bars[-1]

    return owned_bars
#Get user owned bars end here

#Get each bar detail
def get_each_bar_detail(bar_id):
    details = []
    url = "http://dodgethat.co.uk/bars/bars.php?get_bar=1&barid="+str(bar_id)
    url_open = urllib.request.Request(url)
    url_req = urllib.request.urlopen(url_open)
    url_read = str(url_req.read())
    spl = url_read.split("b'")
    spl = spl[1]
    spl = spl.split(",")
    for detail in spl:
        details.append(detail)
    return details
#Each bar detail ends here

#Get user selected bar
def get_user_selected_bar(username):
    url = "http://dodgethat.co.uk/bars/bars.php?get_selected=1&username="+str(username)
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    read = str(res.read())
    spl = read.split("b'")
    spl = spl[1]
    spl = spl.split(",")
    bar_id = spl[0]
    return bar_id
#Get user selected bar ends here

#Update user selected bar
def update_user_bar(username,bar_name):
    url = "http://dodgethat.co.uk/bars/bars.php?update_selected=1&username="+str(username)+"&bar_name="+bar_name
    push = urllib.request.urlopen(url)
#Update user selected bar ends here

#Getting maximum shop pages
def get_max_shop_pages():
    url = "http://dodgethat.co.uk/bars/bars.php?get_max"
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    rea = str(res.read())
    spl = rea.split("b'")
    spl = spl[1]
    spl = spl.split(",")
    return spl[0]

#Shop Starts here
def shop(page = 1):
    global name
    shop_loop = True
    shop_image = pygame.image.load("images/store.jpg").convert()
    page = page
    all_bars = get_all_bars(page)
    previous_page = []
    previous_page.append(page)
    number_of_bars_bought = []
    user_details = get_user_details(name)
    username = user_details[0]
    user_coins = user_details[1]
    button_text = "Buy Now"
    get_user_bar = get_user_bars(name)
    user_bar_names = []
    max_pages = get_max_shop_pages()
    get_user_selected = get_user_selected_bar(name)
    user_selected_bar_name = get_each_bar_detail(get_user_selected)

    if len(user_selected_bar_name) >= 1:
        user_selected_bar_name = user_selected_bar_name[0]

    if len(get_user_bar) >= 1:
        for bar_id in get_user_bar:
            bar_detail = get_each_bar_detail(bar_id)
            user_bar_names.append(bar_detail[0])

    while shop_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                offline_update(name)
                pygame.quit()
        gameDisplay.fill(white)
        gameDisplay.blit(shop_image,(0,0))
        mouse = pygame.mouse.get_pos()

        #Back Button
        if mouse[0] >= 561 and mouse[0] <= 666 and mouse[1] >= 535 and mouse[1] <= 587:
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                if page == 1:
                    new_page = int (max_pages)
                    shop_loop = False
                    shop(new_page)
                if page > 1:
                    new_page = previous_page[-1] - 1
                    shop_loop = False
                    shop(new_page)
        #Forward Button
        if mouse[0] >= 684 and mouse[0] <= 794 and mouse[1] >= 535 and mouse[1] <= 587:
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                if previous_page[-1] == int(max_pages):
                    new_page = 1
                    shop_loop = False
                    shop(new_page)
                else:
                    new_page = previous_page[-1] + 1

                    shop_loop = False
                    shop(new_page)
        #Back to main menu Button
        if mouse[0] >= 32 and mouse[0] <= 246 and mouse[1] >= 536 and mouse[1] <= 583:
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                shop_loop = False
                game_Menu()

        i = 0
        for bars in all_bars:
            sorted_bars = bars.split(",")
            bar_name = sorted_bars[0]
            path = sorted_bars[1]

            #Checks if the image exist in user's computer
            image_check = os.path.exists(path)
            #If the image doesn't exists
            if image_check == False:
                #It downloads the image from the server
                download_images_from_server(path)

            speed = int (sorted_bars[2])
            health = int (sorted_bars[3])
            display_name = sorted_bars[4]
            ratio_cal = 103 * i
            cost = sorted_bars[5]
            speed_im = pygame.image.load("images/progress_bar.png").convert()
            health_im = pygame.image.load("images/progress_bar.png").convert()
            scaled_speed = pygame.transform.scale(speed_im,(speed * 15,19))
            scaled_health = pygame.transform.scale(health_im,(health * 15,19))
            bar_image = pygame.image.load(path).convert_alpha()
            scaled_bar = pygame.transform.scale(bar_image,(300,10))
            for owned in user_bar_names:
                if owned == bar_name:
                    button_text = "Select"
                    break
                elif owned != bar_name:
                    button_text = "Buy Now"

            if bar_name == user_selected_bar_name:
                button_text = "Selected"

            message_to_screen(display_name,black,(433,126 + ratio_cal),25)
            message_to_screen("$" + str(cost),black,(433,152 + ratio_cal),25)
            message_to_screen(button_text,white,(607,132 + ratio_cal),35)
            gameDisplay.blit(scaled_bar,(67,128 + ratio_cal))
            gameDisplay.blit(scaled_speed,(122,160 + ratio_cal))
            gameDisplay.blit(scaled_health,(341,160 + ratio_cal))
            if mouse[0] >= 600 and mouse[0] <= 775 and mouse[1] >= 113 + ratio_cal and mouse[1] <= 183 + ratio_cal:
                press = pygame.mouse.get_pressed()
                if press[0] == 1:
                    if button_text == "Buy Now":
                        buy_bar(name,bar_name)
                        number_of_bars_bought.append(1)
                        shop(previous_page[-1])
                    if button_text == "Select":
                        update_user_bar(name,bar_name)
                        shop(previous_page[-1])
            i += 1
        message_to_screen("Page: " + str(page),white,(307,56),20)
        message_to_screen("You bought " + str(len(number_of_bars_bought)) + " bars today",white,(307,86),20)
        message_to_screen("cash: $" + str(user_coins),white,(607,26),20)
    
        
        pygame.display.update()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        clock.tick(60)



#Functionality to avoid ball coming from the same position twice
def no_repeats(last_pos, new_pos):
    last_pos_li = last_pos
    if last_pos_li[-1] == new_pos:
        return True
    else:
        return False
#no repeat functionality ends here
#Checking user position
class CheckUser:
    def __init__(self,name):
        self.name = name
        self.scores_top = []
        for score in scores:
            name_user = score.split(",")
            self.scores_top.append(name_user[0])
        self.user_position = [self.scores_top[0],self.scores_top[1],self.scores_top[2]]
    def get_user_health(self):
        if self.name == self.user_position[0]:
            return 250
        if self.name == self.user_position[1]:
            return 200
        if self.name == self.user_position[2]:
            return 175
    def get_bar_path(self):
        if self.name == self.user_position[0]:
            return "images/new_bars/gold.png"
        if self.name == self.user_position[1]:
            return "images/new_bars/silver.png"
        if self.name == self.user_position[2]:
            return "images/new_bars/bronze.png"
    def get_bar_speed(self):
        if self.name == self.user_position[0]:
            return 8
        if self.name == self.user_position[1]:
            return 7.5
        if self.name == self.user_position[2]:
            return 7

def set_health():
    check_user = CheckUser(name)
    user_health = check_user.get_user_health()
    gameLoop(user_health)


#Main game loop starts here
def gameLoop(health = 150,point = 0,bar_x = 300,ball_y = 50,ball_x = random.choice(random_ball_pos),timer=0,ball_speed = 3.8,wait_time = True,wait_pause = 0):
    global points
    global name

    #Getting bar according to rank, selected bars will override
    check_user = CheckUser(name)
    bar_path = check_user.get_bar_path()
    bar_user_speed = check_user.get_bar_speed()
    #Ends here

    #Getting user bars and speed
    get_user_selected = int(get_user_selected_bar(name))
    user_bar_details = get_each_bar_detail(get_user_selected)
    if get_user_selected >= 1:
        if len(user_bar_details) >= 1:
            bar_path = user_bar_details[1]
            bar_user_speed = 6 + int(user_bar_details[2])
            health = 75 * int(user_bar_details[3])
    #Bar settings ends here

    #If user dont own any bar or is not on top 3 on leaderboard
    #This will give user a default bar
    if get_user_selected == 0:
        if bar_path == None:
            bar_path = "images/bar.png"
        if bar_user_speed == None:
            bar_user_speed = 6
        if health == None:
            health = 150
    #Default bar settings ends here

    wait_time = wait_time
    points = point
    bary = 530
    barx = bar_x
    bar_width = 10
    bar_height = 300
    ball_speed = ball_speed
    bar_speed = bar_user_speed
    ballx = ball_x
    bally = ball_y
    ball1 = Ball_falling(ballx, bally)
    bar = Dodge_bar(barx, bary, bar_height, bar_width,bar_path)
    game_loop = True
    pressed_right = False
    pressed_left = False
    time = timer
    screenoff = 0
    health_width = health
    health_height = 15
    health_num = health
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
    pause = False
    last_bar_pos = []
    previous_ball_pos_x = []
    last_ball_pos_y = []
    previous_time = []
    previous_ball_speed = []
    wait_pause = wait_pause
    while game_loop:
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
                if event.key == pygame.K_SPACE:
                    previous_ball_pos_x.append(ball1.x)
                    last_ball_pos_y.append(ball1.y)
                    previous_time.append(time)
                    previous_ball_speed.append(ball_speed)
                    pause = True
                    game_loop = False


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
                        print ("")

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
            bar.x -= bar_speed

        if bar.x <= 0:
            bar.x += bar_speed


        last_bar_pos.append(bar.x)


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


    #Pause functionality starts here
    time_paused = 0
    time_paused_allowed = 20
    while pause:
        time_paused += timecal
        new_time_paused = round(time_paused)
        count_down = round(time_paused_allowed - time_paused)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                offline_update(name)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    pause = False
                    game_loop = True
                    gameLoop(health_num,points,last_bar_pos[-1],last_ball_pos_y[-1],previous_ball_pos_x[-1],previous_time[-1],previous_ball_speed[-1],False,3)
        if  count_down <= 0:
            pause = False
            game_loop = True
            gameLoop(health_num,points,last_bar_pos[-1],last_ball_pos_y[-1],previous_ball_pos_x[-1],previous_time[-1],previous_ball_speed[-1],False,3)

        gameDisplay.blit(bg, (0, 0))
        message_to_screen("Game Paused", red, [270, 409], 35)
        message_to_screen("Game will continue in "+str(round(time_paused_allowed - time_paused)), red, [210, 460], 30)
        message_to_screen("OR PRESS SPACE TO CONTINUE", red, [210, 500], 30)

        message_to_screen(str(points), red, [740, 565], 25)
        message_to_screen("Health ", red, [50, 569], 25)
        ball1.render()
        bar.render()
        health.render()
        pygame.display.update()
        clock.tick(50)

    #Pause functionality ends here
def run_game():
    enter_Name()

#Starting the game by calling the first function that runs the game
run_game()
