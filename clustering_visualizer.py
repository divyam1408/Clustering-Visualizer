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
import config



'''initializing our screen display'''
screen = config.screen #pygame.display.set_mode()
#pygame.display.set_caption('Clustering Visulaizer')

# Fill background
background = config.background #pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))
data_points = config.data_points#[]
fpsClock = config.fpsClock#pygame.time.Clock()
speed = config.speed#6
in_clusters = config.in_clusters#-1
per_outliers = config.per_outliers#1
dataset = data_points
number_points_per_cluster = config.number_data_points
similarity_matrix_min = config.similarity_matrix_min
similarity_matrix_max = config.similarity_matrix_max
similarity_matrix_ward = config.similarity_matrix_ward
linkage = config.linkage



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

def display(color,point = (-1,-1)):

    '''This functions displays a single point on our screen'''

    global speed
    color_options = [(255,102,102),(0,204,0),(102,102,255),(255,153,255),(229,204,255),(0,102,102)]
    # if(color == (0,0,0)):
    #     print('black')
    #     for i,cluster in enumerate(data_points):
    #         for x,y in cluster:
    #             if(x >=0 and x<=1440 and y >= 0 and y <= 900):
    #                 pygame.draw.circle(background,color,(x,y),3)
    #
    #     for x,y in medians:
    #         print('median')
    #         if(x >=0 and x<=1440 and y >= 0 and y <= 900):
    #             pygame.draw.circle(background,(255,255,255),(x,y),3)

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
    #pygame.time.delay(speed)

    return

def clear_screen():

    '''This function clears our game screen'''
    background.fill((250, 250, 250))

    return

def error():
    pygame.init()
    screen = pygame.display.set_mode((150,90))
    pygame.display.set_caption('Error')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

def draw_rect(medians,color_options):

    '''This function draws the medians on the screen as squares'''

    global speed
    #color_options = [(255,102,102),(0,204,0),(102,102,255),(255,153,255),(229,204,255),(0,102,102)]
    for i,point in enumerate(medians):
        rect = pygame.Rect(point[0],point[1],12,12)
        pygame.draw.rect(background,color_options[i+1],rect)


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



def porportional_sampling(dict,total_distance):

    '''this function porportionaly sample a data point , with prob
    of point being selected porportional to the distance as given by the input dict'''

    #normalizing and calculating cummulative prob of my data
    start = 0
    for key in dict.keys():
        dict[key] /= total_distance
        start += dict[key]
        dict[key] = start

    print('cumm final',start)

    #getting a random number between 0 and 1
    number = random.uniform(0,1)

    for key in dict.keys():
        if(number < dict[key]):
            return key



def k_means(k,probabilistic_initialize):

    '''This functions implements the k means algorithm for clustering of data'''

    global data_points
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

            #doing porportional sampling
            sample = porportional_sampling(nearest_med_distance,total_distance)
            k_medians.append(sample)
            med_number += 1

        #display(color_options[med_number],medians[med_number-1])
        #draw_rect(k_medians,color_options)

        #running knn similar loop again


    print(k_medians)

    '''Loop for checking convergence of medians once they are initialized'''
    while(True):
        ev = pygame.event.pump()


        draw_rect(k_medians,color_options)
        print(k_medians)
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





def k_means_plus_plus(k):

    '''This function implemets k mean ++ algorithm'''

    global data_points
    medians=[]

    #combining my all datapoints into 1 list
    combined_data = []

    for cluster in data_points:
        combined_data += cluster

    color_options={}
    for i in range(k):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        color_options[i+1] = (r,g,b)

    #picking the 1st median randomly from data set
    medians.append(random.sample(combined_data,1)[0])
    med_number = 1
     # point:distance to nearest median

    while(med_number != k):
        ev = pygame.event.pump()
        print(medians)
        #display(color_options[med_number],medians[med_number-1])
        nearest_med_distance = {}
        total_distance = 0
        for point in combined_data:
            if(point not in medians):
                x1 = np.array(point)
                min_dist = 999999999
                belonging_cluster = -1
                for i,median in enumerate(medians):
                    x2 = np.array(median)
                    dist = (np.linalg.norm(x1-x2))**2

                    if(dist < min_dist):
                        min_dist = dist
                        #belonging_cluster = i+1

                nearest_med_distance[point] = min_dist
                total_distance += min_dist

        #doing porportional sampling
        sample = porportional_sampling(nearest_med_distance,total_distance)
        medians.append(sample)
        med_number += 1

    #display(color_options[med_number],medians[med_number-1])
    draw_rect(medians,color_options)

    #running knn similar loop again




def find_similarity(cluster1,cluster2,linkage):

    '''This function computes the similarity value between two clusters based on the MIN,MAX,WARD
    provided by linkage'''

    min = 999999999
    max = -1
    sum=0
    total=0
    cl1_union_cl2 = cluster1.union(cluster2)
    tup = tuple(cl1_union_cl2)
    if(linkage == 'MIN'):

        #print(type(tuple((cluster1,cluster2))))

        if(similarity_matrix_min[tup] != 0.0):
            return similarity_matrix_min[tup]
        else:
            for pt1 in cluster1:
                x1 = np.array(pt1)

                for pt2 in cluster2:
                    x2 = np.array(pt2)
                    dist = (np.linalg.norm(x1-x2))
                    if(dist <= min):
                        min = dist

            similarity_matrix_min[tup] = min

            return min
    elif(linkage == 'MAX'):

        if(similarity_matrix_max[tup] != 0.0):
            return similarity_matrix_max[tup]
        else:
            for pt1 in cluster1:
                x1 = np.array(pt1)
                for pt2 in cluster2:

                    x2 = np.array(pt2)
                    dist = (np.linalg.norm(x1-x2))
                    if(dist > max):
                        max = dist

            similarity_matrix_max[tup] = max
            return max

    else:
        if(similarity_matrix_ward[tup] != 0.0):
            return similarity_matrix_ward[tup]
        else:
            for pt1 in cluster1:
                x1 = np.array(pt1)
                for pt2 in cluster2:

                    x2 = np.array(pt2)
                    dist = (np.linalg.norm(x1-x2))**2
                    sum += dist
                    total += 1

            similarity_matrix_ward[tup] = sum/total

            return sum/total








def agglo_clustering(n_clusters,compute_full_tree,linkage):

    '''This fucntion implements agglomerative clustering based on the given input parameters'''

    cluster_list = []#contains all the clusters , initialy it will have number of datapoints as clusters
    for cluster in dataset:
        for point in cluster:
            cluster_list.append(set([point]))

    color_codes = {}

    clusters = len(cluster_list)
    while(clusters > n_clusters):
        ev = pygame.event.pump()
        print('Number of clustres present: ',clusters)
        #print('*'*50)
        #print(cluster_list)
        #print(clusters)
        min_similarity = 999999999
        min_similarity_clusters = []

        for i,cluster1 in enumerate(cluster_list):
            for cluster2 in cluster_list[i+1:]:

                similarity = find_similarity(cluster1,cluster2,linkage)
                #print('similarity ',similarity)
                if(similarity <= min_similarity):

                    min_similarity = similarity
                    min_similarity_clusters = [cluster1,cluster2]
                    #print('min_similarity ',min_similarity)
                    #print(min_similarity_clusters)

        color = (0,0,0)
        #print(min_similarity_clusters)
        new_cluster = min_similarity_clusters[0].union(min_similarity_clusters[1])
        cl1 = tuple(min_similarity_clusters[0])
        cl2 = tuple(min_similarity_clusters[1])



        #code for updating the screen with appropriate colors
        dic_keys = color_codes.keys()
        if(cl1 not in dic_keys and cl2 not in dic_keys):
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            color = (r,g,b)
            color_codes[tuple(new_cluster)] = color
        elif(cl1 in dic_keys and cl2 in dic_keys):
            if(len(cl1) > len(cl2)):
                color = color_codes[cl1]
            else:
                color = color_codes[cl2]
            color_codes[tuple(new_cluster)] = color
            color_codes.pop(cl1)
            color_codes.pop(cl2)

        else:
            if(cl1 in dic_keys):
                color = color_codes[cl1]
                color_codes.pop(cl1)
            else:
                color = color_codes[cl2]
                color_codes.pop(cl2)

            color_codes[tuple(new_cluster)] = color

        #drawing the points on screen
        for point in new_cluster:
            #print(point)
            display(color_codes[tuple(new_cluster)],point)


        #print(min_similarity_clusters)
        cluster_list.remove(min_similarity_clusters[0])
        cluster_list.remove(min_similarity_clusters[1])
        cluster_list.append(new_cluster)
        #print(new_cluster)
        #print(color_codes)


        clusters = (clusters-2)+1
    print('*************CLUSTERING FINISHED******************')












def main():
    '''This function initializes our display screen and returns it'''


    global data_points
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
    max_clusters = 1000
    clusters=0
    k_centers=[]
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                clusters += 1
                if(clusters <= max_clusters):
                    pos = pygame.mouse.get_pos()
                    k_centers.append(pos)
                    pygame.draw.circle(background,Color(0,0,0),pos,3)
                #cluster limit reached
                else:
                    print('Cluster Limit reached')


            if event.type == pygame.KEYDOWN:

                if(event.key == pygame.K_t):
                    draw_rect((45,45),(204,0,102))
                #creating custom dataset
                if(event.key == pygame.K_c):

                    if(data_points == []):
                        for x,y in k_centers:
                            kx_points = np.random.normal(x,10,number_points_per_cluster)
                            ky_points = np.random.normal(y,10,number_points_per_cluster)
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
                    if(data_points == []):
                        for x,y in k_centers:
                            if(flag%2 == 0):
                                kx_points = np.random.normal(x,15,small_sample)
                                ky_points = np.random.normal(y,15,small_sample)
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
                    clear_screen()

                if(event.key == pygame.K_RETURN):
                    if(clusters != 0):
                        print(clusters)
                        if(in_clusters < 0):
                            k_means(clusters,False)
                        else:
                            k_means(in_clusters,False)
                    else:
                        print('Please select some clusters!!!')

                if(event.key == pygame.K_k):
                    if(clusters != 0):
                        print(clusters)
                        if(in_clusters < 0):
                            k_means(clusters,True)
                        else:
                            k_means(in_clusters,True)
                    else:
                        print('Please select some clusters!!!')


                if(event.key == pygame.K_a):
                    if(clusters != 0):
                        print(clusters)
                        if(in_clusters < 0):
                            agglo_clustering(clusters,True,linkage)
                        else:
                            agglo_clustering(in_clusters,True,linkage)
                    else:
                        print('Please select some clusters!!!')





        screen.blit(background, (0, 0))
        pygame.display.flip()





if __name__ == '__main__': main()
