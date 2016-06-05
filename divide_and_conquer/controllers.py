import math
import sys

from multiprocessing import Process, Queue
from models import Point, PointList, SortedPointList

def read(fname):
    import json
    import os
    if not os.path.exists(fname):
        raise Exception('Unable to locate file {fname}'.format(**locals()))

    elif os.path.splitext(fname)[1] != '.json':
        raise Exception('Unkown format, JSON expected'.format(**locals()))

    with open(fname, 'rt') as fd:
        return json.load(fd)

def parse(data):
    return [Point(**point_tuple) for point_tuple in data['points']]

def min_distance_O2(points):
    plen = len(points)
    min_dist = sys.maxsize-1
    for i, point1 in enumerate(points):
        j = i + 1
        while j < plen:
            point2 = points[j]

            dist = point1.distance(point2)
            if dist < min_dist:
                min_dist = dist
                min_points = (point1, point2)
            j += 1
    return (min_dist, min_points)

def combine(points, min_set1, min_set2, idxmin, half, idxmax):
    dmin = min(min_set1[0], min_set2[0])

    candidates = []
    half_point = points[half]
    # Just a hunch, if we go from the middle to the begining or to the end
    # usually, the looping will end sooner. At least I hope so

    # Disclaimer, half not included in range
    for i in reversed(range(idxmin, half)):
        point = points[i]
        if point.distance(half_point) <= dmin:
            candidates.append(point)
        else:
            break

    for i in range(half, idxmax+1):
        point = points[i]
        if half_point.distance(point) <= dmin:
            candidates.append(point)
        else:
            break

    return min_distance_O2(candidates)

def _min_distance_Olog(points, idxmin, idxmax):
    if idxmax - idxmin == 1:
        point_min, point_max = points[idxmin], points[idxmax]
        return (point_min.distance(point_max), (point_min, point_max))
    else:
        half = round((idxmax+idxmin) / 2)
        return combine(points,
                       _min_distance_Olog(points, idxmin, half),
                       _min_distance_Olog(points, half, idxmax),
                       idxmin, half, idxmax)

def min_distance_Olog(points):
    return _min_distance_Olog(points, 0, len(points)-1)

def run(queue, fname):
    if mode == 'O2':
        points_o2 = PointList(parse(read(fname)))
        return min_distance_O2(points_o2)
    elif mode == 'Olog':
        points_olog = SortedPointList(parse(read(fname)))
        return min_distance_Olog(points_olog)
    else:
        raise Exception('bye')

def dispatch(fnames):
    queue = Queue()
    for sample, fname in enumerate(fnames):
        process = Process(target=run, args=(queue, fname))
        process.start()


