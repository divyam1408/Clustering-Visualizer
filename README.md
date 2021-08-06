# Clustering-Visualizer
Visulaize and see some of the  famous clustering algorithms when they run. Here i have implemented basic clustering algorithms like K means, Kmeans++, heirarichal clustering(aggllomerative clustering),DBSCAN in which we can see the algorithms creating clusters as and when they run. This really helped me understand the alogrithms better. We will build our own 2d data set on the pygame window on which we will run our algorithms.
In this file i will tell you how to run the code on your machine step by step.I have also attached snapshots of the results that i got while running it on my oen machine. Here the Data sets that we will see in the snapshots have been taken by the following slide https://cs.wmich.edu/alfuqaha/summer14/cs6530/lectures/ClusteringAnalysis.pdf

Getting our machine ready:


This is a native python project and uses python environment and libraries to run.

Following Python libraries are required to run the code on your machine:
pygame
numpy
python 3.x (prefered 3.7.7 or higher)

pygame is an python library used to buld 2d games, we can install it using pip or python3 command run any of the following command
pip intall pygame
python3 -m pip install -U pygame --user

Make sure pygame is installed successfully. Also if you run on python 3.7.7 or higher it will be better.I ran on python 3.8 and it worked well on my machine.


How to run the code?

Once pygame is installed you are ready to run the program.
Before running make sure to put all the files in a single folder.
Going in this folder run the following command:
python runner.py


If every thing goes well this should open an pygame window on your screen looking like this:
<img width="1417" alt="Screenshot 2021-08-06 at 11 17 56 PM" src="https://user-images.githubusercontent.com/17786795/128551570-ce617982-0622-48a8-b99c-9c67d3174ed8.png">


This is the screen where we will see our algorithms running.
But first we need to create a dataset on which we want to run our algorithms

How to create Dataset?

There is a config.py file which basically creates different parameter which change the behaviour of our code.
In this file there are 2 variables number_points_per_cluster and spread.
number_points_per_cluster as stated defines how many points we require to sample in our cluster
spread is basically the variance around mean or center which helps us to control the density of our cluster.

To create a data set basically we have to click on the pygame screen , the point where you clicked acts as a center or mean and depending on the variables values 
defined we sample number_points_per_cluster points around center with spread as defined by us.
the following screen shows various dense clusters as eg

number_points_per_cluster = 300 spread = 50
<img width="1440" alt="Screenshot 2021-08-06 at 11 38 22 PM" src="https://user-images.githubusercontent.com/17786795/128553748-462cfdf8-50db-4f42-a168-0f6e5c9821fa.png">
Here as we can see with 3 clicks in different regions of screen 3 clusters were created

number_points_per_cluster = 25, spread = 10
<img width="1440" alt="Screenshot 2021-08-06 at 11 36 41 PM" src="https://user-images.githubusercontent.com/17786795/128553885-6ec715cb-ae3c-4390-a307-ee74b5cc4179.png">
Here with differnt valus we can create differnt shape clusters also, just click on the screen in the shape u desire to create.



