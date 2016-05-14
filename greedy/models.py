# JSON EXPECTED FORMAT
# [nodes]
#  |
#  +-> to: list of nodes (from node list) where the current node goes
#  +-> by: weight of the connections to nodes on 'to' list

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

    def first(self, node):
        if node > len(self):
            raise IndexError('{i} is out of bounds on {self}'.format(i=node+1,
                                                                     self=self))
        return self[node]

    def get_children(self, node):
        return self[node]

    def get_parents(self, node):
        for elem in self:
            yield elem[node]

class DistanceTable:
    def __init__(self, adjacence_matrix, origin):
        if isinstance(adjacence_matrix, AdjacenceMatrix):
            self.distances = list(adjacence_matrix.get_children(origin))
            self.visited = set()
        else:
            raise RuntimeError('AdjacenceMatrix instance expected, got {}'
                               ''.format(type(adjacence_matrix)))

    def visit(self, node):
        self.visited.add(node)

    def update(self, adjacence_matrix, node):
        # Already visited candidate (i should fix this xD)
        if node in self.visited:
            return []

        current_distance = self.distances[node]
        for idx, next_distance in enumerate(adjacence_matrix.get_children(node)):

            distance = current_distance + next_distance
            if (idx != node and next_distance != UNREACHABLE and
                    idx not in self.visited):

                if (self.distances[idx] == UNREACHABLE or
                        distance <= self.distances[idx]):
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
