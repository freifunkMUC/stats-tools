#!/usr/bin/env python3

import sys
import json
import pickle
import struct
from time import time

def get_metrics(timestamp, stats, prefix=''):
    for k,v in stats.items():
        key = '.'.join([prefix, k])
        if type(v) is dict:
            for i in get_metrics(timestamp, v, key):
                yield i
        elif type(v) is not str:
            yield (key, (timestamp, v))

def load_metrics(f):
    nodes = json.load(f)
    for (node_id,node_data) in nodes['nodes'].items():
        for m in get_metrics(int(time()), node_data['statistics'], 'nodes.' + node_id):
            yield m

def get_pickled_msg(metrics):
    payload = pickle.dumps(list(metrics), protocol=2)
    header = struct.pack("!L", len(payload))
    return header + payload

def main():
    metrics = load_metrics(sys.stdin)

    for (k,(t,v)) in metrics:
        print(' '.join(map(str, [k,v,t])))

if __name__ == '__main__':
    main()
