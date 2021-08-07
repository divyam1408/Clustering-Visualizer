import pygame
from pygame.locals import *
from pygame import Color
import random
import numpy as np
from tkinter import *
from tkinter import messagebox
from collections import defaultdict
from agglomerative_clustering import agglo_clustering
from display import *
import math
import time
from config import *
from k_means import *
from dbscan import *




def create_dataset(screen,clusters=3):

    '''this function creates a clustering dataset to visulaize with maximum upto 6 clusters
    adn returns the data points'''

    screen_size = screen.get_size()

    '''asking user to  choose k points from our grid which acts as the mean of a region with radius
    as the variance '''


    x_samples = random.sample(range(0,screen_size[0]),clusters)
    y_samples = random.sample(range(0,screen_size[1]),clusters)
    k_centers = list(zip(x_samples,y_samples))

    radius = 100

    data_points = []
    for x,y in k_centers:
        kx_points = np.random.normal(x,50,500)
        ky_points = np.random.normal(y,50,500)
        k_points = list(zip(kx_points,ky_points))

        data_points.append(k_points)


    return data_points


def main():
    '''This function initializes our display screen and returns it'''


    global data_points
    global linkage
    global eps_list,eps
    pygame.init()

    # '''Showing default data configuration'''
    # data_points = create_dataset(screen,3)
    # for cluster in data_points:
    #     color = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
    #     for x,y in cluster:
    #         if(x >=0 and x<=1440 and y >= 0 and y <= 900):
    #             pygame.draw.circle(background,color,(x,y),3)

    #joblib.dump(data_points,'config1.pkl')

    # Blit everything to the screen
    # screen.blit(background, (0, 0))
    # pygame.display.flip()

    # Event loop
    max_clusters = 10000
    clusters=0
    k_centers=[]
    outliers = []
    k_medians = []
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                clusters += 1

                if(clusters <= max_clusters):
                    #pos = pygame.mouse.get_pos()
                    #k_centers.append(pos)
                    #display((0,0,0),pos)
                    ##pygame.draw.circle(background,Color(0,0,0),pos,3)
                    pos = pygame.mouse.get_pos()
                    display((0,0,0),pos)
                    x = pos[0]
                    y = pos[1]
                    kx_points = np.random.normal(x,spread,number_points_per_cluster)
                    ky_points = np.random.normal(y,spread,number_points_per_cluster)
                    k_points = list(zip(kx_points,ky_points))
                    k_points.append((x,y))
                    k_centers.append(pos)
                    data_points.append(k_points)

                    display((0,0,0))

                #cluster limit reached
                else:
                    print('Cluster Limit reached')


            if event.type == pygame.KEYDOWN:

                if(event.key == pygame.K_t):
                    draw_rect((45,45),(204,0,102))
                #creating custom dataset
                if(event.key == pygame.K_c):

                    if(k_centers != []):
                        for x,y in k_centers:
                            kx_points = np.random.normal(x,spread,number_points_per_cluster)
                            ky_points = np.random.normal(y,spread,number_points_per_cluster)
                            k_points = list(zip(kx_points,ky_points))
                            k_points.append((x,y))

                            data_points.append(k_points)

                        #show points on screen
                        display((0,0,0))
                    else:
                        print('Dataset already created , press escape to create new one')

                if(event.key == pygame.K_1):
                    #differing sizes clusters
                    flag=0
                    small_sample=50
                    large_sample = 500
                    background.fill((250, 250, 250))
                    data_points.clear()
                    if(data_points == []):
                        print('here')
                        for x,y in k_centers:
                            if(flag%2 == 0):
                                kx_points = np.random.normal(x,10,small_sample)
                                ky_points = np.random.normal(y,10,small_sample)
                                k_points = list(zip(kx_points,ky_points))
                                flag += 1
                            else:
                                kx_points = np.random.normal(x,50,large_sample)
                                ky_points = np.random.normal(y,50,large_sample)
                                k_points = list(zip(kx_points,ky_points))
                                flag += 1

                            data_points.append(k_points)
                        display((0,0,0))

                    else:
                        print('Dataset already created , press escape to create new one')


                if(event.key == pygame.K_2):
                    #different densities cluster
                    flag=0
                    dense = 10
                    sparse = 50
                    if(data_points == []):
                        for x,y in k_centers:
                            if(flag%2 == 0):
                                kx_points = np.random.normal(x,dense,500)
                                ky_points = np.random.normal(y,dense,500)
                                k_points = list(zip(kx_points,ky_points))
                                flag += 1
                            else:
                                kx_points = np.random.normal(x,sparse,500)
                                ky_points = np.random.normal(y,sparse,500)
                                k_points = list(zip(kx_points,ky_points))
                                flag += 1

                            data_points.append(k_points)
                        display((0,0,0))

                if(event.key == pygame.K_3):
                    #impact of outliers
                    if(data_points == []):
                        for i,point in enumerate(k_centers):
                            if(i < len(k_centers)-1):
                                kx_points = np.random.normal(point[0],50,500)
                                ky_points = np.random.normal(point[1],50,500)
                                k_points = list(zip(kx_points,ky_points))

                                data_points.append(k_points)
                        #create outliers
                        point = k_centers[-1]
                        number_of_outliers = (((len(k_centers)*500)*per_outliers)//100)
                        kx_points = np.random.normal(point[0],5,number_of_outliers)
                        ky_points = np.random.normal(point[1],5,number_of_outliers)
                        k_points = list(zip(kx_points,ky_points))

                        data_points.append(k_points)


                        #show points on screen
                        print(number_of_outliers)
                        display((0,0,0))
                        clusters = clusters-1
                    else:
                        print('Dataset already created , press escape to create new one')



                if(event.key == pygame.K_ESCAPE):
                    data_points.clear()
                    k_centers.clear()
                    clusters=0
                    outliers.clear()
                    clear_screen()

                if(event.key == pygame.K_o):
                    outliers = []
                    pos = pygame.mouse.get_pos()
                    if(pos not in outliers):
                        display((0,0,0),pos)
                        outliers.append(pos)
                    data_points.append(outliers)
                    #print(data_points)


                if(event.key == pygame.K_RETURN):
                    if(data_points != []):
                        #print(clusters)
                        if(in_clusters < 0):
                            if(cluster != 0):
                                k_medians = k_means(clusters,False)
                            else:
                                print('Running K MEans with default = 2 clusters. Change IN_CLUSTERS variable in config file')
                                k_medians = k_means(2,False)

                        else:
                            k_medians = k_means(in_clusters,False)
                    else:
                        print('Please select some clusters!!!')

                if(event.key == pygame.K_k):
                    if(data_points != []):
                        print(clusters)
                        if(in_clusters < 0):
                            if(clusters != 0):
                                k_medians = k_means(clusters,True)
                            else:
                                print('Running K MEans  with default = 2 clusters. Change IN_CLUSTERS variable in config file')
                                k_medians = k_means(2,True)
                        else:
                            k_medians = k_means(in_clusters,True)
                    else:
                        print('Please select some clusters!!!')


                if(event.key == pygame.K_l):
                    linkage = 'MIN'
                    print('Agglo Clustering with MIN linkage')
                    if(data_points != []):
                        print(clusters)
                        if(in_clusters < 0):
                            if(clusters != 0):
                                agglo_clustering(clusters,True,linkage)
                            else:
                                print('Running Agglomerative Clustering  with default = 2 clusters. Change IN_CLUSTERS variable in config file')
                                agglo_clustering(2,True,linkage)

                        else:
                            agglo_clustering(in_clusters,True,linkage)
                    else:
                        print('Please select some clusters!!!')

                if(event.key == pygame.K_g):
                    linkage = 'MAX'
                    print('Agglo Clustering with MAX linkage')
                    if(data_points != []):
                        print(clusters)
                        if(in_clusters < 0):
                            if(clusters != 0):
                                agglo_clustering(clusters,True,linkage)
                            else:
                                print('Running Agglomerative Clustering  with default = 2 clusters. Change IN_CLUSTERS variable in config file')
                                agglo_clustering(2,True,linkage)

                        else:
                            agglo_clustering(in_clusters,True,linkage)
                    else:
                        print('Please select some clusters!!!')

                if(event.key == pygame.K_w):
                    print('Agglo Clustering with WARD linkage')
                    linkage = 'WARD'
                    if(data_points != []):
                        print(clusters)
                        if(in_clusters < 0):
                            if(clusters != 0):
                                agglo_clustering(clusters,True,linkage)
                            else:
                                print('Running Agglomerative Clustering  with default = 2 clusters. Change IN_CLUSTERS variable in config file')
                                agglo_clustering(2,True,linkage)

                        else:
                            agglo_clustering(in_clusters,True,linkage)
                    else:
                        print('Please select some clusters!!!')

                if(event.key == pygame.K_d):
                    if(clusters != 0):
                        print(clusters)
                        if(eps_list == []):
                            dbscan()

                        else:
                            for eps_ in eps_list:
                                print('DBSCAN for eps = {}'.format(eps))
                                eps = eps_
                                dbscan()

                    else:
                        print('Please select some clusters!!!')

                if(event.key == pygame.K_r):
                    print(k_medians)
                    draw_rect(k_medians)
                    for median in k_medians:
                        print(median)

                    print(k_medians)
                    display((0,0,0))






        screen.blit(background, (0, 0))
        pygame.display.flip()





if __name__ == '__main__': main()
