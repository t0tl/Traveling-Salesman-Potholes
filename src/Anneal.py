import math
import random
import visualize_tsp
import matplotlib.pyplot as plt
from Haversine import haversine
'''
Class adopted from https://github.com/chncyhn/simulated-annealing-tsp/blob/master/anneal.py, 
with heavy modifications by Timothy Lindblom and addition of using the Haversine formula for finding the great circle distance.
'''
class Anneal(object):
    def __init__(self, coords, T, alpha, stopping_T):
        self.coords = coords
        self.N = len(coords)
        self.T = T
        self.T_save = self.T  # save inital T to reset if batch annealing is used
        self.alpha = alpha
        self.stopping_temperature = stopping_T

        self.nodes = [i for i in range(self.N)]

        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []

    def nearest_neighbour(self):
        """
        Nearest neighbour algorithm to get an initial solution.
        """
        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node] #set solution to selected random node

        free_nodes = set(self.nodes) #removes duplicates, saves nodes as set.
        free_nodes.remove(cur_node) #remove current node.
        while free_nodes: #while we have remaining nodes. 
            next_node = min(free_nodes, key=lambda x: self.dist(cur_node, x))  # nearest neighbour (minimize the distance between free_nodes.)
            free_nodes.remove(next_node) #Remove the closest node from the list
            solution.append(next_node) #Append the closest node to solution
            cur_node = next_node #Check for the closest node from the latest node

        cur_fit = self.fitness(solution) #Calculate total distance.
        if cur_fit < self.best_fitness:  #If best found so far, update best fitness
            self.best_fitness = cur_fit #Least distance is the current distance.
            self.best_solution = solution #Best solution is current solution
        self.fitness_list.append(cur_fit) #Add total distance to list of total distances.
        return solution, cur_fit #return the solution and the total distance for the solution.

    def dist(self, node_0, node_1):
        """
        Distance in kilometers between two nodes using the Haversine formula.
        """
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1] #Take in each coordinate.
        return haversine(coord_0[1], coord_0[0], coord_1[1], coord_1[0]) #Return distance between points in kilometers.

    def fitness(self, solution):
        """
        Total distance of the current solution path.
        """
        cur_fit = 0 #Start with zero distance.
        for i in range(self.N):
            cur_fit += self.dist(solution[i % self.N], solution[(i + 1) % self.N]) #Sum distance between all nodes in solution.
        return cur_fit #return total distance of solution.

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T) #Metropolis criterion.

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty p_accept() if candidate is worse.
        """
        candidate_fitness = self.fitness(candidate) #Calculate total distance for candidate
        if candidate_fitness < self.cur_fitness: #If candidate solution is a better solution
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate #Accept candidate
            if candidate_fitness < self.best_fitness: #If candidate solution was also the best solution seen, 
                self.best_fitness, self.best_solution = candidate_fitness, candidate #make best solution.
        else: #Otherwise
            if random.random() < self.p_accept(candidate_fitness): #If sample from [0,1) uniform distribution is less than metropolis criterion.
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate #Accept the worse candidate solution.

    def anneal(self):
        """
        Execute simulated annealing algorithm.
        """
        # Initialize with the greedy solution.
        self.cur_solution, self.cur_fitness = self.nearest_neighbour() 

        print("Starting annealing.")
        while self.T > self.stopping_temperature: #Meanwhile T > stopping T.
            candidate = list(self.cur_solution) #Turn set into list.
            l = random.randint(2, self.N - 1) #Choose random int between 2 and N-1, including both
            i = random.randint(0, self.N - l) #Choose random int between 0 and N-1, including both
            candidate[i : (i + l)] = reversed(candidate[i : (i + l)]) #Reverse list between index [i and i+l].
            self.accept(candidate) #Accept or reject candidate.
            self.T *= self.alpha #multiply T by alpha

            self.fitness_list.append(self.cur_fitness) #Append current_fitness list to fitness_lists.

        print("Best fitness obtained: ", self.best_fitness)
        improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
        print(f"Improvement over greedy heuristic: {improvement : .2f}%")

    def batch_anneal(self, times=1):
        """
        Execute simulated annealing algorithm `times` times, with random initial solutions.
        """
        for i in range(1, times + 1): #For 1 to times.
            print(f"Iteration {i}/{times} -------------------------------") #Print iteration out of times.
            self.T = self.T_save # T = T-saved
            self.cur_solution, self.cur_fitness = self.nearest_neighbour() #Run NNA heuristic
            self.anneal() #Run SA.

    def visualize_routes(self):
        """
        Visualize the TSP route with matplotlib.
        """
        visualize_tsp.plotTSP([self.best_solution], self.coords)

    def plot_fitness(self):
        """
        Plot the fitness through iterations.
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel("Fitness")
        plt.xlabel("Iteration")
        plt.show()
