import json
EXAMPLE = json.dumps({
    'nodes': [
        {
            'id': 0,
            'to': [
                1, 2
            ],
            'by': [
                3, 7
            ]
        },
        {
            'id': 1,
            'to': [
                2, 3
            ],
            'by': [
                11, 9
            ]
        },
        {
            'id': 2,
            'to': [
                4
            ],
            'by': [
                3
            ]
        },
        {
            'id': 3,
            'to': [
                5
            ],
            'by': [
                5
            ]
        },
        {
            'id': 4,
            'to': [
                3, 5
            ],
            'by': [
                1, 9
            ]
        },
        {
            'id': 5,
            'to': [],
            'by': []
        }
    ]
})

def read(fname):
    import json
    if isinstance(fname, str):
        return json.loads(fname)
    else:
        import os
        if not os.path.exists(fname):
            raise Exception('Unable to locate file {fname}'.format(**locals()))

        elif os.path.splitext(fname)[1] != '.json':
            raise Exception('Unkown format, json expected'.format(**locals()))

        with open(fname, 'rb') as f:
            return json.load(f)

def parse(content):
    # -> Dimension, parsed_content
    # TODO parse format
    dim = len(content['nodes'])
    return dim, content

def run(fname, first, destination):
    from heapq import heapify, heappush, heappop
    from models import AdjacenceMatrix, DistanceTable

    matrix = AdjacenceMatrix(*parse(read(fname)))
    dtable = DistanceTable(matrix, first)
    candidates = list(dtable.update(matrix, first))

    dtable.visit(first)
    heapify(candidates)

    while len(candidates) > 0:

        goto = heappop(candidates)[1]
        for elem in dtable.update(matrix, goto):
            heappush(candidates, elem)

        dtable.visit(goto)

    print(dtable.distances)
    print(dtable.min_path(matrix, first, destination))
