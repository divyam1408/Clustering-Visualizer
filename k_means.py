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
from display import *



def porportional_sampling(dict,total_distance):

    '''this function porportionaly sample a data point , with prob
    of point being selected porportional to the distance as given by the input dict'''

    #print(dict)
    #print(total_distance)

    #normalizing and calculating cummulative prob of my data
    start = 0
    for key in dict.keys():
        dict[key] /= total_distance


    for key in dict.keys():
        start = start + dict[key]
        dict[key] = start

    #print('cumm final',start)

    #getting a random number between 0 and 1
    number = random.uniform(0,1)
    #print(dict)
    for key in dict.keys():
        if(number < dict[key]):
            return key



def k_means(k,probabilistic_initialize):

    '''This functions implements the k means algorithm for clustering of data'''

    global data_points
    #print('data points ',data_points)
    color_options = [(255,102,102),(0,204,0),(102,102,255),(255,153,255),(229,204,255),(0,102,102)]
    data_dict = defaultdict(int) #point:cluster_number
    med_number = 1
    k_medians = []

    color_options={}
    for i in range(k):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        color_options[i+1] = (r,g,b)

    combined_data = []
    for cluster in data_points:
        combined_data += cluster

    #print('combined_data ',combined_data)
    '''choosing k medians randomly'''
    if(probabilistic_initialize == False):
        k_medians = random.sample(combined_data,k)
    else:
        '''Probalisticlly choosing medians'''

        k_medians.append(random.sample(combined_data,1)[0])
        while(med_number != k):
            ev = pygame.event.pump()

            #display(color_options[med_number],medians[med_number-1])
            nearest_med_distance = {}
            total_distance = 0
            for point in combined_data:
                if(point not in k_medians):
                    x1 = np.array(point)
                    min_dist = 999999999
                    for i,median in enumerate(k_medians):
                        x2 = np.array(k_medians)
                        dist = (np.linalg.norm(x1-x2))**2

                        if(dist < min_dist):
                            min_dist = dist
                            #belonging_cluster = i+1

                    nearest_med_distance[point] = min_dist
                    total_distance += min_dist
                    #print(total_distance)

            #doing porportional sampling
            sample = porportional_sampling(nearest_med_distance,total_distance)
            k_medians.append(sample)
            med_number += 1

        #display(color_options[med_number],medians[med_number-1])
        #draw_rect(k_medians,color_options)

        #running knn similar loop again


    print('k_medians',k_medians)

    '''Loop for checking convergence of medians once they are initialized'''
    while(True):
        ev = pygame.event.pump()


        draw_rect(k_medians,color_options)
        print('Centroids: ',k_medians)
        cluster_dis = defaultdict(int)#cluster:number_of_points
        '''clustering data based on nearest median'''
        random.shuffle(combined_data)

        for point in combined_data:
            x1 = np.array(point)
            min_dist = 999999999
            belonging_cluster = -1
            for i,median in enumerate(k_medians):
                x2 = np.array(median)
                dist = (np.linalg.norm(x1-x2))**2

                if(dist < min_dist):
                    min_dist = dist
                    belonging_cluster = i+1

            data_dict[point] = belonging_cluster
            cluster_dis[belonging_cluster] += 1
            display(color_options[belonging_cluster],point)
            #screen.blit(background, (0, 0))
            #pygame.display.flip()
            #time.sleep(0.1)


        '''initializing our dictionary'''
        cluster_sums = {}
        for i,k in enumerate(k_medians):
            cluster_sums[i+1] = [0,0]


        '''Updating the medians'''
        for point in combined_data:
            belonging_cluster = data_dict[point]
            cluster_sums[belonging_cluster][0] += point[0]
            cluster_sums[belonging_cluster][1] += point[1]

        for key in cluster_sums.keys():
            cluster_sums[key][0] /= cluster_dis[key]
            cluster_sums[key][1] /= cluster_dis[key]


        total = 0
        for i,median in enumerate(k_medians):
            med1 = np.array(median)
            med2 = np.array(cluster_sums[i+1])

            if(math.isclose(med1[0],med2[0],rel_tol=1e-02) == True and math.isclose(med1[1],med2[1],rel_tol=1e-02) == True):
                total += 1


        if(total == len(k_medians)):
            print('********CLUSTERING COMPLETED************')
            break
        else:
            refresh((0,0,0),k_medians)
            for i in range(len(k_medians)):
                k_medians[i] = tuple(cluster_sums[i+1])

    return k_medians
