from testest import Anneal
import matplotlib.pyplot as plt
import random
import json
import pandas as pd
'''
Main script for solving the traveling salesman problem 
using simulated annealing and the nearest neighbour algorithm.
'''


'''
Import coordinates from a .xlsx file.
'''
def read_coords(path):
    data = pd.read_excel(path, sheet_name=0, header=None, usecols=[0,1])
    gps_data = list(zip(data[0].values, data[1].values))        
    return gps_data
'''
Import coordinates from a .json file.
'''
def read_json_coords(path):
    data = json.load(open(path))
    return data
'''
Import coordinates from a .txt file.
'''
def read_txt(path):
    coords = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = [float(x.replace("\n", "")) for x in line.split(" ")]
            coords.append(line)
    return coords
'''
Generate random coordinates to use for the traveling salesman problem.
'''
def generate_random_coords(num_nodes):
    return [[random.uniform(-1000, 1000), random.uniform(-1000, 1000)] for i in range(num_nodes)]


if __name__ == "__main__":
    coords = read_json_coords("pothallref.json") #generate_random_coords(100) #read_coords("pothallref.xlsx")
    sa = Anneal(coords, 1000, 0.5, 0.1) #Create instance of object "Anneal"
    sa.batch_anneal() #Call method batch_anneal
    sa.visualize_routes() #Call method visualize_routes
    sa.plot_fitness() #Call method plot_fitness
