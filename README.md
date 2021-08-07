# Clustering-Visualizer
Visulaize and see some of the  famous clustering algorithms when they run. Here i have implemented basic clustering algorithms like K means, Kmeans++, heirarichal clustering(aggllomerative clustering),DBSCAN in which we can see the algorithms creating clusters as and when they run. This really helped me understand the alogrithms better. We will build our own 2d data set on the pygame window on which we will run our algorithms.
In this file i will tell you how to run the code on your machine step by step.I have also attached snapshots of the results that i got while running it on my oen machine. Here the Data sets that we will see in the snapshots have been taken by the following slide https://cs.wmich.edu/alfuqaha/summer14/cs6530/lectures/ClusteringAnalysis.pdf

Getting our machine ready:


This is a native python project and uses python environment and libraries to run.

Following Python libraries are required to run the code on your machine:
pygame,
numpy,
python 3.x (prefered 3.7.7 or higher)

pygame is an python library used to buld 2d games, we can install it using pip or python3 command run any of the following command
<img width="667" alt="Screenshot 2021-08-07 at 12 20 59 AM" src="https://user-images.githubusercontent.com/17786795/128558352-af449c94-cd03-4b1d-b397-b48677781431.png">
or pip install pygame

Make sure pygame is installed successfully by seeing if it gets imported or not. Also if you run on python 3.7.7 or higher it will be better.I ran on python 3.8 and it worked well on my machine.


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
Here with differnt values we can create differnt shape clusters also, just click on the screen in the shape u desire to create.

with the same valraible values we can also create very dense clusters by repeteadlly clicking in and around a small region many times as shown below
![image](https://user-images.githubusercontent.com/17786795/128554705-c2cb7c1c-7c83-4054-b55f-bcf56a9248a0.png)

If we want to add single points one by one in our screen we can do that by just pressing key o from our keyboard.
just move your mouse cursor to the posiiton you want to create a single data point(NOTE: Do not click on the point) and then press o
This is a very good way if we want to create some sparser clusters and if we want outlier points in our data , as shown below:
![image](https://user-images.githubusercontent.com/17786795/128555651-1a49eb7c-47da-4cdc-99ab-3f0cbb4964ad.png)
Here by repeated pressing of key o we can create such clusters also.

At any point of time when algorithm is not running if you want to clear your screen just press ESC key. It will remove all the datapoints on the screen and screen will be blank again.

If you want to form different sizes clusters on the same screen , This can be done by first simple clicking on the screen as always to select the centers, ignore whatever clusters are created by doing this. Now remember that every odd numbered click that you clicked will create a smaller and denser cluster , Even numbered click will create a larger and sparser cluster. After doing this just press the 1 key on your keyboard. you should be able to see differnt sized clusters now.
As shown below
![image](https://user-images.githubusercontent.com/17786795/128557595-8f65d5ee-8c35-4887-b2c0-b11e4d7e43b6.png)

Remeber you can always make your cluster even more denser by repeated clicking again on top of these points as shown below:
![image](https://user-images.githubusercontent.com/17786795/128557739-b7018796-2cb3-4101-9505-93acbea8018b.png)
Here i repeated clicked on the small sized clusters to make them more dense.






Since we know now how to create dataset lets move on to how to run algorithms on our data set?

Kmeans:
Once our data set is created to run kmeans on this data set press ENTER or RETURN. If Everything works well you will be now able to see Kmeans running on your screen.
We can control how many clusters our algorithm will find by just changing the in_clusters variable in the config.py file.

We can also choose to run kmeans++ by pressing the k key from keyboeard.Only difference is rather than choosing the initial centroids randomly here we choose it probabistically.

I ran Kmeans with different datasets showing its limitations as shown below:

As we can see kmeans does not performs well on different sized clusters and tends to break the bigger cluster. Ran it with in_clusters = 3
![image](https://user-images.githubusercontent.com/17786795/128588877-46e97845-a933-4f1f-9443-714db00e670f.png)

Another problem of kmeans is when we have differnt densities clusters it then also it does not work ver well. Ran it with in_clusters = 3
![image](https://user-images.githubusercontent.com/17786795/128588912-bc81a1df-a82e-4754-8d44-08a250746bc0.png)

Kmeans does not perform well on non gobular structure also as shown below. in_clusters = 2.
![image](https://user-images.githubusercontent.com/17786795/128589115-744e0722-3cf9-4373-a612-697dfed6d690.png)


WE can overcome kmeans limitation by increasing the k or in_clusters in our case.
Here the results i got when in_clusters = 7 for different data sets.
![image](https://user-images.githubusercontent.com/17786795/128589084-95acc87b-81e1-419d-928c-be3e61a16246.png)

![image](https://user-images.githubusercontent.com/17786795/128589106-3af8e39b-7fb0-4680-9507-1cd51f999854.png)

![image](https://user-images.githubusercontent.com/17786795/128589125-b13d1a58-249e-4eba-a2bb-ec458fc49a89.png)


Heirarchical Clustering:

We can run the Agglomerative clustering algorithm.

Here we have three options to provide the linkage parameter for this algorithm those are  MIN, MAX and WARD.


To run this algorithm with MIN linkage just press l key from your keyboard after creating the data sets.
To run this algorithm with MAX linkage just press g key from your keyboard after creating the data sets.
To run this algorithm with WARD linkage just press w key from your keyboard after creating the data sets.

However just as a note of caution since the runtime complexity of this algorithm is O(n^3) hence please be a bit patient with it while it is running on larger number of data points.
You can always track the progress from your terminal also where each algorithm will display the stage that is being run.


One of the strength of MIN linkage is that it can handle non elleptical clusters as shown:(in_clusters = 2)
![image](https://user-images.githubusercontent.com/17786795/128589319-7efcdc59-a1b7-489a-b535-f3c502a80cce.png)

Limitation of MIN is that it is too sensitive to noise or outliers
![image](https://user-images.githubusercontent.com/17786795/128589357-b4dcfb79-c53e-4d41-be0d-2dd672491394.png)

Limitation of MAX is that it tends to break larger clusterers as shown:
![image](https://user-images.githubusercontent.com/17786795/128589392-690ca77c-0443-4c22-9281-229fbf161a84.png)


DBSCAN:

Density based clusestring is another algorithm that we can run.

To run it just press d key from your keyboard.

The behaviour of this algorithm is controlled by 3 variables nodes_in_leaf, eps and min_samples. nodes_in_leaf represents the minimum number of points we want to have in our leaves of the built kd tree.

eps represents the radius of the hypercuboid we want to consider.

min_samples represent the min points required by the any point in its surrounding area to be called as a core point.

we can change these values to see the changes in our clustering.

Also you can run dbscan for different eps values and check the result. For doing so just fill in the variable eps_list with differnt value that you want to try and run the algorithm.

in the below examples the following values were used: number_points_per_cluster = 25, spread = 10, nodes_in_leaf = 6,eps = 8,min_samples = 4




This algorithm runs in 2 stages:

In stage 1 it calculates all the core, boundary and noise points in our data set. We can see it running on our visualizer where Green color represents core points,Blue color represents Boundary points and red color represents noise points.

Here is the result i got while running it on a particular data set:
![image](https://user-images.githubusercontent.com/17786795/128589655-11bf99e8-6981-46d6-93a2-7e46c2e91248.png)

In stage 2 it clusters the given data set. Result that i got:
![image](https://user-images.githubusercontent.com/17786795/128589678-eba33559-3747-4c52-baa0-419344eeebb4.png)


Limitations of dbscan is that it does not work well with varying densities of clusters as shown :
![image](https://user-images.githubusercontent.com/17786795/128589916-36f3da2c-6614-4d47-a96d-fa8844facb0f.png)

Changing our variables a bit will also result in the following clustering:
![image](https://user-images.githubusercontent.com/17786795/128590679-cd0025e8-6d4d-4c37-9b37-e3cbc32a7ad0.png)


HOW TO RUN DIFFERRNT ALGORITHMS ON CREATED DATASET?

At any stage after the algorithm has finished if u wish to run another algorithm on the same dataset, just press r key it will reset your screen with original datapoints and run the desired algorithm.


I hope this was helpful in running and understanding the visualizer. There will be shortcomings i know in this , but will try to my best to remove them with time.
Thanks for reading.















