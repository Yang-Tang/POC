"""
blabla
"""

EX_GRAPH0 = {0:set([1,2]),
             1:set([]),
             2:set([])}

EX_GRAPH1 = {0:set([1,4,5]),
             1:set([2,6]),
             2:set([3]),
             3:set([0]),
             4:set([1]),
             5:set([2]),
             6:set([])}

EX_GRAPH2 = {0:set([1,4,5]),
             1:set([2,6]),
             2:set([3,7]),
             3:set([7]),
             4:set([1]),
             5:set([2]),
             6:set([]),
             7:set([3]),
             8:set([1,2]),
             9:set([0,3,4,5,6,7])}

def make_complete_graph(num_nodes):
    """
    blabla
    """
    dic = {}
    all_nudes = set(range(num_nodes))
    for node in range(num_nodes):
        dic[node] = all_nudes - set([node])
    return dic

def compute_in_degrees(digraph):
    """
    blabla
    """
    dic = {}
    for node in digraph:
        dic[node] = 0
    for node in digraph:
        for target in digraph[node]:
            dic[target] = dic.get(target, 0) + 1
    return dic

def in_degree_distribution(digraph):
    """
    blabla
    """
    dic = {}
    for node in digraph:
        dic[node] = 0
    for node in digraph:
        for target in digraph[node]:
            dic[target] = dic.get(target, 0) + 1
    dic1 = {}
    for node in dic:
        dic1[dic[node]] = dic1.get(dic[node],0) + 1
    return dic1

