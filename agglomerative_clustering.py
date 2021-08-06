import numpy as np
import random
from config import *
import pygame
from pygame.locals import *
from display import *



dataset = data_points

def re_initialize():
    global similarity_matrix_min
    global similarity_matrix_max
    global similarity_matrix_ward

    similarity_matrix_min.clear()
    similarity_matrix_max.clear()
    similarity_matrix_ward.clear()



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

    re_initialize()

    cluster_list = []#contains all the clusters , initialy it will have number of datapoints as clusters
    for cluster in dataset:
        for point in cluster:
            cluster_list.append(set([point]))

    color_codes = {}

    clusters = len(cluster_list)
    while(clusters > n_clusters):
        ev = pygame.event.pump()
        print('Number of clustres present(linkage {}): {}'.format(linkage,clusters))
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
