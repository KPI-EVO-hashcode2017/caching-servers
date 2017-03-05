from collections import defaultdict
import numpy as np


def _readints(line):
    return map(int, line.split(' '))


def readfile(filename):
    print('readfile start')
    with open(filename, 'r') as file_in:
        num_videos, num_endpoints, req_descriptions, num_caches, capacity = (
            _readints(next(file_in))
        )
        videosizes = np.array(list(_readints(next(file_in))))
        dc = np.empty(num_endpoints, dtype=np.int32)
        e2c = np.full((num_endpoints, num_caches), np.inf, dtype=np.int32)
        e2v = np.full((num_endpoints, num_videos), 0, dtype=np.int32)

        for e_id in range(num_endpoints):
            latency, cache_servers = _readints(next(file_in))
            dc[e_id] = latency

            for _ in range(cache_servers):
                server_id, server_latency = _readints(next(file_in))
                e2c[e_id][server_id] = server_latency
        for _ in range(req_descriptions):
            video_id, endpoint_id, requests_num = _readints(next(file_in))
            e2v[endpoint_id][video_id] = requests_num
    print('readfile end')
            
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


def writefile(fname, result):
    with open(fname, 'w') as fileout:
        fileout.write(str(len(result)))
        for k, v in result.items():
            fileout.write('\n')
            fileout.write(str(k) + ' ' + ' '.join([str(x) for x in v]))
