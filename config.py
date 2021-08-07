import pygame
from pygame.locals import *
from pygame import Color
from collections import defaultdict




'''initializing our screen display'''
screen = pygame.display.set_mode()
pygame.display.set_caption('Clustering Visulaizer')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))
data_points = []
fpsClock = pygame.time.Clock()
speed = 6
in_clusters = 2
per_outliers = 1
number_points_per_cluster = 25
spread = 10
similarity_matrix_min = defaultdict(float)
similarity_matrix_max = defaultdict(float)
similarity_matrix_ward = defaultdict(float)
linkage = 'MIN' #options: MIN, MAX, WARD
nodes_in_leaf = 1
recent_medians = defaultdict(list)
is_core = False
eps = 9.92
min_samples = 4
eps_list = []
