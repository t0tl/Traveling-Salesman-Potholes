import matplotlib.pyplot as plt

"""
Function displays a plot of the points along with the connections between the points (distances).
Adapted from https://github.com/chncyhn/simulated-annealing-tsp/blob/master/visualize_tsp.py

Parameters:
paths: List of lists with the different orders in which the nodes are visited
points: coordinates for the different nodes
num_iters: number of paths that are in the path list

Returns void.
"""

def plotTSP(paths, points, num_iters=1):

    # Unpack the primary TSP path and transform it into a list of ordered
    # coordinates
    x = []; y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    # Set scale for arrow heads
    a_scale = float(max(x))/float(100)
    max_x = max(x)
    max_y = max(y)
    min_x = min(x)
    min_y = min(y)
    # note we must use plt.subplots, not plt.subplot
    # (or if you have an existing figure)
    # fig = plt.gcf()
    # ax = fig.gca()
    midpoint_x = (max_x-min_x)/2+min_x
    midpoint_y = (max_y-min_y)/2+min_y
    circle1 = plt.Circle((17.143144,60.6747821), a_scale*.25, color="r", fill = False) #coordinates of stadshuset in Gävle
    circle2 = plt.Circle((17.143144,60.6747821), a_scale*.5, color="r", fill = False)
    ax = plt.gca()
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.plot(zorder=5)
    ax.plot(x, y, 'co', zorder=10)
    ax.set_aspect('equal')
    ax.autoscale(enable=True, axis='both')
    ax.plot()
    plt.show()
    

    # Draw the primary path for the TSP problem
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale,
            color ='g', length_includes_head=True)
    for i in range(0,len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
                color = 'g', length_includes_head = True)

    #Set axis too slitghtly larger than the set of x and y
    plt.xlim(min(x)*1.1, max(x)*1.1)
    plt.ylim(min(y)*1.1, max(y)*1.1)
    plt.show()