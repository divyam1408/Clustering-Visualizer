import pygame
from pygame.locals import *
from pygame import Color
import random
import numpy as np
from tkinter import *
from tkinter import messagebox
from collections import defaultdict
from collections import deque
#from agglomerative_clustering import agglo_clustering
import math
import time
from config import *
from display import *



#point_list = [(7, 2), (5, 4), (9, 6), (4, 7), (8, 1), (2, 3)]
#combined_data = point_list

#A binary tree node
class Node:

    def __init__(self,data):
        self.median = data
        self.left = None
        self.right = None


core_dic = defaultdict(int)
test_dic = {}
count = 0
points_representation = {}
queue = deque()
inqueue = defaultdict(int)

# def build_kdtree(query_point,data,depth):
#
#     '''This function builds a kd tree along the given data points and stops when the leaf has
#     minimum number of nodes as defined by varaible nodes_in_leaf. It returns the head of the tree.'''
#
#     global recent_medians
#
#     nodes = len(data)
#     if(nodes <= nodes_in_leaf):
#         is_core = core_point(query_point,data)
#         return None
#
#
#
#     axis = depth%2
#
#     #sort the data along the given axis 0:x ,1:y
#     data.sort(key=lambda x:x[axis])
#     med = (nodes)//2
#
#     if(query_point == data[med]):
#         is_core = core_point(query_point,data)
#         return None
#
#     draw_line(data[med],axis)
#
#     if(axis == 0):
#         recent_medians['x'].append(data[med])
#     else:
#         recent_medians['y'].append(data[med])
#
#     node = Node(data[med])
#     node.left = build_kdtree(data[:med],depth+1)
#     if(is_core == False):
#         if(axis == 0):
#             dist = abs(data[med][0]-query_point[0])
#         else:
#             dist =  abs(data[med][1]-query_point[1])
#         if(dist < eps):
#
#     node.right = build_kdtree(data[med:],depth+1)
#     if(is_core == False):
#         if(axis == 0):
#             dist = abs(data[med][0]-query_point[0])
#         else:
#             dist =  abs(data[med][1]-query_point[1])
#         if(dist < eps):
#
#
#
#
#
#
#     return  node

def reinitialize():
    global core_dic
    global count
    global points_representation
    global queue,inqueue
    global is_core

    core_dic.clear()
    count = 0
    points_representation.clear()
    queue.clear()
    inqueue.clear()
    is_core = False



def core_point(query_point,data,to_find):
    global min_samples
    global eps
    global core_dic
    global count
    global points_representation
    global queue,inqueue

    if(to_find == 'core'):
        pt1 = np.array(query_point)
        for point in data:
            if(core_dic[point] == 0):
                pt2 = np.array(point)
                dist = np.linalg.norm(pt1-pt2)
                if(dist < eps):
                    count += 1
                core_dic[point] = 1


        #print('count:',count)
        if(count >= min_samples):
            return True
        else:
            return False

    elif(to_find == 'border'):
        for point in data:
            #print(point)
            if(point in points_representation.keys()):
                if(points_representation[point] == 'Core'):
                    #print('true',point)
                    return True
        return False
    else:
        pt1 = np.array(query_point)
        for point in data:

            pt2 = np.array(point)
            dist = np.linalg.norm(pt1-pt2)
            if(dist < eps):
                if(points_representation[point] =='Core'):
                    if(inqueue[point] == 0):
                        queue.append(point)
                        inqueue[point] = 1
        return False



def build_kdtree(query_point,data,depth,to_find):

    global is_core
    global core_dic
    global eps

    nodes = len(data)
    if(nodes <= nodes_in_leaf):
        #print('1')
        if(to_find == 'cluster'):
            core_point(query_point,data,to_find)
        else:
            #print('1\n',data)
            is_core = core_point(query_point,data,to_find)
        return None

    axis = depth%2

    #sort the data along the given axis 0:x ,1:y
    data.sort(key=lambda x:x[axis])
    med = (nodes)//2

    if(query_point == data[med]):
        #print('2')
        if(to_find == 'cluster'):
            core_point(query_point,data,to_find)
        else:
            #print('2\n',data)
            is_core = core_point(query_point,data,to_find)
        return None

    if(axis == 0):
        if(query_point[0] < data[med][0]):
            #print('3')
            build_kdtree(query_point,data[:med],depth+1,to_find)
        else:
            #print('4')
            build_kdtree(query_point,data[med+1:],depth+1,to_find)
    else:
        if(query_point[1] < data[med][1]):
            #print('5')
            build_kdtree(query_point,data[:med],depth+1,to_find)
        else:
            #print('6')
            build_kdtree(query_point,data[med+1:],depth+1,to_find)

    if(is_core == False):
        dist = 0
        if(axis == 0):
            dist = abs(data[med][0]-query_point[0])
        else:
            dist =  abs(data[med][1]-query_point[1])
        if(dist < eps):
            #print('7')
            if(to_find == 'clustering'):
                core_point(query_point,data,to_find)
            else:
                #print('3\n',data)
                is_core = core_point(query_point,data,to_find)

    return None








def dbscan():
    print('Breaking data points into Core , Represented by green color')
    global data_points
    global is_core
    global core_dic
    global count
    global queue,inqueue

    reinitialize()
    combined_data = []
    clusters = []
    for cluster in data_points:
        combined_data += cluster
    #print(len(combined_data))

    for point in combined_data:
        count = 0
        core_dic = defaultdict(int)
        tree = build_kdtree(point,combined_data,0,'core')
        if(is_core):
            points_representation[point] = 'Core'
            display((0,255,0),point)
        is_core = False

    print('Breaking Points into Boundary and Noise Points,Rpresenyed by blue and Red points.')
    is_core = False
    #print('combined data ',combined_data)
    for point in combined_data:
        #print(point)
        if(point not in points_representation.keys()):
            build_kdtree(point,combined_data,0,'border')
            if(is_core):
                points_representation[point] = 'Border'
                display((0,0,255),point)
            else:
                #print('noise')
                points_representation[point] = 'Noise'
                display((255,0,0),point)

        is_core = False

    print('Clustering the Data set')
    is_core = False
    for point in combined_data:
        is_core = False
        if(points_representation[point] == 'Core'):
            #print(point)
            cluster = {point}
            queue.append(point)
            inqueue[point] = 1
            color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            while(queue != deque([])):

                pt = queue.popleft()
                display(color,pt)
                build_kdtree(pt,combined_data,0,'cluster')
                points_representation[pt] = 'Clustered'
                cluster.add(pt)
            clusters.append(cluster)
            queue.clear()

        if(points_representation[point] == 'Noise'):
            display((255,255,255),point)

    print('***********Clustering Completed*****************')
