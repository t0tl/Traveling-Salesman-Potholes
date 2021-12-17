import matplotlib.pyplot as plt
from Haversine import haversine
from numba import njit
import json
import numpy as np

'''
Class for coordinate points with two methods for getting the distance from the instances.
Includes numba functions for getting the distance from pure data sets.
'''



class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @staticmethod
    def get_distance_NNA(coord_1, coord_2, coords, expected_value):
        """
        Road adjusted distance in kilometers between two nodes using the Haversine formula. 
        :param: coord_1 - Coordinate number x1 in the data set
        :param: coord_2 - Coordinate number x2 in the data set
        :param: coords - Complete set of coordinates (data set)
        :param: expected_value - Expected value from the type-1 distribution
        :return: flight_distance adjusted using the road_distance.
        """
        lat1, lon1, lat2, lon2 = coords[coord_1][1], coords[coord_1][0], coords[coord_2][1], coords[coord_2][0]
        return haversine(lat1, lon1, lat2, lon2)*expected_value

    @staticmethod
    def get_total_distance_NNA(coords, solution, expected_value):
        """
        Road adjusted distance in kilometers between sum of all connected nodes using the Haversine formula. 
        :param: coord_1 - Coordinate number x1 in the data set
        :param: coord_2 - Coordinate number x2 in the data set
        :param: coords - Complete set of coordinates (data set)
        :param: expected_value - Expected value from the type-1 distribution
        :return: Total flight_distance adjusted using the road_distance.
        """
        dist = 0
        for i in range(len(coords)-1):
            dist += Coordinate.get_distance_NNA(solution[i], solution[i+1], coords, expected_value)
        dist += Coordinate.get_distance_NNA(solution[0], solution[-1], coords, expected_value)
        return dist



def read_json_coords(path):
    '''
    Read .json file with data set in path.
    :param: path - file pathway of data set as a string.
    :return: data - returns data set.
    '''
    data = json.load(open(path))
    return data

@njit
def get_distance_two_opt(coord_1, coord_2, coords, expected_value):
        """
        Road adjusted distance in kilometers between two nodes using the Haversine formula. 
        :param: coord_1 - Coordinate number x1 in the data set
        :param: coord_2 - Coordinate number x2 in the data set
        :param: coords - Complete set of coordinates (data set)
        :param: expected_value - Expected value from the type-1 distribution
        :return: flight_distance adjusted using the road_distance.
        """
        lat1, lon1, lat2, lon2 = coords[coord_1][1], coords[coord_1][0], coords[coord_2][1], coords[coord_2][0]
        return haversine(lat1, lon1, lat2, lon2)*expected_value

@njit
def get_total_distance_two_opt(coords, solution, expected_value):
        """
        Road adjusted distance in kilometers between sum of all connected nodes using the Haversine formula. 
        :param: coord_1 - Coordinate number x1 in the data set
        :param: coord_2 - Coordinate number x2 in the data set
        :param: coords - Complete set of coordinates (data set)
        :param: expected_value - Expected value from the type-1 distribution
        :return: Total flight_distance adjusted using the road_distance.
        """
        dist = 0
        for i in range(len(coords)-1):
            dist += get_distance_two_opt(solution[i], solution[i+1], coords, expected_value)
        dist += get_distance_two_opt(solution[0], solution[len(coords)-1], coords, expected_value)
        return dist
