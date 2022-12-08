import pygame as pyg
import numpy as np 
import math, random ##

#custom stuff here

def t_particleBurst(x,y,particlelist):
    '''
    creates a burst of particles, basic implementation
    '''
    for i in range(10):
        vx = (random.random() - 0.5) * 15
        vy = (random.random() - 0.5) * 15
        t_createParticle(x,y,vx,vy,20,30,particlelist)

def t_createParticle(x,y,vx,vy,life,size,particlelist):
    '''
    x y pixel coords\n
    velocity is p/s\n
    life is in frames until death\n
    '''
    p = [x,y,vx,vy,life,size,life,size]
    ##  0  1 2  3  4    5    6    7 
    particlelist.append(p)

def t_updateParticles(screen,color,particlelist):
    for i, p in enumerate(particlelist):
        particlelist[i] = [p[0]+ p[2],p[1]+p[3],p[2],p[3],p[4] - 1,(p[4] / p[6]) * p[7],p[6],p[7]]
    for p in list(particlelist):
        if p[4] <= 0:
            particlelist.remove(p)
    
    for p in particlelist:
        pyg.draw.rect(screen,color,(p[0],p[1],p[5],p[5]))
#

def drop_meteors(met_list, met_dim, width): #liam
    rx = random.randint(0, width)
    newpos = [rx,0]
    if random.randint(0,5) == 2:
        met_list.append(newpos)
def set_speed(score):
    if score <= 0:
        speed = 1
    elif score < 5:
        speed = score*0.5
    elif score >= 5:
        speed = score*0.6
    else:
        speed = score*0.8
    return speed

def update_meteor_positions(met_list2, height, score, speed, a,pl):
    '''

    The parameters are the meteor list, with the nested list of positions, the height of the screen, the score, and the speed of the meteor.
    This function checks if the meteor is still in the range of the screen through referencing the height (since the meteor is only falling vertically.)
    For every meteor in met_position, we are checking if it is in the screen and if it is we are increasing it by the speed,
    and if it isn't then the score is increased by 1. Then we return the score since it is the only parameter adjusted. 
    '''

    if a:
        for m in met_list2:
            if m[1] > height:
                met_list2.remove(m)
                t_particleBurst(m[0],m[1]-30,pl)
                score += 1
            else:
                m[1] += speed * 5
                x = random.random() -0.5
                if random.randint(1,3) == 1:
                    t_createParticle(m[0],m[1],x*5,0,20,15,pl)
        return score
    

#add comment
def collision_check(met_list, player_pos, player_dim, met_dim): ##shane
    '''
    collision check: this function is non-void and has 4 parameter, the nested list of meteor positions, the list that is the position of the player,
    the size of the player, and the size of the meteor. This func calls the detect collision func for each meteor. as soon as a collision is
    found it returns true to main to end the game. The iterating for loop iterates over the list of meteors so that the y position is udated by the amount of pixels moved.
    If the loop returns true, then the game is over. Then if it is false and the game continues as the character has not died.
    '''
    for i in range(len(met_list)):
        met_pos = met_list[i]
        hit = detect_collision(met_pos, player_pos, player_dim, met_dim)
        if hit == True:
            return True

def draw_meteors(met_list, met_dim, screen, color):#eva
    '''
    This fucntion is void with 4 parameters. the nested list of met_list, the meteor dimenstion in met_dim, the screen dimensions, and the color
    of the meteors. This function is realtively simple, you just have to follow the pygame format for drawing a rectangle. 
    The for loop then has you draw a meteor for each meteror in the meteor list. Which makes sense since in order for the game to have meteors fall,
    you must have them drawn into the game. The function draw_meteors returns norhting since it is a void fucntion. 
    '''
    for met_position in met_list:
        pyg.draw.rect(screen, color,(met_position[0],met_position[1], met_dim, met_dim))

def detect_collision(met_pos, player_pos, player_dim, met_dim): #liam
    px = player_pos[0]
    py = player_pos[1]
    mx = met_pos[0]
    my = met_pos[1]
    mb = met_dim
    pb = player_dim
    if my + mb > py and my < py + pb:
        if px < mx + mb and px + pb > mx:
            return True
        else:
            return False
    else:
        return False

def main():
    '''
    Initialize pygame and pygame parameters.  Note that both player and meteors
    are square.  Thus, player_dim and met_dim are the height and width of the
    player and meteors, respectively.  Each line of code is commented.
    '''
    pyg.init()                # initialize pygame
    ####
    ####
    width = 800               # set width of game screen in pixels
    height = 600              # set height of game screen in pixels

    red = (250,250,210)           # rgb color of player
    yellow = (244,208,63)     # rgb color of meteors
    background =  (72,61,139)    # rgb color of sky (purple)
    white = (255,255,255)

    player_dim = 50           # player size in pixels
    player_pos = [width/2, height-2*player_dim]  # initial location of player
                                                 # at bottom middle; height
                                                 # never changes

    met_dim = 20              # meteor size in pixels
    met_list = []             # initialize list of two-element lists
                              # giving x and y meteor positions

    screen = pyg.display.set_mode((width, height)) # initialize game screen

    game_over = False         # initialize game_over; game played until
                              # game_over is True, i.e., when collision
                              # is detected

    score = 0                 # initialize score
    #custom
    t_utime = 0
    particlelist = []
    #

    clock = pyg.time.Clock()  # initialize clock to track time

    my_font = pyg.font.SysFont("monospace", 35) # initialize system font

    while not game_over:                       # play until game_over == True
        for event in pyg.event.get():          # loop through events in queue
            if event.type == pyg.KEYDOWN:      # checks for key press
                x = player_pos[0]              # assign current x position
                y = player_pos[1]              # assign current y position
                if event.key == pyg.K_LEFT:    # checks if left arrow;
                    x -= player_dim            # if true, moves player left
                elif event.key == pyg.K_RIGHT: # checks if right arrow;
                    x += player_dim            # else moves player right
                player_pos = [x, y]            # reset player position
            
        screen.fill(background)                # refresh screen bg color
        drop_meteors(met_list, met_dim, width) # read PA prompt
        speed = set_speed(score)               # read PA prompt
        score = update_meteor_positions(met_list, height, score, speed,True,particlelist)
                                               # read PA prompt
        text = "Score: " + str(score)              # create score text
        label = my_font.render(text, 1, yellow)    # render text into label
        screen.blit(label, (width-250, height-40)) # blit label to screen at
                                                   # given position; for our 
                                                   # purposes, just think of
                                                   # blit to mean draw
        draw_meteors(met_list, met_dim, screen, yellow) # self-explanatory;
                                                        # read PA prompt
        t_updateParticles(screen,white,particlelist)
        print(len(particlelist))
        pyg.draw.rect(screen, red, (player_pos[0], player_pos[1], player_dim, player_dim))                                        # draw player

        if collision_check(met_list, player_pos, player_dim, met_dim):
            game_over = True                       # read PA prompt
    
        clock.tick(30)                             # set frame rate to control
        t_utime += 1
        
                                                   # frames per second (~30); 
                                                   # slows down game

        pyg.display.update()                       # update screen characters
    # Outside while-loop now.
    print('Congrats player! Your final score is:', score)                   # final score
    pyg.quit()                                     # leave pygame

main()
