from collections import defaultdict


def readints(line):
    return map(int, line.split(' '))


def readfile(filename):
    videosizes = []
    endpoints = []
    requests = defaultdict(dict)
    with open(filename, 'r') as file_in:
        V, E, R, C, X = readints(next(file_in))
        videosizes = readints(next(file_in))
        for e_id in range(E):
            e_latency, cache_servers = readints(next(file_in))
            endpoint = {
                'latency': e_latency,
                'cache_servers': [],
            }
            for _ in range(cache_servers):
                server_id, server_latency = readints(next(file_in))
                endpoint['cache_servers'].append({
                    'id': server_id,
                    'latency': server_latency,
                })
            endpoints.append(endpoint)
        for _ in range(R):
            video_id, endpoint_id, requests_num = readints(next(file_in))
            requests[video_id][endpoint_id] = requests_num
    return {
        'sizes': videosizes,
        'endpoints': endpoints,
        'requests': requests,
    }


from pprint import pprint
pprint(readfile('data/kittens.in'))
            
