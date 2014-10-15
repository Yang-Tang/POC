"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster



def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    dist = float('inf')
    idx1 = -1
    idx2 = -1
    min_dist_set = set([(dist, idx1, idx2)])
    num = len(cluster_list)
    for idx1 in range(num):
        for idx2 in range(num):
            if idx1 <> idx2:
                new_dist = pair_distance(cluster_list, idx1, idx2)
                if round(new_dist[0], 8) == round(dist, 8):
                    min_dist_set.add(new_dist)
                elif round(new_dist[0], 8) < round(dist, 8):
                    dist = new_dist[0]
                    min_dist_set = set([new_dist])
    return min_dist_set


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper_base(cluster_list, horiz_order, vert_order):
        """
        base case
        """
        dist = float('inf')
        idx1 = -1
        idx2 = -1
        min_dist = (dist, idx1, idx2)
        for idx1 in horiz_order:
            for idx2 in horiz_order:
                if idx1 <> idx2:
                    new_dist = pair_distance(cluster_list, idx1, idx2)
                    if new_dist[0] < dist:
                        dist = new_dist[0]
                        min_dist = new_dist
        return min_dist
    
    def fast_helper_divide(cluster_list, horiz_order, vert_order):
        """
        divide
        """
        num = len(horiz_order)
        half = num/2
        m_1_idx = horiz_order[half-1]
        m_idx = horiz_order[half]
        mid = (cluster_list[m_1_idx].horiz_center() + cluster_list[m_idx].horiz_center())/2.0
        horiz_order_left = horiz_order[:half]
        horiz_order_right = horiz_order[half:]
        vert_order_left = []
        vert_order_right = []
        for idx in vert_order:
            if idx in set(horiz_order_left):
                vert_order_left.append(idx)
            elif idx in set(horiz_order_right):
                vert_order_right.append(idx)
        return (horiz_order_left, vert_order_left, horiz_order_right, vert_order_right, mid)
    
    
    def fast_helper_merge(cluster_list, horiz_order, vert_order, answer, mid):
        """
        merge
        """
        horiz_order_mid = []
        for idx in horiz_order:
            if cluster_list[idx].horiz_center() > mid + answer[0]:
                break
            if cluster_list[idx].horiz_center() > mid - answer[0]:
                horiz_order_mid.append(idx)
        vert_order_mid = []
        for idx in vert_order:
            if idx in set(horiz_order_mid):
                vert_order_mid.append(idx)
        mid_num = len(vert_order_mid)
        for idx1 in range(mid_num - 1):
            for idx2 in range(idx1 + 1, min(idx1 + 4, mid_num)):
                new_answer = pair_distance(cluster_list, vert_order_mid[idx1], vert_order_mid[idx2])
                answer = min(answer, new_answer)
        return answer
    
    
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        num = len(horiz_order)
        if num <= 3:
            return (fast_helper_base(cluster_list, horiz_order, vert_order))
        divide = fast_helper_divide(cluster_list, horiz_order, vert_order)
        answer_left = fast_helper(cluster_list, divide[0], divide[1])
        answer_right = fast_helper(cluster_list, divide[2], divide[3])
        answer = min([answer_left, answer_right])
        return fast_helper_merge(cluster_list, horiz_order, vert_order, answer, divide[4])
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
#     return (answer[0], min(answer[1:]), max(answer[1:]))
    return answer

    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        if len(cluster_list) % 10 == 0:
            print len(cluster_list),
        closest_pair_idx = fast_closest_pair(cluster_list)[1:]
        merged_cluster = cluster_list[closest_pair_idx[0]].merge_clusters(cluster_list[closest_pair_idx[1]])
        cluster_list.append(merged_cluster)
        cluster_list.pop(closest_pair_idx[0])
        cluster_list.pop(closest_pair_idx[1] - 1)
    return cluster_list



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # initialize k-means clusters to be initial clusters with largest populations
    population_and_cluster = [(cluster_list[idx].total_population(), cluster_list[idx]) 
                        for idx in range(len(cluster_list))]
    population_and_cluster.sort(reverse=True)
    k_cluster = [population_and_cluster[idx][1] for idx in range(num_clusters)]
    num = len(cluster_list)
    for dummy_idx in range(num_iterations):
        cluster_list_plus = cluster_list + k_cluster
        k_cluster = []
        for idx in range(num_clusters):
            k_cluster.append(alg_cluster.Cluster(set(), 0, 0, 0, 0))
        for idx in range(num):
            k_dist = []
            for k_cluster_idx in range(num_clusters):
                dist = pair_distance(cluster_list_plus, idx, k_cluster_idx + num)[0]
                k_dist.append((dist, k_cluster_idx))
            k_cluster_idx = min(k_dist)[1]
            k_cluster[k_cluster_idx] = cluster_list[idx].copy().merge_clusters(k_cluster[k_cluster_idx])
    return k_cluster
