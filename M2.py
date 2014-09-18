"""
blabla
"""

from collections import deque
import random

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
        if n % 20 == 0:
            print 100*n/l, '%'
        ugraph = rm_node(ugraph, node)
        #ugraph = tmp.delete_node(ugraph, node)
        lst.append(largest_cc_size(ugraph))
        #print ugraph
    return lst

def er_graph(n, p):
    g = {}
    v = range(n)
    for i in v:
        g[i] = set([])
    for i in v:
        for j in v:
            if i <> j and not j in g[i]:
                a = random.random()
                if a < p:
                    g[i] |= set([j])
                    g[j] |= set([i])
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

import tmp
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
ldg = tmp.load_graph(NETWORK_URL)

print 'Creating er graph...'
erg = er_graph(10, 0.5)

print 'Creating upa graph...'
upag = upa_graph(1000, 10)

g = upag

print 'caculating...'
print compute_resilience(g, random_order(g))
#print g
