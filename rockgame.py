import pygame
import random
import serial
import time
import random
from rock import *

pygame.init()
display_width=800
display_height=600

#color definitions
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)

#game character
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Rocky Start - Copyright 2018, The College of Saint Rose')
clock=pygame.time.Clock()

rocklist=[]     # Create an empty list to hold our rocks
numRocks = 7    # Specify the number of rocks to create
rockImage = 'rock2.png'
imageWidth = 125
imageHeight = 125
playerImg=pygame.image.load('you-rock2.png')
playerImg_width = 125
playerImg_height = 100

use_port = False

def serialRead(ser):
    line=ser.readline().decode('ascii')
    xy = line.strip().split(',')
    return xy

def speedDelta(ser):
    delta = 0
    accel = serialRead(ser)
    print(accel)

    if len(accel) == 2:
        if len(accel[0]) > 0 and float(accel[0]) < -0.25:
            delta = -1
        elif len(accel[0]) > 0 and float(accel[0]) > 0.25:
            delta = 1

    return delta

# Create our rocks using the the specified image
# Initially, our position (x,y) will be set to (0,0) and speed will be 0.
def init_rocks():
    for i in range(0, numRocks):
        rock = Rock(0, 0, 0, pygame.image.load(rockImage))
        rocklist.append(rock)

# a function to place the car in our surface
def show_rock(rock):
    gameDisplay.blit(rock.getImage(),(rock.getXpos(),rock.getYpos()))  #blit is displaying image xy is a tuple

# a function to place the player ioon in our surface
def player(x,y):
    gameDisplay.blit(playerImg,(x,y))  #blit is displaying image xy is a tuple

def score(s):
    scoretext = myfont.render("Score: {0}".format(s), 1, (0, 0, 0))
    gameDisplay.blit(scoretext, (5, 5))

def gameover():
    gameovertext = gofont.render("GAME OVER", 1, (0,0,0))
    gameDisplay.blit(gameovertext, (display_width/2 - 150,display_height/2))

# check if there was a collision between 2 items
def check_collision(r1, r2, width, height):
    x1 = r1.getXpos()
    y1 = r1.getYpos()
    x2 = r2.getXpos()
    y2 = r2.getYpos()
    if abs(x2-x1) < width-20 and abs(y2-y1) < height-50:
        return True
    else:
        return False

def player_collide(x1,y1,x2, y2):
    if abs(x2-x1) < 50 and abs(y2-y1) < 50:
        return True
    else:
        return False

def game_loop():
    game_score = 0
    delta_speed = 0
    delta = 0
    player_x = (display_width*0.5) - (0.5*playerImg_width)
    player_y = (display_height-playerImg_height)
    gameExit=False
    ser = None
    key_x = 0

    #Update each rock in the rocklist
    for rock in rocklist:
        rock.setXpos(random.randrange(0, display_width-imageWidth))  # subtract the width of the image
        rock.setYpos(-125)
        rock.setSpeed(random.randrange(1,7))

    # open port to read accelerometer data from Arduino
    if use_port:
        ser = serial.Serial('COM3', 9600, timeout=1)  # Arduino serial communication

    while not gameExit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            key_x = 0
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_x = -0.20
                if event.key == pygame.K_RIGHT:
                    key_x = 0.20
                if event.key == pygame.K_DOWN:
                    delta_speed = 0

        if use_port:
            delta = speedDelta(ser)
        else:
            delta = key_x

        delta_speed += delta  # accumulate increases/decreases from iteration to iteration
        player_x += delta_speed  # change x by current delta
        if player_x < -25:
            player_x = -25
            delta_speed = 0
        if player_x > display_width-100:
            player_x = display_width-100
            delta_speed = 0

        gameDisplay.fill(white)
        j=0
        for rock in rocklist:
            #changing the y coordinate to make rocks move
            rock.setYpos(rock.getYpos() + rock.getSpeed())
            show_rock(rock)
            # Reset rock to top of screen if it fell below bottom

            if rock.getYpos() > display_height:
                rock.setYpos(-125)
                rock.setXpos(random.randrange(0, display_width-imageWidth))  # subtract the width of the image
                rock.setSpeed(random.randrange(1,7))
            j+=1
            for i in range(j,numRocks):
                if check_collision(rock,rocklist[i],imageWidth, imageHeight)and(not (rock.getYpos==-125)):
                    rock.setYpos(-125)
                    rock.setXpos(random.randrange(0, display_width-imageWidth))  # subtract the width of the image
                    rock.setSpeed(random.randrange(1,7))

        for rock in rocklist:
            if player_collide(rock.getXpos(),rock.getYpos(),player_x,player_y):
                gameExit = True

        player(player_x,player_y)
        #gameDisplay.blit(disclaimertext, (5, 5))
        game_score+=10
        score(game_score)
        pygame.display.update()
        clock.tick(50)

      #how many frames per second is updated

    gameDisplay.fill(white)
    player(player_x, player_y)
    # gameDisplay.blit(disclaimertext, (5, 5))
    game_score += 10
    score(game_score)
    gameover()
    pygame.display.update()
    time.sleep(5)

if __name__ == "__main__":
    #gameDisplay.fill(white)
    myfont = pygame.font.SysFont('arial', 18)
    gofont = pygame.font.SysFont('arial', 40)
    disclaimertext = myfont.render("Copyright 2018, The College of Saint Rose", 1, (0,0,0))


    init_rocks()
    game_loop()
    # to quit you need to stop pygame
    pygame.quit()
    quit()  #this will quit if not in IDLE when you run
