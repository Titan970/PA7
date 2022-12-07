import pygame as pyg
import numpy as np 
import math, random

#custom stuff here
class Particle:
    def __init__(self,x,y,vx,vy,life,size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.size = size
        self.initialsize = size
        self.initiallife = life
    
    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.life -= 1

        self.size = (self.life / self.initiallife) * self.initialsize

def t_particleBurst(x,y,particlelist):
    for i in range(10):
        vx = (random.random() - 0.5) * 15
        vy = (random.random() - 0.5) * 15
        t_createParticle(x,y,vx,vy,20,30,particlelist)

def t_createParticle(x,y,vx,vy,life,size,particlelist):
    '''
    x y pixel coords
    velocity is p/s
    life is in frames until death
    '''
    p = Particle(x,y,vx,vy,life,size)
    particlelist.append(p)

def t_updateParticles(screen,color,particlelist):
    for p in particlelist:
        p.update()
    for p in list(particlelist):
        if p.life <= 0:
            particlelist.remove(p)
            del p
    
    for p in particlelist:
        pyg.draw.rect(screen,color,(p.x,p.y,p.size,p.size))
#

def drop_meteors(met_list, met_dim, width): #liam
    rx = random.randint(0, width)
    newpos = [rx,0]
    if random.randint(0,5) == 2:
        met_list.append(newpos)


def set_speed(s):
    if type(s) == type(4):
        return s * 1
    else:
        return 999

def update_meteor_positions(met_list2, height, score, speed, a,pl):
    '''

    The parameters are the meteor list, with the nested list of positions, the height of the screen, the score, and the speed of the meteor.
    This function checks if the meteor is still in the range of the screen through referencing the height (since the meteor is only falling vertically.)
    For every meteor in met_position, we are checking if it is in the screen and if it is we are increasing it by the speed,
    and if it isn't then the score is increased by 1. Then we return the score since it is the only parameter adjusted. 
    '''
   #check if meteor is still in screen
    # for met_position in met_list:
    #   if met_position in list(range(0, height)):
    #     #increase y, and increase the score every time the meteor goes beyond the bound.
    #     met_position[1] += speed
    if a:
        for m in met_list2:
            if m[1] > height:
                met_list2.remove(m)
                t_particleBurst(m[0],m[1]-30,pl)
                score += 1
            else:
                m[1] += 10
                x = random.random() -0.5
                if random.randint(1,3) == 1:
                    t_createParticle(m[0],m[1],x*5,0,20,15,pl)
        return score
    

#add comment
def collision_check(met_list, player_pos, player_dim, met_dim): ##shane
    for i in range(len(met_list)):
        met_pos = met_list[i]
        hit = detect_collision(met_pos, player_pos, player_dim, met_dim)
        if hit == True:
            return True

def draw_meteors(met_list, met_dim, screen, color):#eva
    '''
add docstring
    '''
    for met_position in met_list:
        pyg.draw.rect(screen, color,(met_position[0],met_position[1], met_dim, met_dim) )

def inBounds(a1,a2,b1,b2):
    if a1 < b2 and a2 > b1:
        return True
    else:
        return False
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
        t_updateParticles(screen,yellow,particlelist)
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
