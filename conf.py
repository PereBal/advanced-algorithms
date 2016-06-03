import os
from itertools import groupby

ROOT = os.path.dirname(os.path.abspath(__file__))

SHARED_DATA_FOLDER = os.path.join(ROOT, 'shared_data')
SHARED_DATA = {}

def _splfun(elem_fname):
    return os.path.splitext(elem_fname)[0]

# Dynamically load all data paths to shared_data. We'll grup elements with a
# common prefix together and inside them we'll put an entry for each exception.
# For example:
# {
#     'run': {
#         'jpe': '/home/pere/Repositories/Advanced_Algorithms/shared_data/run.jpe',
#         'png': '/home/pere/Repositories/Advanced_Algorithms/shared_data/run.png',
#     },
# }
#
# Why? Because we can and because this way we don't have to remember any path,
# just the filename and the extension (because of multiple files named the same
# way)

_ITEMS = sorted(os.listdir(SHARED_DATA_FOLDER), key=_splfun)
for ign, extensions in groupby(_ITEMS, _splfun):
    name = os.path.splitext(ign)[0]
    fname = os.path.join(SHARED_DATA_FOLDER, name)

    SHARED_DATA[name] = {}
    for ext in extensions:
        ext = os.path.splitext(ext)[1]
        SHARED_DATA[name][ext[1:]] = '{fname}{ext}'.format(**locals())
