import argparse
import numpy as np

def cluster_numpy(points_list, Max_iterations=10, clusters=3, print_output=False):
    """Collect together clusters of nearby points using Numpy.
    
    Randomly selects a number of points to centre around. The algorithm then assigns each datapoint to one of these centres to form a cluster. \
        The midpoint of each cluster is then selected as the new centre and this is then repeated for a given number of iterations. \
            This ultimately gives the user clusters of closely related points. \
                This function works the same as 'cluster', except it uses functions found in the Numpy module, allowing the algorithm to run faster.
            
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
        If the given number of clusters is larger than the number of entered points."""
    points_number=len(points_list)
    if clusters > points_number:
        raise(ValueError("Number of clusters must be smaller than the number of given points."))
    
    dimension = len(points_list[0])
    clusters_information = {}
    points_list=np.array(points_list)
    alloc=np.empty(points_number)
    centers=points_list[np.random.choice(points_number,size=clusters,replace=False)]
    
    iteration = 0
    while iteration < Max_iterations:

        alloc=Calculate_index(points_list,centers)

        for i in range(clusters):
            indices = np.argwhere(alloc == i)
            alloc_ps = points_list[indices]
            new_mean = np.mean(alloc_ps,axis=0)
            centers[i] = new_mean

            if iteration == Max_iterations-1:
                #Convert allocated points into a list of tuples
                alloc_ps_converted = list(map(tuple, alloc_ps.reshape((alloc_ps.shape[0], dimension))))
                clusters_information[i]={'center': centers[i].tolist(),'allocated_points': alloc_ps_converted}
        iteration +=1
    if print_output:
        print_points(clusters_information)
    else:
        return clusters_information

def print_points(clusters_information):
    """Print output."""
    for cluster, dic in clusters_information.items():
        center = dic['centers']
        allocated_points = dic['allocated_points']
        print("Cluster " + str(cluster) + " is centred at " + str(center) + " and has " + str(len(allocated_points)) + " points.")
        print_list=[]
        for i in allocated_points:
            print_list.append(i)
        print(print_list)


def Calculate_index(points, mean_point):
    """Finds the indices of the clusters which are closest to each point in the given array."""
    return np.argmin(np.linalg.norm(points-mean_point[:,None],axis=2),axis=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Seperating points into clusters.')
    parser.add_argument('data', metavar = 'data', help = 'Input a dataset to analyse.')
    parser.add_argument('--iters', type = int, default = 10, help = 'Input the iteration times (default is 10).')
    args = parser.parse_args()
    lines = open(str(args.data), 'r').readlines()
    points = []
    for line in lines: points.append(tuple(map(float, line.strip().split(','))))
    cluster_numpy(points, args.iters, print=True)