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
    min_dist_set = set((dist, idx1, idx2))
    num = len(cluster_list)
    for idx1 in range(num):
        for idx2 in range(num):
            if idx1 <> idx2:
                new_dist = pair_distance(cluster_list, idx1, idx2)
                if new_dist[0] == dist:
                    min_dist_set.add(new_dist)
                elif new_dist[0] < dist:
                    dist = new_dist[0]
                    min_dist_set = set(new_dist)
    return min_dist_set


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
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
        num = len(cluster_list)
        if num <= 3:
            return slow_closest_pairs(cluster_list)
        half = num/2
        m_1_idx = horiz_order[half-1]
        m_idx = horiz_order[half]
        mid = (cluster_list[m_1_idx].horiz_center() + cluster_list[m_idx].horiz_center())/2.0
        horiz_order_left = horiz_order[:half-1]
        horiz_order_right = horiz_order[half:]
        horiz_order_left_set = set(horiz_order_left)
        horiz_order_right_set = set(horiz_order_right)
        vert_order_left = []
        vert_order_right = []
        cluster_list_left = []
        cluster_list_right = []
        for idx in vert_order:
            if idx in horiz_order_left_set:
                vert_order_left.append(idx)
                cluster_list_left.append(cluster_list[idx])
            elif idx in horiz_order_right_set:
                vert_order_right.append(idx)
                cluster_list_right.append(cluster_list[idx])
        answer_left = fast_helper(cluster_list_left, horiz_order_left, vert_order_left)
        answer_right = fast_helper(cluster_list_right, horiz_order_right, vert_order_right)
        answer = min([answer_left, answer_right])
        horiz_order_mid = []
        for idx in horiz_order:
            if cluster_list[idx].horiz_center() > mid - answer[1]:
                horiz_order_mid.append(idx)
            if cluster_list[idx].horiz_center() > mid + answer[1]:
                break
        horiz_order_mid_set = set(horiz_order_mid)
        vert_order_mid = []
        for idx in vert_order:
            if idx in horiz_order_mid_set:
                vert_order_mid.append(object)
        mid_num = len(vert_order_mid)
        for idx1 in range(mid_num - 1):
            for idx2 in range(1, min(idx1 + 3, mid_num - 1)):
                new_answer = pair_distance(cluster_list, idx1, idx2)
                answer = min(answer, new_answer)
        return answer
            
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
    return (answer[0], min(answer[1:]), max(answer[1:]))

    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        closest_pair_idx = fast_closest_pair(cluster_list)[1:2]
        merged_cluster = cluster_list.pop(closest_pair_idx[0]).merge_clusters(cluster_list.pop(closest_pair_idx[1]))
        cluster_list.append(merged_cluster)
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
            k_cluster[k_cluster_idx] = cluster_list[idx].merge_clusters(k_cluster[k_cluster_idx])
    return k_cluster
