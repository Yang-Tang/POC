from M2_help import *
from M2 import *
import matplotlib.pyplot as plt

print 'Creating ld graph...'
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
ldg = load_graph(NETWORK_URL)
print 'Nodes: ', len(ldg)
print 'Edges:', edges(ldg)
ld = compute_resilience(ldg, fast_targeted_order(ldg))
print ld
 
print 'Creating er graph...'
p = 3112/float(1347*1346/2)
erg = er_graph2(1347, p)
print 'Nodes: ', len(erg)
print 'Edges:', edges(erg)
er = compute_resilience(erg, fast_targeted_order(erg))
print er
 
print 'Creating upa graph...'
upag = upa_graph(1347, 2)
print 'Nodes: ', len(upag)
print 'Edges:', edges(upag)
upa = compute_resilience(upag, fast_targeted_order(upag))
print upa

plt.plot(range(1348), ld, '-b', label='Computer network')
plt.plot(range(1348), er, '-r', label='ER graph network (p=%.4f)' %p)
plt.plot(range(1348), upa, '-g', label='UPA graph network (m=2)')
line = plt.Polygon([[0,1347*0.75],[1347*0.2,1374*0.8*0.75],[1347*0.2,1374*0.8*1.25],[0,1347*1.25]], color='y', alpha=0.5, label='First 20% resilient range')
plt.gca().add_patch(line)
plt.ylim(0, 1800)
plt.legend(loc='upper right')
plt.xlabel('Number of nodes disconnected')
plt.ylabel('The size of the largest connect component')
plt.title('Network resilience under a targeted attack')
plt.show()