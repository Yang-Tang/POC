"""
blabla
"""

from collections import deque
import random
import itertools


class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def bfs_visited(ugraph, start_node):
    """
    blabla
    """
    que = deque()
    visitied = set([start_node])
    que.append(start_node)
    while len(que) > 0:
        elem = que.popleft()
        neighbors = ugraph[elem]
        for node in neighbors:
            if not node in visitied:
                visitied |= set([node])
                que.append(node)
    return visitied

def cc_visited(ugraph):
    """
    bla
    """
    remainingnodes = set(ugraph.keys())
    cc_lst = []
    while len(remainingnodes) > 0:
        node = remainingnodes.pop()
        c_comp = bfs_visited(ugraph, node)
        cc_lst.append(c_comp)
        remainingnodes -= c_comp
    return cc_lst

def largest_cc_size(ugraph):
    """
    bla
    """
    try:
        return max(map(len, cc_visited(ugraph)))
    except ValueError:
        return 0
    
def rm_node(ugraph, node):
    """
    bla
    """
    neighbors = ugraph.get(node)
    if neighbors:
        for item in neighbors:
            ugraph[item] -= set([node])
    ugraph.pop(node)
    return ugraph

def compute_resilience(ugraph, attack_order):
    """
    bla
    """
    lst = [largest_cc_size(ugraph)]
    n = -1
    l = len(ugraph)
    for node in attack_order:
        #print 'rm: ', node
        n += 1
        if n % 100 == 0:
            print 100*n/l, '%',
        ugraph = rm_node(ugraph, node)
        #ugraph = M2_help.delete_node(ugraph, node)
        lst.append(largest_cc_size(ugraph))
        #print ugraph
    print '\n'
    return lst

def er_graph(n, p):
    g = {}
    v = range(n)
    for i in v:
        g[i] = set([])
    for i in v:
        for j in v:
#             if i <> j and not j in g[i]:
            if i <> j :
                a = random.random()
                if a < p:
                    g[i] |= set([j])
                    g[j] |= set([i])
    return g

def er_graph2(n, p):
    g = {}
    for i in range(n):
        g[i] = set()
    v = itertools.combinations(range(n), 2)
    for edge in v:
        a = random.random()
        if a < p:
            g[edge[0]].add(edge[1])
            g[edge[1]].add(edge[0])
    return g

def make_complete_graph(num_nodes):
    """
    blabla
    """
    dic = {}
    all_nudes = set(range(num_nodes))
    for node in range(num_nodes):
        dic[node] = all_nudes - set([node])
    return dic

def upa_graph(n, m):
    g = make_complete_graph(m)
    t = UPATrial(m)
    for i in range(m, n):
        neighbors = t.run_trial(m)
        g[i] = set(neighbors)
        for node in neighbors:
            g[node].add(i)
    return g

def random_order(ugraph):
    lst = ugraph.keys()
    random.shuffle(lst)
    return lst

def edges(ugraph):
    n = 0
    for nodes in ugraph.values():
        n += len(nodes)
    return n/2

def fast_targeted_order(ugraph):
    degreesets = {}
    for degree in range(len(ugraph)):
        degreesets[degree] = set()
    for node in ugraph:
        degree = len(ugraph[node])
        degreesets[degree].add(node)
    lst = []
    i = 0
    for degree in range(len(ugraph)-1, -1, -1):
        while len(degreesets[degree]) > 0:
            node = degreesets[degree].pop()
            for neighber in ugraph[node]:
                nb_deg = len(ugraph[neighber])
                degreesets[nb_deg].remove(neighber)
                degreesets[nb_deg - 1].add(neighber)
            lst.append(node)
            i += 1
            ugraph = rm_node(ugraph, node)
    return lst


# print 'Creating ld graph...'

# # NETWORK_URL = "alg_rf7.txt"
# NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
# ldg = M2_help.load_graph(NETWORK_URL)
# print 'Nodes: ', len(ldg)
# print 'Edges:', edges(ldg)
# ld = compute_resilience(ldg, random_order(ldg))
# print ld
# 
# print 'Creating er graph...'
# p = 3112/float(1347*1346/2)
# erg = er_graph2(1347, p)
# print 'Nodes: ', len(erg)
# print 'Edges:', edges(erg)
# er = compute_resilience(erg, random_order(erg))
# print er
# 
# print 'Creating upa graph...'
# upag = upa_graph(1347, 2)
# print 'Nodes: ', len(upag)
# print 'Edges:', edges(upag)
# upa = compute_resilience(upag, random_order(upag))
# print upa


# import matplotlib.pyplot as plt
# def legend_example():
#     """
#     Plot an example with two curves with legends
#     """
#     nodes_removed = range(1348)
#     y1 = ld
#     y2 = er
#     y3 = upa
# #     up = map(lambda x: (1347-x)*1.25, nodes_removed)
# #     down = map(lambda x: (1347-x)*0.75, nodes_removed)
# 
#     plt.plot(nodes_removed, y1, '-b', label='Computer network')
#     plt.plot(nodes_removed, y2, '-r', label='ER graph network (p=%.4f)' %p)
#     plt.plot(nodes_removed, y3, '-g', label='UPA graph network (m=2)')
# #     plt.plot(nodes_removed, up, '-y', label='up')
# #     plt.plot(nodes_removed, down, '-y', label='down')
# #     plt.plot((0.2*1347,0.2*1347), (0,1800))
#     line = plt.Polygon([[0,1347*0.75],[1347*0.2,1374*0.8*0.75],[1347*0.2,1374*0.8*1.25],[0,1347*1.25]], color='y', alpha=0.5, label='First 20% resilient range')
#     plt.gca().add_patch(line)
#     plt.ylim(0, 1800)
#     plt.legend(loc='upper right')
#     plt.xlabel('Number of nodes disconnected')
#     plt.ylabel('The size of the largest connect component')
#     plt.title('Network resilience under an attack')
#     plt.show()
# 
# legend_example()
