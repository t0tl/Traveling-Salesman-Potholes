import numpy as np
import json


def logscore(T, V, X):
    """Function for calculating the score of a knapsack.
    Args:
        T (float): "temperature" of the system
        V (int): integer vector with all values
        X (int): boolean vector for the knapsack (whether the item is included or not)
    Returns:
        double: log score of the knapsack
    """
    return np.dot(V, X)/T


def proposal_gen(X, W, W_max):
    """Function which generates the proposal knapsack
    
    Function which generates the proposal knapsack,
    which is to be evaluted against the current knapsack.
    Args:
        X (int): boolean vector for the knapsack (whether the item is included or not)
        W (int): integer vector with all weights
        W_max (int): maximum weight allowed in the knapsack
    Returns:
        int: vector called proposal_state
    """

    new_index = np.random.randint(0, len(W)-1)
    proposal_state = list(X)
    proposal_state[new_index] = 1- proposal_state[new_index] #Changes bool to include item from 0 to 1 or 1 to 0

    if np.dot(proposal_state, W) <= W_max:
        return proposal_state

    else:
        return proposal_gen(X, W, W_max)



def main_evaluator(a, i, X, W, W_max, V, T):
    """Evaluation function.
    
    Determines whether the knapsack should change or not.
    Includes item if it leads to a better solution or
    uniform probability is less than acceptance probability.
    Args:
        a (float): geometric cooling parameter
        i (int): length of markov chain
        X (int): boolean vector for the knapsack (whether the item is included or not)
        W (int): integer vector with all weights
        W_max (int): maximum weight allowed in the knapsack
        V (int): integer vector with all values
        T (float): "temperature" of the system
    Returns:
        int int: vector representing a state along with its temperature.
    """

    best_state=[]

    for i in range(i):
        proposed_X = proposal_gen(X, W, W_max)
        proposed_score = logscore(T, V, proposed_X)
        current_score = logscore(T, V, X)
        acceptance_probability = min(np.exp(proposed_score-current_score), 1)
        if (acceptance_probability == 1):
            X = proposed_X
            best_state = X
        elif (acceptance_probability < 1 and acceptance_probability > 0):
            unif_prob = np.random.randint(0,1)
            if (unif_prob <= acceptance_probability):
                X = proposed_X
                best_state = X
        else:
            T = a*T
            return X, T
    T = a*T
    
    return best_state, T

### Main, containing outer loop for the stopping criterion.
### Specifies hyperparameters for the method.
### Initializes vectors.

#Import weight and value values from json files
with open('value.json') as json_value:
    V = json.load(json_value)
with open("weight.json") as json_weight:
    W = json.load(json_weight)

#Specify desired maximum weight.
W_max = 1500

#Specify hyperparameters.
T = 500
a = .95
i = 10000

#Initialise best state tracker and starting state.
max_state_value = 0
solution_MCMC = [0]
best_state_value_list = []
starting_state = [0]*len(W)
best_state = starting_state

#Run simulated annealing until temperature has cooled sufficiently.
while(T>.01):
    best_state, T = main_evaluator(a, i, best_state, W, W_max, V, T)
    state_value = np.dot(best_state, V)
    if state_value > max_state_value:
        max_state_value = state_value
        solution_MCMC = best_state

#Display solution.
print("Simple simulated annealing solution is :", str(solution_MCMC), "with Value:", str(max_state_value))