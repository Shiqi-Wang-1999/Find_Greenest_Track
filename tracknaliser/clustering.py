from math import sqrt
from random import randrange
import argparse

def cluster(points_list, Max_iterations=10, clusters = 3, output_print=False):
    """Collect together clusters of nearby points.
    
    Randomly selects a number of points to centre around. The algorithm then assigns each datapoint to one of these centres to form a cluster. \
        The midpoint of each cluster is then selected as the new centre and this is then repeated for a given number of iterations. \
            This ultimately gives the user clusters of closely related points.
            
    Parameters
    ----------
    points_list: list of tuples
        List of data points which will form the clusters.
    Max_iterations: int, optional
        Number of iterations to run the algorithm for (default is 10).
    clusters: int, optional
        Number of clusters to form (default is 3).
    output_print: bool, optional
        If True the output clusters and relevant points will be printed. If False the function will return a dictionary with the relevant information (default is False).
        
    Returns
    -------
    cluster_information: dict
        Nested dictionary with the keys corresponding to each cluster. \
            Within the dictionary lies a further dictionary containing a list of the centres and a list of tuples of the relevant points for each cluster.
    
    Raises
    ------
    ValueError
        If the number of entered points is less than the number of clusters.
    ZeroDivisionError
        If the algorithm fails due to no points being assigned to a cluster. It can either be re-ran with a chance of success or the number of clusters could be reduced."""

    if clusters > len(points_list):
        raise ValueError("Number of clusters must be smaller than the number of given points.")
    
    # Pick n points randomly to be the initial centres of the clusters where n is the number of clusters in the 'clusters' argument
    dimension = len(points_list[0])
    centers = []
    clusters_information = {}
    for _ in range(clusters):
        centers.append(rand_point(points_list))
    # Multiple iterations
    iteration=0
    while iteration < Max_iterations:
        #Update the centre of each cluster by setting it to the average of all points assigned to the cluster
        allocated_cluster = [find_best_cluster(clusters, point, centers, dimension) for point in points_list]
        for cluster_id in range(clusters):
            allocated_points=[point for point_index, point in enumerate(points_list) if allocated_cluster[point_index] == cluster_id]
            if len(allocated_points) == 0:
                pass
            else:
                centers[cluster_id]=mid_point(allocated_points, dimension)
           #On final iteration, write the centres and points into a dictionary
            if iteration == Max_iterations -1:
                clusters_information[cluster_id] = {'center': centers[cluster_id], 'allocated_points': allocated_points}
        iteration +=1
    if output_print:
        print_points(clusters_information)
    else: 
        return clusters_information

def find_best_cluster(clusters, point, centers, dimension):
    """Assign each data point to a cluster by computing the distance."""
    distance = [None] * clusters
    for cluster_id in range(clusters):
        distance[cluster_id]= calculate_distance(centers[cluster_id], point, dimension)
    return distance.index(min(distance))

def calculate_distance(center_point, point, dimension):
    """Calculate distance between points."""
    square_distance = 0
    for i in range(dimension):
        square_distance += (point[i]-center_point[i])**2
    return sqrt(square_distance)

def mid_point(points, dimension):
    """Find the average point for a given list of points."""
    centers = []
    for i in range(dimension):
        centers.append(sum([point[i] for point in points]) / len(points))
    return tuple(centers)

def rand_point(points):
    """Select a random point within a list of points."""
    rand = points[randrange(len(points))]
    return rand

def print_points(clusters_information):
    """Print output."""
    for cluster, dic in clusters_information.items():
        center = dic['centers']
        allocated_points = dic['allocated_points']
        print("Cluster " + str(cluster) + " is centred at " + str(center) + " and has " + str(len(allocated_points)) + " points.")
        print(allocated_points)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Seperating points into clusters.')
    parser.add_argument('data', metavar = 'data', help = 'Input a dataset to analyse.')
    parser.add_argument('--iters', type = int, default = 10, help = 'Input the iteration times (default is 10).')
    args = parser.parse_args()
    lines = open(str(args.data), 'r').readlines()
    points = []
    for line in lines: points.append(tuple(map(float, line.strip().split(','))))
    cluster(points, args.iters, print=True)