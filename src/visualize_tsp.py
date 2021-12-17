import matplotlib.pyplot as plt
import numpy as np

"""
Function displays a plot of the points along with the connections between the points (distances).
Structure adapted from https://github.com/chncyhn/simulated-annealing-tsp/blob/master/visualize_tsp.py, 
modified by Timothy Lindblom.

:param paths: List of lists with the different orders in which the nodes are visited
:param points: coordinates for the different nodes
:return: Smaller data set from the smallest circle.
"""

def plotTSP(paths, points):

    # Unpack the primary TSP path and transform it into a list of ordered
    # coordinates
    x = []; y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    # Set scale for arrow heads
    a_scale = float(max(x))/float(100)
    x_origin = 17.143144
    y_origin = 60.6747821

    #coordinates of stadshuset in Gävle
    circle00 = plt.Circle((17.143144,60.6747821), a_scale*.05, color="r", fill = False)
    circle0 = plt.Circle((17.143144,60.6747821), a_scale*.15, color="r", fill = False)
    circle1 = plt.Circle((17.143144,60.6747821), a_scale*.25, color="r", fill = False)
    circle2 = plt.Circle((17.143144,60.6747821), a_scale*.4, color="r", fill = False)
    #radius 4.826304596079909 km
    circle3 = plt.Circle((17.143144,60.6747821), a_scale*.5, color="r", fill = False) 
    #radius 9.652609192160607 km
    ax = plt.gca()
    
    ax.add_patch(circle00)
    ax.add_patch(circle0)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)
    ax.plot(zorder=5)
    ax.plot(x, y, 'co', zorder=0)
    ax.set_title("Coordinates in Gävle and around Gävle town hall")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    #ax.set_aspect('equal')
    ax.autoscale(enable=True, axis='both')
    ax.plot()
    plt.show()
    '''
    Can be made into a separate function.
    '''
    # How many points were inside the circles?
    # Radius scaling factor:
    #print(str(a_scale))

    def points_inside(scaling_factor):
        counter = 0
        for i in range(len(x)):
        #Equation of the circle, if less than the radius then inside the circle.
            if((x[i]-x_origin)**2 + (y[i]-y_origin)**2 < (a_scale*scaling_factor)**2): 
                counter += 1
        print("Number of points inside the circle are: " + str(counter) +". ") 
        print("Giving a proportion of " + str(counter*100/len(x)) + " %.\n")

    points_inside(.05)
    points_inside(.15)
    points_inside(.25)
    points_inside(.4)
    points_inside(.5)


    def coords_points_inside(scaling_factor):
        coords_new = []
        coordinate = []
        for i in range(len(x)):
        #Equation of the circle, if less than the radius then inside the circle.
            if((x[i]-x_origin)**2 + (y[i]-y_origin)**2 < (a_scale*scaling_factor)**2): 
                coordinate = [x[i], y[i]]
                coords_new.append(coordinate)

        coords_new = np.asarray(coords_new)
        return coords_new
    
    coords_new = coords_points_inside(.05)
    return coords_new