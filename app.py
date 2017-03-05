import sys
from collections import defaultdict
from pprint import pprint as pp

import numpy as np

from rw import readfile, writefile
from solver import solve


filename = sys.argv[1]

data = readfile(filename)

e2v = data['endpoint_video_requests']
e2c = data['endpoint_cache_latency']
dcl = data['data_center_latency']
vsz = data['video_sizes']
csz = data['cache_size']


# build matrix of latency differences
e2cd = np.copy(e2c)
n_endpoints, n_caches = e2cd.shape
for e in range(n_endpoints):
    for c in range(n_caches):
        e2cd[e][c] = max(dcl[e] - e2cd[e][c], 0)

# calculate matrix of profits
profits = np.transpose(e2cd).dot(e2v)

result = solve(profits, vsz, csz)
writefile(filename + '.out', result)
