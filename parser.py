from collections import defaultdict
import numpy as np


def readints(line):
    return map(int, line.split(' '))


def readfile(filename):
    with open(filename, 'r') as file_in:
        num_videos, num_endpoints, req_descriptions, num_caches, capacity = (
            readints(next(file_in))
        )
        videosizes = np.array(list(readints(next(file_in))))
        dc = np.empty(num_endpoints)
        e2c = np.full((num_endpoints, num_caches), np.inf)
        e2v = np.full((num_endpoints, num_videos), 0)

        for e_id in range(num_endpoints):
            latency, cache_servers = readints(next(file_in))
            dc[e_id] = latency

            for _ in range(cache_servers):
                server_id, server_latency = readints(next(file_in))
                e2c[e_id][server_id] = server_latency
        for _ in range(req_descriptions):
            video_id, endpoint_id, requests_num = readints(next(file_in))
            e2v[endpoint_id][video_id] = requests_num
            
    return {
        'cache_size': capacity,
        'num_videos': num_videos,
        'num_endpoints': num_endpoints,
        'num_caches': num_caches,
        'data_center_latency': dc,
        'video_sizes': videosizes,
        'endpoint_cache_latency': e2c,
        'endpoint_video_requests': e2v,
    }


# from pprint import pprint
# pprint(readfile('data/kittens.in'))
