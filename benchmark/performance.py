import random

import numpy as np
import matplotlib.pyplot as plt
from tracknaliser.clustering import cluster
from tracknaliser.clustering_numpy import cluster_numpy
import datetime


def samples(n):
    data=[]
    for _ in range(n):
        data.append([random.uniform(0,10),random.uniform(0,10),random.uniform(0,10)])
    return data


x = np.arange(100, 10000, 100,dtype=int)
y = []
z = []

for i in x:
    cf = samples(i)
    start = datetime.datetime.now()
    cluster(cf,10,3,False)
    finish = datetime.datetime.now()
    z.append((finish - start).total_seconds())

for i in x:
    cf = np.array(samples(i))
    begin = datetime.datetime.now()
    cluster_numpy(cf,10,3,False)
    end = datetime.datetime.now()
    y.append((end - begin).total_seconds())

plt.plot(x, y, label='Clustering function with numpy')
plt.plot(x, z, label='Clustering function without numpy')
plt.xlabel('Sample size')
plt.ylabel('Time taken (s)')
plt.title('Performance')
plt.legend()
plt.yscale("log")
plt.savefig("./benchmark/performance.png")
