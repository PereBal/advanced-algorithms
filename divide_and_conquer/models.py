import math
from collections import namedtuple

# XXX OOP YEEEEAAAAA!!! all this just for not using a tuple and a list of
# tuples

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
        from operator import itemgetter
        super(SortedPointList, self).__init__(*args)
        # Sort by X-axis
        self.sort(key=itemgetter(0))
