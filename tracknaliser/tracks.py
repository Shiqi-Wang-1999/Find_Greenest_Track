"""Classes designed to analyse tracks."""
from math import sqrt
from .clustering_numpy import cluster_numpy
import matplotlib.pyplot as plt
import numpy as np
import doctest

class Tracks:
    """A class containing information of a list of SingleTrack objects.

    This class is designed to hold information from tracks along a map that have been loaded in externally. \
    These tracks are stored as SingleTrack objects in the tracks attribute with various further attributes giving more information. \
    The methods of the class give us a way to pick out a particlular track, find the best tracks under certain conditions and group similar tracks.\

    Attributes
    ----------
    start: tuple or list
        The starting point of the track in (x,y) coordinates.
    end: tuple or list
        The ending point of the track in (x,y) coordinates.
    map_size: tuple or list
        The total size of the map in (x,y) coordinates.
    date: datetime object
        The date in which the query loading the tracks was run.
    tracks: list
        A list of the SingleTrack objects stored in the class.
    """
    def __init__(self, start, end, map_size, date, tracks_list):
        """
        Parameters
        ----------
        start: tuple or list
            The starting point of the track in (x,y) coordinates.
        end: tuple or list
            The ending point of the track in (x,y) coordinates.
        map_size: tuple or list
            The total size of the map in (x,y) coordinates.
        date: datetime object
            The date in which the query loading the tracks was run.

        Examples
        --------
        >>> tracks_list = [SingleTrack((2, 3), "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14]), \
            SingleTrack((2,3), "443411122", "rrrrrrrrr", "ppddppggg", [17, 12, 7, 6, 1, 2, 3, 4, 9, 14]), \
                SingleTrack((2,3), "3341111", "llrrrrr", "ddddppg", [17,16,15,10,11,12,13,14]), \
                    SingleTrack((2,3), "21144", "mmmlr", "ppggg", [17, 22, 23, 24, 19, 14]), \
                        SingleTrack((2,3), "343411121", "lrrrrrrrr", "dddddpppg", [17, 16, 11, 10, 5, 6, 7, 8, 13, 14])]
        >>> tracks = Tracks((2,3), (4,2), (5,5), "2021-12-11T21:12:20", tracks_list)
        >>> tracks
        <Tracks: 5 from (2, 3) to (4, 2)>
        """
        self.start = start
        self.end = end
        self.map_size = map_size
        self.date = date
        self.tracks = tracks_list

    def __len__(self):
        return len(self.tracks)

    def __repr__(self):
        return "<Tracks: %s from %s to %s>" % (len(self.tracks), tuple(self.start), tuple(self.end))
    
    def greenest(self):
        """
        Find the track which releases the least CO2.
        
        Returns
        -------
        track: SingleTrack object
            Track which outputs the least amount of CO2.
        
        Raises
        ------
        AttributeError
            If there are no tracks stored in the class.
        
        Examples
        --------
        >>> tracks_list = [SingleTrack((2, 3), "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14]), \
            SingleTrack((2,3), "443411122", "rrrrrrrrr", "ppddppggg", [17, 12, 7, 6, 1, 2, 3, 4, 9, 14]), \
                SingleTrack((2,3), "3341111", "llrrrrr", "ddddppg", [17,16,15,10,11,12,13,14]), \
                    SingleTrack((2,3), "21144", "mmmlr", "ppggg", [17, 22, 23, 24, 19, 14]), \
                        SingleTrack((2,3), "343411121", "lrrrrrrrr", "dddddpppg", [17, 16, 11, 10, 5, 6, 7, 8, 13, 14])]
        >>> tracks = Tracks((2,3), (4,2), (5,5), "2021-12-11T21:12:20", tracks_list)
        >>> tracks.greenest()
        <SingleTrack: starts at (2, 3) - 5 steps>
        """
        if len(self) == 0:
            raise(AttributeError("No tracks stored."))  
        co2s = [track.co2() for track in self.tracks]
        index_min = np.argmin(np.array(co2s))
        return self.tracks[index_min]

    def fastest(self):
        """
        Find the fastest track.
        
        Returns
        -------
        track: SingleTrack object
            Track which takes the least amount of time to traverse.
        
        Raises
        ------
        AttributeError
            If there are no tracks stored in the class.

        Examples
        --------
        >>> tracks_list = [SingleTrack((2, 3), "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14]), \
            SingleTrack((2,3), "443411122", "rrrrrrrrr", "ppddppggg", [17, 12, 7, 6, 1, 2, 3, 4, 9, 14]), \
                SingleTrack((2,3), "3341111", "llrrrrr", "ddddppg", [17,16,15,10,11,12,13,14]), \
                    SingleTrack((2,3), "21144", "mmmlr", "ppggg", [17, 22, 23, 24, 19, 14]), \
                        SingleTrack((2,3), "343411121", "lrrrrrrrr", "dddddpppg", [17, 16, 11, 10, 5, 6, 7, 8, 13, 14])]
        >>> tracks = Tracks((2,3), (4,2), (5,5), "2021-12-11T21:12:20", tracks_list)
        >>> tracks.fastest()
        <SingleTrack: starts at (2, 3) - 5 steps>
        """
        if len(self) == 0:
            raise(AttributeError("No tracks stored.")) 
        times = [track.time() for track in self.tracks]
        index_min = np.argmin(np.array(times))
        return self.tracks[index_min]

    def shortest(self):
        """
        Find the shortest track.
        
        Returns
        -------
        track: SingleTrack object
            Track which is the shortest in distance.
        
        Raises
        ------
        AttributeError
            If there are no tracks stored in the class.
        
        Examples
        --------
        >>> tracks_list = [SingleTrack((2, 3), "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14]), \
            SingleTrack((2,3), "443411122", "rrrrrrrrr", "ppddppggg", [17, 12, 7, 6, 1, 2, 3, 4, 9, 14]), \
                SingleTrack((2,3), "3341111", "llrrrrr", "ddddppg", [17,16,15,10,11,12,13,14]), \
                    SingleTrack((2,3), "21144", "mmmlr", "ppggg", [17, 22, 23, 24, 19, 14]), \
                        SingleTrack((2,3), "343411121", "lrrrrrrrr", "dddddpppg", [17, 16, 11, 10, 5, 6, 7, 8, 13, 14])]
        >>> tracks = Tracks((2,3), (4,2), (5,5), "2021-12-11T21:12:20", tracks_list)
        >>> tracks.shortest()
        <SingleTrack: starts at (2, 3) - 5 steps>
        """
        if len(self) == 0:
            raise(AttributeError("No tracks stored.")) 
        lengths = [track.distance() for track in self.tracks]
        index_min = np.argmin(np.array(lengths))
        return self.tracks[index_min]

    def kmeans(self, iterations=10, clusters=3):
        """Collect together tracks of similar attributes.
        
        This function uses the k_means algorithm to group together tracks with similar variables. \
            The algorithm selects random tracks to centre around and then assigns similar tracks to this cluster. \
                It then creates a new centre based on the average of the assigned track variables and runs again through a number of iterations. \
                    The variables used to centre around are the co2, distance and time methods of the SingleTrack object.
                    
        Parameters
        ----------
        iterations: int, optional
            Number of iterations to run the algorithm through (default is 10).
        clusters: int, optional
            Number of clusters to form (default is 3).
        
        Returns
        -------
        list of tracks: list
            List containing further lists with the indices of the tracks with similar attributes. The number of lists within the output should match the clusters parameter.
        """
        #Example cannot be run here since we are using a random variable. We could set a seed number and a further function input which uses a random variable if True but I don't think this is needed since the examples are similar to the other methods.
        clustered_tracks = [[] for _ in range(clusters)]
        points = [(track.co2(), track.time(), track.distance()) for track in self.tracks]
        cluster_info = cluster_numpy(points, Max_iterations=iterations, clusters=clusters)
        for key, info in cluster_info.items():
            for allocated_points in info['allocated_points']:
                for index, point in enumerate(points):
                    if allocated_points == point:
                        clustered_tracks[key].append(index)
                        break
        return clustered_tracks

    def get_track(self, x):
        """
        Find a specific track.
        
        Parameters
        ----------
        x: int
            Number of the desired track.
        
        Returns
        -------
        track: SingleTrack object
            The requested track.
        
        Raises
        ------
        AttributeError
            If there are no tracks stored in the class.
        ValueError
            If x is greater than the number of tracks stored.

        Examples
        --------
        >>> tracks_list = [SingleTrack((2, 3), "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14]), \
            SingleTrack((2,3), "443411122", "rrrrrrrrr", "ppddppggg", [17, 12, 7, 6, 1, 2, 3, 4, 9, 14]), \
                SingleTrack((2,3), "3341111", "llrrrrr", "ddddppg", [17,16,15,10,11,12,13,14]), \
                    SingleTrack((2,3), "21144", "mmmlr", "ppggg", [17, 22, 23, 24, 19, 14]), \
                        SingleTrack((2,3), "343411121", "lrrrrrrrr", "dddddpppg", [17, 16, 11, 10, 5, 6, 7, 8, 13, 14])]
        >>> tracks = Tracks((2,3), (4,2), (5,5), "2021-12-11T21:12:20", tracks_list)
        >>> tracks.get_track(0)
        <SingleTrack: starts at (2, 3) - 11 steps>
        """
        if len(self) == 0:
            raise(AttributeError("No tracks stored."))
        if x > len(self):
            raise(ValueError(f"Track number given is larger than the number of tracks stored ({len(self)})." ))
        return self.tracks[x]

class SingleTrack:
    """A class containing information for a single track.

    This class is designed to hold information from a single track which traverses a map. \
    The track is defined by a set of chain codes which describe the direction the track takes in the map.\
    The properties such as the height, terrain and type of road are also stored for each section along the track.\
    The methods of the class give us a way of visualising the track, as well as determining certain properties such \
        as the CO2 output, the distance and the time taken to traverse it.

    Attributes
    ----------
    start: tuple or list
        The starting point of the track in (x,y) coordinates.
    cc: string
        Chain code containing numbers 1, 2, 3 & 4 corresponding to moving East, North, West and South, respectively.
    road: string
        Defines the type of road along the track. Contains letters r, l & m meaning residential, local and motorway, respectively.
    terrain: string
        Defines the terrain along the track. Contains letters d, g & p meaning dirt, gravel and paved, respectively.
    elevation: string
        Gives the elevation of the track at each coordinate in m.
    """
    def __init__(self, start, cc, road, terrain, elevation):
        """
        Parameters
        ----------
        start: tuple or list
        The starting point of the track in (x,y) coordinates.
        cc: string
            Chain code containing numbers 1, 2, 3 & 4 corresponding to moving East, North, West and South, respectively.
        road: string
            Defines the type of road along the track. Contains letters r, l & m meaning residential, local and motorway, respectively.
        terrain: string
            Defines the terrain along the track. Contains letters d, g & p meaning dirt, gravel and paved, respectively.
        elevation: list
            Gives the elevation of the track at each coordinate in m.

        Examples
        --------
        >>> SingleTrack([2, 3], "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14])
        <SingleTrack: starts at (2, 3) - 11 steps>
        """
        self.start = start
        self.cc = cc
        self.road = road
        self.terrain = terrain
        self.elevation = elevation

    def __len__(self):
        return len(self.cc) + 1  # There are N - 1 chaincodes

    def __repr__(self):
        return "<SingleTrack: starts at %s - %s steps>" % (tuple(self.start), len(self.cc))

    def corners(self):
        """
        Find the corners of the track.

        Returns
        -------
        corners: list
            list of tuples pertaining to the coordinates of the corners of the track.
        
        Examples
        --------
        >>> singletrack = SingleTrack([2, 3], "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14])
        >>> singletrack.corners()
        [(2, 3), (4, 3), (4, 4), (1, 4), (1, 2), (4, 2)]
        """
        coordinate = list(self.start)
        corner_list = [tuple(self.start)]
        prev = None
        for direction in self.cc:
            if prev is None:
                pass
            elif (int(prev) - int(direction))%2 == 1:
                corner_list.append(tuple(coordinate))
            
            if direction == '1':
                coordinate[0] += 1
            elif direction == '2':
                coordinate[1] += 1
            elif direction == '3':
                coordinate[0] -= 1
            elif direction == '4':
                coordinate[1] -=1

            prev = direction
        corner_list.append(tuple(coordinate))
        return corner_list

    def visualise(self, show=True, filename="track.png"):
        """
        Plot both the elevation along the track and the route of the track itself.
        
        Parameters
        ----------
        show: bool, optional
            If True the method will show the plots in a figure. If False it will save the output under the given filename (default is True).
        filename: string, optional
            The filename we wish to save the plot under, if the show parameter is True (default is "track.png").
        """
        x = [coords[0] for coords in self.corners()]
        y = [coords[1] for coords in self.corners()]
        distance = range(len(self.elevation))
        plot = plt.figure(1, figsize=(10,5))
        plot.add_subplot(1,2,1)
        plt.plot(distance, self.elevation)
        plt.xlabel("Distance")
        plt.ylabel("Elevation")
        plt.title("Change of Elevation with distance travelled")

        plot.add_subplot(1,2,2)
        plt.plot(x,y)
        plt.xlabel("Distance in x direction")
        plt.ylabel("Distance in y direction")
        plt.title("Track taken")
        plt.tight_layout()
        if show:
            plt.show()
        else:
            plt.savefig(filename)

    def co2(self, base_consumption=5.4, co2_per_litre=2.6391, \
        road_cons = {'r': 1.4, 'l': 1, 'm': 1.25}, \
        terrain_cons = {'d': 2.5, 'g': 1.25, 'p': 1}, \
        slope_cons = {-8: 0.16, -4: 0.45, 0: 1, 4: 1.3, 8: 2.35, 12: 2.9}):
        """
        Find the amount of CO2 released after traversing the track in kg.
        
        Parameters
        ----------
        base_consumption: float, optional
            The consumption of the car modelled under normal conditions per 100km (default is 5.4).
        co2_per_litre: float, optional
            The amount of CO2 produced per litre of fuel used (default is 2.6391).
        road_cons: dict, optional
            The consumption factor for each type of road (default is {'r': 1.4, 'l': 1, 'm': 1.25}).
        terrain_cons: dict, optional
            The consumption factor for each terrain type (default is {'d': 2.5, 'g': 1.25, 'p': 1}).
        slope_cons: dict, optional
            The consumption factor for each % of slope (default is {-8: 0.16, -4: 0.45, 0: 1, 4: 1.3, 8: 2.35, 12: 2.9}).

        Returns
        -------
        co2: float
            The amount of CO2 released after traversing the track in kg.

        Examples
        --------
        >>> singletrack = SingleTrack([2, 3], "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14])
        >>> singletrack.co2()
        2.8484609645484342
        """
        co2 = 0
        prev = None
        for index, height in enumerate(self.elevation):
            if prev == None:
                pass
            else:
                height_diff = height - prev
                distance = sqrt(1 + (height_diff/1000)**2)
                slope = height_diff/10
                for key, value in road_cons.items():
                    if key == self.road[index-1]:
                        f_r = value
                        break

                for key, value in terrain_cons.items():
                    if key == self.terrain[index-1]:
                        f_t = value
                        break
                            
                if slope < -6:
                    f_s = slope_cons[-8]
                elif slope >= -6 and slope < -2:
                    f_s = slope_cons[-4]
                elif slope >= -2 and slope <= 2:
                    f_s = slope_cons[0]
                elif slope > 2 and slope <= 6:
                    f_s = slope_cons[4]
                elif slope > 6 and slope <= 10:
                    f_s = slope_cons[8]
                else:
                    f_s = slope_cons[12]
                
                co2 += base_consumption*f_t*f_r*f_s*distance*co2_per_litre/100
            prev = height
        return co2

    def distance(self):
        """
        Find the length of the track in km.
        
        Returns
        -------
        distance: float
            The length of the track in km.
            
        Examples
        --------
        >>> singletrack = SingleTrack([2, 3], "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14])
        >>> singletrack.distance()
        11.000041499764627
        """
        distance = 0
        prev = None
        for height in self.elevation:
            if prev == None:
                pass
            else:
                height_diff = height - prev
                distance += sqrt(1 + (height_diff/1000)**2)
            prev = height
        return distance

    def time(self, road_speed = {'r': 30, 'l': 80, 'm': 120}):
        """
        Find the time taken to traverse the track in hours.
        
        Parameters
        ----------
        road_speed: dict, optional
            The average speed in km/h for each type of road (default is {'r': 30, 'l': 80, 'm': 120}).

        Returns
        -------
        time: float
            The time taken to traverse the track in hours.
        
        Examples
        --------
        >>> singletrack = SingleTrack([2, 3], "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14])
        >>> singletrack.time()
        0.2041674187457495
        """
        time = 0
        prev = None
        for index, height in enumerate(self.elevation):
            if prev == None:
                pass
            else:
                height_diff = height - prev
                distance = sqrt(1 + (height_diff/1000)**2)
                
                for key, value in road_speed.items():
                    if key == self.road[index-1]:
                        speed = value
                        break

                time += distance/speed
            prev = height
        return time
        