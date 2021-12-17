import math
from numba import njit
import pandas as pd
import matplotlib.pyplot as plt

'''
Haversine formula used to calculate the great circle distance for two points.

:param lat1: latitude of first coordinate
:param lon1: longitude of first coordinate
:param lat2: latitude of second coordinate
:param lon2: longitude of second coordinate
:return radius * c: Distance between two points in kilometres.

If running this script only, print radius of circles in visualize_tsp.
'''
@njit()
def haversine(lat1, lon1, lat2, lon2):
	
	# difference in latitudes and longitudes, converted to radians.
	dLat = (lat2 - lat1) * math.pi / 180.0
	dLon = (lon2 - lon1) * math.pi / 180.0

	# convert longitude and latitude to radians
	lat1 = (lat1) * math.pi / 180.0
	lat2 = (lat2) * math.pi / 180.0

	# Haversine formula
	a = (pow(math.sin(dLat / 2), 2) +
		pow(math.sin(dLon / 2), 2) *
			math.cos(lat1) * math.cos(lat2))
	radius = 6371
	c = 2 * math.asin(math.sqrt(a))
	return radius * c

if (__name__ == "__main__"):
	print(f"{haversine(60.6747821, 17.143144, 60.7609, 17.143144)} km")
	print(f"{haversine(60.6747821, 17.143144, 60.7434, 17.143144)} km")
	print(f"{haversine(60.6747821, 17.143144, 60.7177, 17.143144)} km")
	print(f"{haversine(60.6747821, 17.143144, 60.7012, 17.143144)} km")
	print(f"{haversine(60.6747821, 17.143144, 60.6832, 17.143144)} km")