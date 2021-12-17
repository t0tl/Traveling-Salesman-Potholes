from Haversine import haversine
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
'''
Performs data exploration for the samples from the road data to determine 
the pdf the the ratio of road and flight distance. Thereafter tries to fit a Pareto type-1 distribution using 
maximum likelihood estimation and also another proposed MVUE estimator. Made by Timothy Lindblom
'''

if (__name__ == "__main__"):
    sample = [[17.1371, 60.6621], [17.1461, 60.7114], [17.1464, 60.6495], [17.1051, 60.6876], [17.1096, 60.6876], [17.1601, 60.6804], [17.1612, 60.6524], [17.2562, 60.6756], [17.1474, 60.6703], [17.1604, 60.7068], [17.1468, 60.6934], [17.1647, 60.7165], [16.9767, 60.6439], [17.172, 60.6743], [17.1592, 60.6705], [17.1352, 60.6746], [17.2469, 60.6862], [17.0183, 60.6493], [17.1479, 60.6708], [17.1091, 60.686], [17.1433, 60.6656], [17.1467, 60.6762], [17.146, 60.7114], [17.1722, 60.6749], [17.2559, 60.6748], [17.1668, 60.7014], [17.1643, 60.7034], [17.2006, 60.6715], [17.1452, 60.6892], [17.1574, 60.675], [17.1843, 60.6586]]
	
    dist = []
    
    k=1
    for j in range(3):
        for i in range(k, len(sample)):
            dist.append(haversine(sample[j][1], sample[j][0], sample[i][1], sample[i][0]))
        k +=1
    for i in range(3, len(sample)-1):
	    dist.append(haversine(sample[i][1], sample[i][0], sample[i+1][1], sample[i+1][0]))

    dist = pd.DataFrame(dist)
    dist.columns = ["Flight"]
    road_dist = pd.read_excel("road.xlsx", usecols=[0])
    both = pd.concat([road_dist, dist], axis=1)
    both["Prop"] = both["Road"]/both["Flight"]	
    plt.scatter(both["Prop"], both["Flight"])
    plt.xlabel("Road distance divided by flight distance")
    plt.ylabel("Flight distance")
    plt.show()
	

    #betaMLE = min(both["Prop"])
    betaMLE = 1
    n = len(both["Prop"])
    print(n)
    sum = np.sum(np.log(both["Prop"]))
    alphaMLE = n/(sum-n*np.log(betaMLE))
    alphaMVUE = (n-1)/(sum-n*np.log(betaMLE))
    print(alphaMLE/(alphaMLE-1))
    print(betaMLE, alphaMLE, alphaMVUE)
    x = np.linspace(stats.pareto.ppf(0.01, alphaMLE), stats.pareto.ppf(0.99, alphaMLE), 100)
    plt.plot(x, stats.pareto.pdf(x, alphaMLE),'r-', lw=5, alpha=0.6, label='pareto pdf')
    plt.hist(both["Prop"], density=True, histtype='stepfilled', alpha=0.2)
    plt.xlabel("Road distance divided by flight distance")
    plt.ylabel("Density")
    plt.show()

    stats.probplot(both["Prop"], dist='pareto', sparams=(alphaMLE, betaMLE), plot=plt)
    plt.show()
    
    
    #np.random.pareto()
def get_expected_value():
    sample = [[17.1371, 60.6621], [17.1461, 60.7114], [17.1464, 60.6495], [17.1051, 60.6876], [17.1096, 60.6876], [17.1601, 60.6804], [17.1612, 60.6524], [17.2562, 60.6756], [17.1474, 60.6703], [17.1604, 60.7068], [17.1468, 60.6934], [17.1647, 60.7165], [16.9767, 60.6439], [17.172, 60.6743], [17.1592, 60.6705], [17.1352, 60.6746], [17.2469, 60.6862], [17.0183, 60.6493], [17.1479, 60.6708], [17.1091, 60.686], [17.1433, 60.6656], [17.1467, 60.6762], [17.146, 60.7114], [17.1722, 60.6749], [17.2559, 60.6748], [17.1668, 60.7014], [17.1643, 60.7034], [17.2006, 60.6715], [17.1452, 60.6892], [17.1574, 60.675], [17.1843, 60.6586]]
    dist = []
    
    k=1
    for j in range(3):
        for i in range(k, len(sample)):
            dist.append(haversine(sample[j][1], sample[j][0], sample[i][1], sample[i][0]))
        k +=1
    for i in range(3, len(sample)-1):
	    dist.append(haversine(sample[i][1], sample[i][0], sample[i+1][1], sample[i+1][0]))

    dist = pd.DataFrame(dist)
    dist.columns = ["Flight"]
    road_dist = pd.read_excel("road.xlsx", usecols=[0])
    both = pd.concat([road_dist, dist], axis=1)
    both["Prop"] = both["Road"]/both["Flight"]	
    betaMLE = 1
    n = len(both["Prop"])
    sum = np.sum(np.log(both["Prop"]))
    alphaMLE = n/(sum-n*np.log(betaMLE))
    return (alphaMLE/(alphaMLE-1))