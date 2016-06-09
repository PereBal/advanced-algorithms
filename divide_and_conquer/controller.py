import os
import math
import sys
import time
import json

from multiprocessing import Process, Queue

from base import BaseController

from divide_and_conquer.models import Point, PointList, SortedPointList

def read(fname):
    if not os.path.exists(fname):
        raise Exception('Unable to locate file {fname}'.format(**locals()))

    elif os.path.splitext(fname)[1] != '.json':
        raise Exception('Unkown format, JSON expected'.format(**locals()))

    with open(fname, 'rt') as fd:
        return json.load(fd)

def parse(data):
    return [Point(**point_tuple) for point_tuple in data['points']]

def _min_distance_O2(points):
    plen = len(points)

    if plen == 1:
        return (0, points[0])

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

    return _min_distance_O2(candidates)

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

def sample(points, num_samples):
    import random as rnd
    rnd.seed()
    max_len = len(points)-1
    return [points[rnd.randint(0, max_len)] for p in range(num_samples)]

def min_distance_O2(q, points, num_samples):
    new_points = sample(points, num_samples)
    tini = time.time()
    _min_distance_O2(new_points)
    tend = time.time() - tini
    q.put(('O2', tend))
    return None


def min_distance_Olog(q, points, num_samples):
    new_points = sample(points, num_samples)
    tini = time.time()
    _min_distance_Olog(new_points, 0, len(new_points)-1)
    tend = time.time() - tini
    q.put(('Olog', tend))
    return None


class DCController(BaseController):
    def __init__(self, view, max_samples):
        super(DCController, self)
        self._file = None
        self.max_samples = max_samples
        self.view = view

    @classmethod
    def get_instance(cls, view, max_samples):
        return cls(view)

    def pre_switch(self):
        pass

    def start(self):
        _points = parse(read(self._file))
        self.view.notify({
            'func': 'update_graphic',
            'data': {
                'num_samples': 0,
                'time_O2': [],
                'time_Olog': [],
            }
        })

        # With more than 4000 samples takes about 20seconds and so on, enough
        # with this
        #for num_samples in range(500, min(len(_points), 3500), 500):
        for num_samples in range(500, min(len(_points), self.max_samples), 250):
            t_o2, t_olog = self.run(_points, num_samples)
            self.view.notify({
                'func': 'update_graphic',
                'data': {
                    'num_samples': num_samples,
                    'time_O2': t_o2,
                    'time_Olog': t_olog,
                }
            })

        self.view.notify({
            'func': 'plot_graphic',
            'data': {}
        })

    @staticmethod
    def run(points, num_samples):
        q = Queue()

        procs = (
            Process(target=min_distance_O2, args=(q, points, num_samples)),
            Process(target=min_distance_Olog, args=(q, points, num_samples)),
        )

        for proc in procs:
            proc.start()

        res1 = q.get()
        res2 = q.get()

        e0 = res1[1] if res1[0] == 'O2' else res2[1]
        e1 = res2[1] if res2[0] == 'Olog' else res1[1]

        return (e0, e1)

    def file_selected(self, fname):
        self._file = fname if fname else None
        self.view.notify({
            'func': 'update_filedata',
            'data': {
                'fname': str(self._file),
                'enable': bool(self._file),
            }
        })
