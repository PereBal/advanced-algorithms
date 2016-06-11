import operator as op
import os
import json
from collections import defaultdict
from functools import partial

from conf import ROOT

class Meta:
    IMAGES = defaultdict(set)
    IPATH = {}
    _file_name_cache = None
    _file_data_cache = None

    @staticmethod
    def set_image(image, sid):
        Meta.IMAGES[image].add(sid)
        Meta.IPATH[image] = os.path.join(
            ROOT,
            os.path.dirname(os.path.abspath(__file__)),
            'data',
            image,
        )

    @staticmethod
    def get_image(sid):
        for img, ids in Meta.IMAGES.items():
            if sid in ids:
                return Meta.IPATH[img]
        return ''

    @staticmethod
    def read(fname):
        if not os.path.exists(fname):
            raise Exception('Unable to locate file {fname}'.format(**locals()))

        elif os.path.splitext(fname)[1] != '.json':
            raise Exception('Unkown format, JSON expected'.format(**locals()))

        with open(fname, 'rt') as fd:
            return json.load(fd)

    @staticmethod
    def parse(data):
        piece = data['piece']
        return {
            'name': piece['id'],
            'kills': piece['kills'],
            'img': piece['img']
        }

    @staticmethod
    def get_piece_definitions():
        dirname = os.path.join(
            ROOT,
            os.path.dirname(os.path.abspath(__file__)),
            'data',
        )
        candidates = [os.path.join(dirname, fname)
                      for fname in os.listdir(dirname)
                      if os.path.splitext(fname)[1] == '.json']
        dirty = [(Meta.parse(Meta.read(fname)), fname) for fname in candidates]
        return {
            piece['name']: (piece, fname)
            for piece, fname in dirty
        }

    @classmethod
    def from_file(cls, fname):
        # Yeeeaaaaa, cacheeess
        if not cls._file_data_cache or \
                cls._file_name_cache != fname:
            cls._file_name_cache = fname
            cls._file_data_cache = Meta.parse(Meta.read(fname))
        return cls._file_data_cache


class Piece:
    def __init__(self, kills, img):
        super(Piece, self)
        self._image_cache = None
        # Shit-ton of magic here
        self._init_kills(kills)

        Meta.set_image(img, id(self))

    def _init_kills(self, kills):
        """
        This function generates a list of lambda functions which can be
        applied to 2 points (piece position and desired x,y) and will return
        True if x,y is in the piece's kill area (False otherwise).

        Special values: 0, +/-n. 0 means same value and +/-n is used to
        mark 'all' cells of that row/col from the piece up/right (+) or from
        the piece down/left (-)
        """
        self._kills = [lambda px, py, x, y: x == px and y == py]
        for kx, ky in kills:
            # Diagnonals
            if kx in ('+n', '-n') and ky in ('+n', '-n'):
                self._kills.append(
                        lambda px, py, x, y: abs(x-px) == abs(y-py))

            elif kx == '0':
                if ky == '+n':
                    self._kills.append(
                        lambda px, py, x, y: x == px and y < py)

                elif ky == '-n':
                    self._kills.append(
                        lambda px, py, x, y: x == px and y > py)

                else:
                    fy = partial(op.add, int(ky[1:])) \
                                 if ky[0] == '+' \
                                 else partial(op.sub, int(ky[1:]))
                    self._kills.append(
                        lambda px, py, x, y: x == px and y == fy(py))

            elif ky == '0':
                if kx == '+n':
                    self._kills.append(
                        lambda px, py, x, y: x <= px and y == py)

                elif kx == '-n':
                    self._kills.append(
                        lambda px, py, x, y: x >= px and y == py)

                else:
                    fx = partial(op.add, int(kx[1:])) \
                                 if kx[0] == '+' \
                                 else partial(op.sub, int(kx[1:]))
                    self._kills.append(
                        lambda px, py, x, y: x == fx(px) and y == py)

            else:
                fx = partial(op.add, int(kx[1:])) \
                             if kx[0] == '+' \
                             else partial(op.sub, int(kx[1:]))
                fy = partial(op.add, int(ky[1:])) \
                             if ky[0] == '+' \
                             else partial(op.sub, int(ky[1:]))
                self._kills.append(
                    lambda px, py, x, y: x == fx(px) and y == fy(py))

    @property
    def image(self):
        if not self._image_cache:
            self._image_cache = Meta.get_image(id(self))
        return self._image_cache

    @classmethod
    def from_file(cls, fname):
        # Efficient instantiator to be used on lists of objects of the same
        # type
        p = Meta.from_file(fname)
        return cls(p['kills'], p['img'])

    def kills(self, px, py, x, y):
        return any(kFun(px, py, x, y) for kFun in self._kills)


class Panel:
    def __init__(self, dimension):
        super(Panel, self)
        self.pieces = {}
        self.dimension = dimension

    def add_piece(self, piece, pos):
        # nones...
        x, y = pos

        for ipiece in self.pieces.values():
            # If we had different types of pieces, there we sould validate
            # ipiece doesn't kill piece and the contrary.
            if ipiece[1].kills(*ipiece[0], x, y):
                return False

        self.pieces[id(piece)] = (pos, piece)
        return True

    def remove_piece(self, piece):
        del self.pieces[id(piece)]
