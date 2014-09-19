
from M2 import *
from M2_help import *
import time
import matplotlib.pyplot as plt

n = range(10, 1000, 10)
m = 5
norm = []
fast = []
for i in n:
    g = upa_graph(i, m)
    starttime = time.clock()
    targeted_order(g)
    endtime = time.clock()
    norm.append(endtime-starttime)
    starttime = time.clock()
    fast_targeted_order(g)
    endtime = time.clock()
    fast.append(endtime-starttime)
# print norm
# print fast

plt.plot(n, norm, '-r', label='Targeted_Order')
plt.plot(n, fast, '-b', label='Fast_Targeted_Order')
plt.legend(loc='upper left')
plt.xlabel('Number of nodes in graph')
plt.ylabel('The running times')
plt.title('The comparing the running times (desktop Python)')
plt.show()