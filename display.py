import pygame
from pygame.locals import *
from pygame import Color
import random
import numpy as np
from tkinter import *
from tkinter import messagebox
from collections import defaultdict
#from agglomerative_clustering import agglo_clustering
import math
import time
from config import *




def display(color,point = (-1,-1)):

    '''This functions displays a single point on our screen'''

    global speed
    color_options = [(255,102,102),(0,204,0),(102,102,255),(255,153,255),(229,204,255),(0,102,102)]

    if(point[0] == -1 and point[1] == -1):

        for i,cluster in enumerate(data_points):
            col = (0,0,0)
            for x,y in cluster:
                if(x >=0 and x<=1440 and y >= 0 and y <= 900):
                    pygame.draw.circle(background,col,(x,y),3)
    else:
        pygame.draw.circle(background,color,point,3)

    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.delay(speed)



def clear_screen():

    '''This function clears our game screen'''
    background.fill((250, 250, 250))


def draw_line(pos,axis):

    global recent_medians

    max_x = screen.get_size()[0]
    max_y = screen.get_size()[1]

    if(axis == 0):
        recent_y = max_y
        #if(recent_medians['y'] != []):
        #    recent_y = min(recent_medians['y'],key=lambda x:x[1])
        start = (pos[0],0)
        end = (pos[0],recent_y)
    else:
        recent_x = max_x
        #if(recent_medians['x'] != []):
        #    recent_x = recent_medians['x'][-1][0]
        start = (0,pos[1])
        end = (recent_x,pos[1])

    pygame.draw.line(background,(0,0,0),start,end)


    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.delay(speed)

    return


def draw_rect(medians,color_options={}):

    '''This function draws the medians on the screen as squares'''

    global speed
    #color_options = [(255,102,102),(0,204,0),(102,102,255),(255,153,255),(229,204,255),(0,102,102)]
    if(color_options != {}):
        for i,point in enumerate(medians):
            rect = pygame.Rect(point[0],point[1],12,12)
            pygame.draw.rect(background,color_options[i+1],rect)
    else:
        for point in medians:
            rect = pygame.Rect(point[0],point[1],12,12)
            pygame.draw.rect(background,(255,255,255),rect)






    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.delay(speed)

    return

def refresh(color,medians):
    for i,cluster in enumerate(data_points):
        for x,y in cluster:
            if(x >=0 and x<=1440 and y >= 0 and y <= 900):
                pygame.draw.circle(background,color,(x,y),3)

    for i,point in enumerate(medians):
        print('median',(x,y))

        rect = pygame.Rect(point[0],point[1],12,12)
        pygame.draw.rect(background,(255,255,255),rect)

    screen.blit(background, (0, 0))
    pygame.display.flip()


    return
