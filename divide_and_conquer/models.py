import math
from collections import namedtuple
from operator import itemgetter

# Generate samples
# import json; import random as rnd; rnd.seed();
# with open('divide_and_conquer/data/example.json', 'w') as f:
#     json.dump({
#         'points': [
#             {
#                 'x': rnd.randint(0, 1000000),
#                 'y': rnd.randint(0, 1000000)
#             } for x in range (10000)
#         ]
#     }, f)

class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = ()

    def distance(self, point2):
        if isinstance(point2, Point):
            return math.sqrt(
                (self.x - point2.x) * (self.x - point2.x) +
                (self.y - point2.y) * (self.y - point2.y)
            )
        else:
            raise Exception('Go away, incompatible types!')


class PointList(list):
    __slots__ = ()


class SortedPointList(PointList):
    __slots__ = ()

    def __init__(self, *args):
        super(SortedPointList, self).__init__(*args)
        # Sort by X-axis
        self.sort(key=itemgetter(0))
