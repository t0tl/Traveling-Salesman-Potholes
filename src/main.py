from prog import Coordinate, read_json_coords, get_total_distance_two_opt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import random
import visualize_tsp
from MLE import get_expected_value

'''
Main program for Simulated Annealing and Nearest Neighbour algorithm by Timothy Lindblom. 
Includes adjustment of flight distance to road distance.
'''

if __name__ == "__main__":
    dataset = input("Enter small or complete: ")
    data = read_json_coords("pothallref.json")
    expected_value = get_expected_value()
    expected_value = 1
    print(f"Expected value:  {expected_value}\n")

    # Plot points
    nodes = [i for i in range(len(data))]
    coords_new = visualize_tsp.plotTSP([nodes], data)
    if (dataset == "small"):

        N = len(coords_new)
        fitness_list = []

        """
        Nearest neighbour algorithm
        """
        nodes = [i for i in range(len(coords_new))]

        cur_node = random.choice(nodes)  # start from a random node
        solution = [cur_node] #set solution to selected random node

        free_nodes = set(nodes) #removes duplicates, saves nodes as set.
        free_nodes.remove(cur_node) #remove current node.
        while free_nodes: #while we have remaining nodes. 
            next_node = min(free_nodes, key=lambda x: Coordinate.get_distance_NNA(cur_node, x, coords_new, expected_value))  # Take the neighbour with smallest distance
            free_nodes.remove(next_node) #Remove the closest node from the list
            solution.append(next_node) #Append the closest node to solution
            cur_node = next_node #Check for the closest node from the latest node
        cur_fit = Coordinate.get_total_distance_NNA(coords_new, solution, expected_value) #Calculate total distance.
        fitness_list.append(cur_fit) #Add total distance to list of total distances.
        best_fit = cur_fit

        #Plot Nearest Neighbour solution
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.title.set_text('Nearest neighbour')
        ax2.title.set_text('Simulated annealing')
        ax1.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        new_coords = []
        for i in solution:
            new_coords.append(coords_new[solution[i]])
        for first, second in zip(new_coords[:-1], new_coords[1:]):
            ax1.plot([first[0], second[0]], [first[1], second[1]], 'b')
        ax1.plot([new_coords[0][0], new_coords[-1][0]], [new_coords[0][1], new_coords[-1][1]], 'b')
        for c in new_coords:
            ax1.plot(c[0], c[1], 'ro')


        '''
        Simulated annealing with random two edges swapped.
        '''
        new_coords = [i for i in range(N)]
        solution = np.asarray(solution)
        for i in solution:
            new_coords[i] = coords_new[nodes[i]]
        new_coords = np.asarray(new_coords)
        cost0 = get_total_distance_two_opt(new_coords, solution, expected_value)
        T = 1
        factor = .99
        i = 0
        while(T>1*10**(-5)):
            print(i, 'cost =', cost0)

            T = T*factor
            for j in range(500):
                #Swap two coordinates.
                r1, r2 = np.random.randint(0, N-1, size=2)

                temp = solution[r1]
                solution[r1] = solution[r2]
                solution[r2] = temp
                if r1 - r2 < 0:
                    new_coords[r2:r1] = new_coords[r2:r1][::-1]
                else:
                    new_coords[r1:r2] = new_coords[r1:r2][::-1]

                cost1 = get_total_distance_two_opt(new_coords, solution, expected_value)
                if cost1 < cost0:
                    cost0 = cost1
                else:
                    if np.random.uniform() > np.exp((cost1-cost0)/T):
                        cost0 = cost1
                    else:
                        temp = solution[r1]
                        solution[r1] = solution[r2]
                        solution[r2] = temp
            if (cost0 < best_fit):
                best_fit = cost0
            fitness_list.append(cost0)
            i+=1

        #Plot SA solution
        for i in solution:
            new_coords[i] = coords_new[solution[i]]
        for first, second in zip(new_coords[:-1], new_coords[1:]):
            ax2.plot([first[0], second[0]], [first[1], second[1]], 'b')
        ax2.plot([new_coords[0][0], new_coords[-1][0]], [new_coords[0][1], new_coords[-1][1]], 'b')
        for c in new_coords:
            ax2.plot(c[0], c[1], 'ro')
        plt.show()    
    
    else:
        N = len(data)
        data = np.asarray(data)
        fitness_list = []

        coords = []
        for i in range(N): # You set the number here
            coords.append(Coordinate(data[i][0], data[i][1]))

        """
        Nearest neighbour algorithm
        """

        cur_node = random.choice(nodes)  # start from a random node
        solution = [cur_node] #set solution to selected random node

        free_nodes = set(nodes) #removes duplicates, saves nodes as set.
        free_nodes.remove(cur_node) #remove current node.
        while free_nodes: #while we have remaining nodes. 
            next_node = min(free_nodes, key=lambda x: Coordinate.get_distance_NNA(cur_node, x, data, expected_value))  # Take the neighbour with smallest distance
            free_nodes.remove(next_node) #Remove the closest node from the list
            solution.append(next_node) #Append the closest node to solution
            cur_node = next_node #Check for the closest node from the latest node
        cur_fit = Coordinate.get_total_distance_NNA(data, solution, expected_value) #Calculate total distance.
        fitness_list.append(cur_fit) #Add total distance to list of total distances.
        best_fit = cur_fit
        
        #Plot nearest neighbour solution
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.title.set_text('Nearest neighbour')
        ax2.title.set_text('Simulated annealing')

        new_coords = []
        for i in solution:
            new_coords.append(data[solution[i]])
        for first, second in zip(new_coords[:-1], new_coords[1:]):
            ax1.plot([first[0], second[0]], [first[1], second[1]], 'b')
        ax1.plot([new_coords[0][0], new_coords[-1][0]], [new_coords[0][1], new_coords[-1][1]], 'b')
        for c in new_coords:
            ax1.plot(c[0], c[1], 'ro')

        '''
        Simulated annealing with random two edges swapped.
        '''        
        new_coords = [i for i in range(N)]
        for i in solution:
            new_coords[i] = data[nodes[i]]
        solution = np.asarray(solution)
        new_coords = np.asarray(new_coords)

        cost0 = get_total_distance_two_opt(new_coords, solution, expected_value)
        T = 1
        factor = .99
        i = 0
        while(T>1*10**(-5)):
            print(i, 'cost =', cost0)

            T = T*factor
            for j in range(500):
                #Exchange two coordinates.
                r1, r2 = np.random.randint(0, N, size = 2)
                temp = solution[r1]
                solution[r1] = solution[r2]
                solution[r2] = temp
                if r1 - r2 < 0:
                    solution[r2:r1] = solution[r2:r1][::-1]
                else:
                    solution[r1:r2] = solution[r1:r2][::-1]

                cost1 = get_total_distance_two_opt(new_coords, solution, expected_value)
                if cost1 < cost0:
                    cost0 = cost1
                else:
                    if np.random.uniform() > np.exp((cost1-cost0)/T):
                        cost0 = cost1
                    else:    
                        temp = solution[r1]
                        solution[r1] = solution[r2]
                        solution[r2] = temp
            if (cost0 < best_fit):
                best_fit = cost0
            fitness_list.append(cost0)
            i+=1
        
        # Plot the SA solution
        for i in solution:
            new_coords[i] = data[solution[i]]
        for first, second in zip(new_coords[:-1], new_coords[1:]):
            ax2.plot([first[0], second[0]], [first[1], second[1]], 'b')
        ax2.plot([new_coords[0][0], new_coords[-1][0]], [new_coords[0][1], new_coords[-1][1]], 'b')
        for c in new_coords:
            ax2.plot(c[0], c[1], 'ro')
        plt.show()  

    #Comparison
    print("Best fitness obtained: ", best_fit)
    improvement = 100 * (fitness_list[0] - best_fit) / (fitness_list[0])
    print(f"Improvement over greedy heuristic: {improvement : .3f}%")

    # Plot fitness development
    plt.plot([i for i in range(len(fitness_list))], fitness_list)
    plt.ylabel("Fitness")
    plt.xlabel("Iteration")
    plt.show()
    

