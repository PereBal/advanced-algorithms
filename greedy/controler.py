def read(fname):
    import json
    import os
    if not os.path.exists(fname):
        raise Exception('Unable to locate file {fname}'.format(**locals()))

    elif os.path.splitext(fname)[1] != '.json':
        raise Exception('Unkown format, json expected'.format(**locals()))

    with open(fname, 'rt') as fd:
        return json.load(fd)

def parse(content):
    # -> Dimension, parsed_content
    # TODO parse format
    dim = len(content['nodes'])
    return dim, content

def run(fname, first, destination):
    from heapq import heapify, heappush, heappop
    from models import AdjacenceMatrix, DistanceTable, Heap

    matrix = AdjacenceMatrix(*parse(read(fname)))
    dtable = DistanceTable(matrix, first)
    candidates = Heap(dtable.get_and_update(matrix, first), first)

    while candidates.len > 0:
        goto = candidates.get_min()
        if goto is None or goto == destination:
            break
        candidates.add(dtable.get_and_update(matrix, goto), goto)

    return dtable.min_path(matrix, first, destination)
