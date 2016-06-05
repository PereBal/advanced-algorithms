import os
import subprocess
import json
from heapq import heapify, heappush, heappop

from base import BaseController

from greedy.models import AdjacenceMatrix, DistanceTable, Heap

def read(fname):
    if not os.path.exists(fname):
        raise Exception('Unable to locate file {fname}'.format(**locals()))

    elif os.path.splitext(fname)[1] != '.json':
        raise Exception('Unkown format, JSON expected'.format(**locals()))

    with open(fname, 'rt') as fd:
        return json.load(fd)


def to_dotfile(jsonfile, colored_arrows):
    padding = ' ' * 2

    nodes = read(jsonfile).get('nodes')

    head = ['{pad}{node} [ label="{name}" ];\n'.format(
        pad=padding, node=node['id'], name=node['name'])
            for node in nodes if node.get('name')]

    body = ['{pad}{src} -> {dst} [ label="{weight}"{color} ];\n'.format(
        pad=padding, src=node['id'], dst=dest, weight=node['by'][idx],
        color=', color="red"' if (node['id'], dest) in colored_arrows else '')
            for node in nodes
            for idx, dest in enumerate(node['to'])]

    new_name = '{name}.{ext}'.format(
        name=os.path.splitext(jsonfile)[0], ext='dot')

    with open(new_name, 'w') as fd:
        fd.write('digraph {\n')
        fd.write(padding + 'graph [ rankdir="LR" ];\n')
        fd.write(padding + 'node [ shape=polygon, sides=4, height=0.1, width=0.45, fontsize=18 ];\n')
        fd.writelines(head)
        fd.writelines(body)
        fd.write('}\n')


def to_png(dotfile, colored_arrows):
    name, ext = os.path.splitext(dotfile)
    if ext != '.dot':
        if ext == '.json':
            to_dotfile(dotfile, colored_arrows)
            dotfile = name + '.dot'
        else:
            raise Exception('Unkown format, JSON or DOT expected'.format(
                **locals()))

    new_name = '{name}.{ext}'.format(
        name=name, ext='png')
    subprocess.call(['dot', '-o', new_name, '-Tpng', dotfile])

    return new_name


def parse(data):
    # -> Dimension, parsed_content
    # TODO parse format
    dim = len(data['nodes'])
    return dim, data


class GreedyController(BaseController):

    def __init__(self, view):
        super(GreedyController, self)
        self.view = view
        self._file = 'None'

    @classmethod
    def get_instance(cls, view):
        return cls(view)

    @staticmethod
    def run(fname, origin, destination):
        if  origin < 0 or origin == destination:
            return []
        matrix = AdjacenceMatrix(*parse(read(fname)))
        if destination >= matrix.dimension:
            return []
        dtable = DistanceTable(matrix, origin)
        candidates = Heap(dtable.get_and_update(matrix, origin), origin)

        while candidates.len > 0:
            goto = candidates.pop_min()
            if goto is None or goto == destination:
                break
            candidates.add(dtable.get_and_update(matrix, goto), goto)
        return dtable.min_path(matrix, origin, destination)

    def to_png(self, colored_arrows):
        return to_png(self._file, colored_arrows)

    def pre_switch(self):
        if self._file != 'None':
            self.view.notify({
                'func': 'reload_graph',
                'data': {}
            })

    def file_selected(self, fname):
        self._file = fname if fname else 'None'
        self.view.notify({
            'func': 'update_filedata',
            'data': {
                'fname': self._file,
                'enable': {
                    'status': bool(fname),
                    'items': ['all']
                }
            }
        })

    def start(self):
        fname = self._file
        origin = self.view.origin
        destination = self.view.destination
        path = self.run(fname, origin, destination)
        # Notify the view
        self.view.notify({
            'func': 'display_graph',
            'data': {
                'path': path,
            }
        })
