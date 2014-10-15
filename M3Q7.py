import alg_cluster


def compute_distortion(cluster_list, data_table):
    distortion = 0
    for cluster in cluster_list:
        error = cluster.cluster_error(data_table)
        distortion += error
    return distortion

  