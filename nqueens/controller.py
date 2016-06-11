import os
import json

from base import BaseController
from nqueens.models import Piece, Panel, Meta


class NQueensController(BaseController):
    def __init__(self, view):
        super(NQueensController, self)
        self._piece_data = None
        self._piece_cache = None
        self.view = view

    @classmethod
    def get_instance(cls, view):
        return cls(view)

    def pre_switch(self):
        pass

    def start(self):
        dim = self.view.get_dimension()
        # Cached factory, only 1 file read per list
        pieces = [Piece.from_file(self._piece_data) for i in range(dim)]
        panel = Panel(dim)

        self.view.notify({
            'func': 'update_panel',
            'data': {
                'pieces': {},
            }
        })

        res = self.run(panel, pieces, idx=0, ci=0)
        if res:
            self.view.notify({
                'func': 'update_panel',
                'data': {
                    'pieces': panel.pieces,
                }
            })
        else:
            self.view.notify({
                'func': 'display_error',
                'data': {
                    'message': 'No solution found :(',
                }
            })

    def run(self, panel, pieces, idx, ci):
        dim = panel.dimension
        # Base case
        if idx == len(pieces):
            return True
        else:
            # Ultra-fast because:
            # 1. All the pieces are the same (less combinations and shit)
            # 2. We start from the previous index, this makes the panel smaller
            #    each time
            # 3. Instead of keeping track of the killing positions we do a
            #    check each time a piece is added in order to avoid a kill
            #    (which is faster)
            # 4. Python dict operations are astonishingly fast
            for i in range(ci, dim):
                for j in range(dim):
                    if panel.add_piece(pieces[idx], (i, j)):
                        if self.run(panel, pieces, idx+1, i):
                            return True
                        else:
                            panel.remove_piece(pieces[idx])
            return False

    def piece_selected(self, piece_name):
        if not self._piece_cache:
            self._piece_cache = Meta.get_piece_definitions()
        self._piece_data = self._piece_cache.get(piece_name)
        if self._piece_data:
            self._piece_data = self._piece_data[1]
        self.view.notify({
            'func': 'enable_run',
            'data': {
                'enable':  bool(self._piece_data),
            }
        })

    @staticmethod
    def get_pieces_attr(attr):
        candidates = Meta.get_piece_definitions()
        if all(attr in candidate[0].keys() for candidate in candidates.values()):
            return [candidate[0][attr] for candidate in candidates.values()]
        else:
            return []
