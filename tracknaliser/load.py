"""Functions to load in tracks data."""
from .tracks import Tracks, SingleTrack
import os
import json
import requests
import doctest
import time

def load_tracksfile(file_path):
    """
        Loads in data from a group of tracks in a JSON file.

        This function takes a given filepath where a JSON file should be located. Within this JSON file should be a dictionary with the following layout:
        {'metadata': {'datetime': ..., 'end': ..., 'start': ..., 'mapsize': ..., ...}, 'tracks:[{'cc': ..., 'elevation': ..., 'road': ..., 'terrain': ...}, ...]}
        The function then outputs a Tracks object containing the relevant information.

        Parameters
        ----------
        file_path: pathlib.posixpath object or pathlib.windowspath object
            The path along which the JSON file containing the track data exists.

        Returns
        -------
        tracks: Tracks object
            Tracks object containing information of the tracks stored. The tracks are stored as SingleTrack objects in the Tracks.tracks_list attribute.

        Raises
        ------
        OSError
            If the file_path does not exist.
        TypeError
            If the extracted information from the JSON file is not a dictionary
        KeyError
            If the structure of the dictionary is unexpected. Details of the tracks must be held under the 'metadata' key with the specific track data found under the 'tracks' key.

        See Also
        --------
        Tracks: :class:`Tracks class <tracks.Tracks>`
        SingleTrack: :class:`SingleTrack class <tracks.SingleTrack>`

        Examples
        --------
        >>> from pathlib import Path
        >>> filepath = "tests/short_tracks.json"
        >>> load_tracksfile(filepath)
        <Tracks: 5 from (2, 3) to (4, 2)>
        """
    #Checks if the file exists
    does_file_exist(file_path)

    with open(file_path, encoding='utf-8') as file:
        line = file.readline()
        if str(file_path).endswith('.json'):
            dic = json.loads(line)
        else:
            raise TypeError("Input data must be JSON.")
    
    # Checks if the dictionary structure is as expected
    is_well_structured(dic)

    #list for singletrack object
    tracks_list=[]

    #split metadata data
    start=(dic['metadata']['start'][0],dic['metadata']['start'][1])
    end=(dic['metadata']['end'][0],dic['metadata']['end'][1])
    map_size=(dic['metadata']['mapsize'][0],dic['metadata']['mapsize'][1])
    date=dic['metadata']['datetime']

    # split tracks data
    for tracks in dic['tracks']:
        cc=tracks['cc']
        road=tracks['road']
        terrain=tracks['terrain']
        elevation=tracks['elevation']

        # check validation of chain-codes and road properties
        check_illegal_values(cc,road,terrain,elevation)
        #create singletrack object and put into tracks_list
        tracks_list.append(SingleTrack(start, cc, road, terrain, elevation))

    # check validation of 'tracks' parameter
    check_tracks_parameter(date, map_size, end, start)
    #create tracks object
    tracks_obj = Tracks(start, end, map_size, date, tracks_list)
    return tracks_obj



def query_tracks(start=(0, 0), end=(299, 299), min_steps_straight=1, max_steps_straight=None, n_tracks=300, save=True):
    """
        Loads tracks data from an external website.

        A query is sent to a website hosted on an external server with the given parameters. The function then processes this data, ensuring it is of the correct form, and returns a Track object containing the data.

        Parameters
        ----------
        start: list or tuple, optional
            (x,y) coordinates relating to the starting point of the track (default is (0,0)).
        end: list or tuple, optional
            (x,y) coordinates relating to the end point of the track (default is (299,299)).
        min_steps_straight: int, optional
            Minimum number of steps going straight on (default is 1).
        max_steps_straight: int, optional
            Maximum number of steps going straight on (default is 5 more than min_steps_straight).
        n_tracks: int, optional
            Number of tracks to be queried (default is 300).
        save: bool, optional
            Optional argument. If True the data will be saved as a dictionary to a JSON file. If False the function will output a Tracks object with the relevant data (default is True).

        Returns
        -------
        tracks: Tracks object
            Tracks object containing information of the tracks stored. The tracks are stored as SingleTrack objects in the Tracks.tracks_list attribute. Only outputs if save=False.

        Raises
        ------
        KeyError
            If the structure of the dictionary is unexpected. Details of the tracks must be held under the 'metadata' key with the specific track data found under the 'tracks' key.
        TypeError
            If the inputs are of the incorrect data type.
        ValueError
            If the inputs have values which are not allowed by the function.

        See Also
        --------
        Tracks: :class:`Tracks class <tracks.Tracks>`
        SingleTrack: :class:`SingleTrack class <tracks.SingleTrack>`
        """
    # set max_steps_straight default equals to min_steps_straight + 5
    if max_steps_straight is None:
        max_steps_straight = min_steps_straight + 5

    # check validation of user's input
    check_coordinate_valid("start", start)
    check_coordinate_valid("end", end)
    if (type(min_steps_straight) != int) or (type(max_steps_straight) != int) or (type(n_tracks) != int) or (type(save) != bool):
        raise TypeError("Please input the steps straight, 'n_tracks' with int type, and 'save' with bool type.")
    if (min_steps_straight < 0) | (max_steps_straight < 0) | (n_tracks < 0):
        raise ValueError("The value of steps straight and n_tracks should be positive integer.")
    if min_steps_straight > max_steps_straight:
        raise ValueError("max_steps_straight must be greater than min_steps_straight.")

    # query from web service
    url='http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?start_point_x='+str(start[0])\
        +'&start_point_y='+str(start[1])+'&n_tracks='+str(n_tracks)+'&end_point_x='+str(end[0])\
        +'&end_point_y='+str(end[1])+'&min_steps_straight='+str(min_steps_straight)+'&max_steps_straight='\
        +str(max_steps_straight)
    if isConnected(url):
        r = requests.get(url)
        dic = r.json()
        # Checks if the dictionary structure is as expected
        is_well_structured(dic)
    else:
        raise ConnectionError("No Internet Connection.")

    if save is True:
        datetime = dic['metadata']['datetime']
        new_datetime = ''.join(char for char in datetime if char.isalnum())

        name = 'tracks_'+new_datetime+'_'+str(n_tracks)+'_'+str(start[0])+'_'+str(start[1])+'_'+str(end[0])+'_'\
               +str(end[1])+'.json'

        with open(name,'w') as file_obj:
            json.dump(dic, file_obj)
    else:
        return dict_to_tracks(dic)


# ------function to convert dictionary to Tracks object------
def dict_to_tracks(dic):
    """Converts a dictionary of track data into a Tracks object."""
    tracks_list = []

    # Split metadata data
    start = (dic['metadata']['start'][0], dic['metadata']['start'][1])
    end = (dic['metadata']['end'][0], dic['metadata']['end'][1])
    map_size = (dic['metadata']['mapsize'][0], dic['metadata']['mapsize'][1])
    date = dic['metadata']['datetime']

    # Split tracks data
    for tracks in dic['tracks']:
        cc = tracks['cc']
        road = tracks['road']
        terrain = tracks['terrain']
        elevation = tracks['elevation']
        # check validation of chain-codes and road properties
        check_illegal_values(cc, road, terrain, elevation)
        tracks_list.append(SingleTrack(start, cc, road, terrain, elevation))

    # check validation of 'tracks' parameter
    check_tracks_parameter(date, map_size, end, start)
    # Create tracks object
    tracks_obj = Tracks(start, end, map_size, date, tracks_list)
    return tracks_obj


# -------function for query_tracks-----------
def isConnected(url):
    """Tests if the user has an internet connection."""
    try:
        requests.get(url,timeout=30)
        return True
    except ConnectionError:
        return False


# -------function for load tracks file-----------
def does_file_exist(file_path):
    """Tests if a file path exists."""
    if not os.path.exists(file_path):
        raise OSError("File is not accessible.")


def is_well_structured(dic):
    """Checks if the dictionary structure is as expected."""
    if type(dic) != dict:
        raise TypeError("The input data should be a dictionary")
    necessary_keys = ['metadata', 'tracks']
    necessary_metadata_keys = ['datetime', 'end', 'mapsize', 'start']
    necessary_tracks_keys = ['cc', 'elevation', 'road', 'terrain']
    
    # Check dict structure
    for key in necessary_keys:
        if key not in dic.keys():
            raise(KeyError("Missing keys in dictionary. Must have keys metadata and tracks."))

    # Check metadata data structure
    for key in necessary_metadata_keys:
        if key not in dic['metadata'].keys():
            raise(KeyError("Missing data in dictionary. Metadata must have keys datetime, end, mapsize and elevation."))

    # Check track structure
    for track in dic['tracks']:
        for key in necessary_tracks_keys:
            if key not in track.keys():
                raise(KeyError("Missing data in track information. Must have keys cc, elevation, road and terrain."))


# -------function for validation-----------
def check_illegal_values(cc, road, terrain, elevation):
    """Validation for individual tracks."""
    # check the number of characters
    if (len(cc)+1 != len(elevation)) | (len(cc) != len(terrain)) | (len(cc) != len(road)):
        raise ValueError("Please ensure that for each single track, the lengths of chaincode, terrain, road are same and equal to elevation - 1.")

    if type(cc) != str:
        raise TypeError("Chain code must be string.")
    for digit in cc:
        if digit not in ['1','2','3','4']:
            raise(ValueError("Chain Code must consist of digits 1, 2, 3, 4."))

    if type(elevation) != list:
        raise (TypeError("The elevation of a single track should be a list."))
    for i in elevation:
        if type(i) != int:
            raise(TypeError("Elements in the elevation list should be integer."))

    if type(road) != str:
        raise TypeError("Road type must be string.")
    for i in road:
        if i not in ['r','l','m']:
            raise(ValueError("Road type must consist of the characters r, l or m."))

    if type(terrain) != str:
        raise TypeError("Terrain must be string.")
    for i in terrain:
        if i not in ['p','g','d']:
            raise(ValueError("Terrain must consist of characters p, g or d."))


def is_valid_date(strdate):
    """Checks if the date is valid."""
    try:
        time.strptime(strdate, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False


def check_tracks_parameter(date, map_size, end, start):
    """Checks the parameters for the tracks object."""
    if (type(date) != str):
        raise TypeError("The type of date must be string")

    if not is_valid_date(date):
        raise(ValueError("Date is not valid."))

    check_coordinate_valid("map size", map_size)
    check_coordinate_valid("end", end)
    check_coordinate_valid("start", start)

    if end[0] > map_size[0] or end[1] > map_size[1]:
        raise(ValueError("Coordinate of end is outside of map."))

    if start[0] > map_size[0] or start[1] > map_size[1]:
        raise(ValueError("Coordinate of start is outside of map."))


def check_coordinate_valid(coordinate_name, list_or_tuple):
    """General function to check if a coordinate is valid."""
    if (type(list_or_tuple) != list) and (type(list_or_tuple) != tuple):
        raise TypeError("Coordinate of " + coordinate_name + f" {list_or_tuple} must be List or Tuple.")
    elif len(list_or_tuple) != 2:
        raise(ValueError("Coordinate of " + coordinate_name + f" {list_or_tuple} must be 2D."))
    for coordinate in list_or_tuple:
        if type(coordinate) != int:
            raise(TypeError("Coordinate of " + coordinate_name + f" {list_or_tuple} must be integer."))
        elif (coordinate_name == "map size") & (coordinate < 0 or coordinate > 300):
            raise(ValueError("The maximum map size is 300 x 300."))
        elif (coordinate_name == "end" or coordinate_name == "start") & (coordinate < 0 or coordinate > 299):
            raise(ValueError("Coordinate of " + coordinate_name + f" {list_or_tuple} is outside of the maximum map size."))
