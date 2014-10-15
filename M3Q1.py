import random
import time
import matplotlib.pyplot as plt
import alg_cluster
from M3 import *
from IPython.html.services import clusters

def gen_random_clusters(num_clusters):
    cluster_list = []
    for dummy_idx in range(num_clusters):
        cluster = alg_cluster.Cluster(set(), random.uniform(-1, 1), random.uniform(-1, 1), 0, 0)
        cluster_list.append(cluster)
    return cluster_list


slow_time = []
fast_time = []
for n in range(2, 201):
    cluster_list = gen_random_clusters(n)
    
    start = time.clock()
    slow_closest_pairs(cluster_list)
    end = time.clock()
    slow_time.append(end-start)
    
    start = time.clock()
    fast_closest_pair(cluster_list)
    end = time.clock()
    fast_time.append(end-start)

plt.plot(range(2, 201), slow_time, '-r', label='slow_closest_pairs')
plt.plot(range(2, 201), fast_time, '-b', label='fast_closest_pair')
plt.legend(loc='upper left')
plt.xlabel('Size of cluster list')
plt.ylabel('The running times')
plt.title('The comparing the running times (desktop Python)')
plt.show()