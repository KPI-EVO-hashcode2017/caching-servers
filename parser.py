import numpy as np
import pulp

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


def get_solve(data):
    x = []
    for i in range(data.get('num_caches')):
        x.append([])
        for j in range(data.get('num_videos')):
            x[i].append(pulp.LpVariable('x{}{}'.format(i, j), 0, 1))

    prob = pulp.LpProblem('problem', pulp.LpMaximize)
    video_sizes = data.get('video_sizes')
    cache_sizes = data.get('cache_size')
    dc_latency = data.get('data_center_latency')
    latency = data.get('endpoint_cache_latency')
    reqs = data.get('endpoint_video_requests')

    for i in range(data.get('num_caches')):
        condition = pulp.lpSum([
            x[i][j] * video_sizes[j] for j in range(data.get('num_videos'))
        ])
        prob += condition <= cache_sizes, 'Sizes for {} cache'.format(i)

    aim = []

    for c in range(data.get('num_caches')):
        for v in range(data.get('num_videos')):
            for e in range(data.get('num_endpoints')):
                aim.append(
                    x[c][v] * (dc_latency[e] - latency[e][c]) * reqs[e][v]
                )
    prob += pulp.lpSum(aim)

    status = prob.solve(pulp.GLPK(msg=0))
    print(pulp.LpStatus[status])
    res = []
    for i in range(data.get('num_caches')):
        res.append([])
        for j in range(data.get('num_videos')):
            res[i].append(pulp.value(x[i][j]))
    results = np.array(res)
    return results



from pprint import pprint
# pprint(readfile('data/me_at_the_zoo.in'))
a = readfile('data/me_at_the_zoo.in')
pprint(get_solve(a))