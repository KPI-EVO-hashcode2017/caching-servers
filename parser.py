from collections import defaultdict
from pprint import pprint
import numpy as np
import sys


def readints(line):
    return map(int, line.split(' '))


def readfile(filename):
    with open(filename, 'r') as file_in:
        num_videos, num_endpoints, req_descriptions, num_caches, capacity = (
            readints(next(file_in))
        )
        videosizes = np.array(list(readints(next(file_in))))
        dc = np.empty(num_endpoints)
        e2c = np.full((num_endpoints, num_caches), 0)
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


fname = sys.argv[1]
m = readfile(fname)
# pprint(m)

e2v = m['endpoint_video_requests']
dcs = m['data_center_latency']
e2c = m['endpoint_cache_latency']
vss = m['video_sizes']


e2cd = np.copy(e2c)
for r in range(len(e2cd)):
    for c in range(len(e2cd[r])):
        if e2cd[r][c]:
            e2cd[r][c] = dcs[r] - e2cd[r][c]

def calc_pred(diffm):
    pred = np.transpose(diffm).dot(e2v)
    return pred

pred = calc_pred(e2cd)
cache_capacity = np.full(m['num_caches'], m['cache_size'])
cache_videos = defaultdict(list)
while pred.argmax() > 0 :
    me, mv = np.unravel_index(pred.argmax(), pred.shape)
    if vss[mv] < cache_capacity[me]:
        cache_videos[me].append(mv)
        cache_capacity[me] -= vss[mv]
    pred[me][mv] = 0

with open(fname + '.out', 'w') as fileout:
    fileout.write(str(len(cache_videos)))
    for k, v in cache_videos.items():
        fileout.write('\n')
        fileout.write(str(k) + ' ' + ' '.join([str(x) for x in v]))


# pprint(cached_videos)

# pprint(data_center_result)

# pprint(np.transpose(e2c).dot(e2v))
