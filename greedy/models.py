# JSON EXPECTED FORMAT
# [nodes]
#  |
#  +-> to: list of nodes (from node list) where the current node goes
#  +-> by: weight of the connections to nodes on 'to' list
from heapq import heapify, heappush, heappop
UNREACHABLE = -1

class AdjacenceMatrix(list):
    def __init__(self, dimension, parsed_content):
        # XXX rethink, parallelize
        matrix = [[0 if i == j else UNREACHABLE for j in range(dimension)]
                  for i in range(dimension)]

        for node, data in enumerate(parsed_content['nodes']):
            node = data.get('id', node)
            by = data['by']
            for idx, conn in enumerate(data['to']):
                matrix[node][conn] = by[idx]

        super(AdjacenceMatrix, self).__init__(matrix)

    def get_children(self, node):
        return self[node]

    def get_parents(self, node):
        for elem in self:
            yield elem[node]

class DistanceTable:
    def __init__(self, adjacence_matrix, origin):
        if isinstance(adjacence_matrix, AdjacenceMatrix):
            self.distances = list(adjacence_matrix.get_children(origin))
        else:
            raise RuntimeError('AdjacenceMatrix instance expected, got {}'
                               ''.format(type(adjacence_matrix)))

    # Because of ugliness
    def _valid(self, idx, distance):
        return (self.distances[idx] == UNREACHABLE or
                distance <= self.distances[idx])

    def get_and_update(self, adjacence_matrix, node):
        current_distance = self.distances[node]
        for idx, next_distance in enumerate(adjacence_matrix.get_children(node)):
            distance = current_distance + next_distance

            if (idx != node and next_distance != UNREACHABLE and
                    self._valid(idx, distance)):
                self.distances[idx] = distance
                yield (distance, idx)

    def min_path(self, adjacence_matrix, origin, destination):
        if origin == destination:
            return ''

        node = destination
        path = [node]
        while node != origin:
            for idx, distance in enumerate(adjacence_matrix.get_parents(node)):
                if (idx != node and distance != UNREACHABLE and
                        distance + self.distances[idx] == self.distances[node]):
                    node = idx
                    break
            path.append(node)

        # goddamn magic
        return path[::-1]


class Heap:
    def __init__(self, iterable, first):
        self.items = list(iterable)
        self.len = len(self.items)
        heapify(self.items)

        self.visited = set([first])

    def pop_min(self):
        if self.len > 0:
            goto = heappop(self.items)[1]
            self.len -= 1

            while goto in self.visited and self.len > 0:
                goto = heappop(self.items)[1]
                self.len -= 1

            return None if goto in self.visited else goto
        else:
            return None

    def add(self, iterable, node):
        for elem in iterable:
            heappush(self.items, elem)
            self.len += 1

        self.visited.add(node)
