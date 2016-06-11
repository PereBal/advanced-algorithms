from PyQt5 import QtCore, QtGui, QtWidgets

from base import BaseWidgetView

from nqueens.controller import NQueensController
from nqueens.ui_nqueens_view import Ui_NQueensWidget

class NQueensView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(NQueensView, self).__init__(parent)
        self.controller = NQueensController(self)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return NQueensView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_NQueensWidget()
        self.ui.setupUi(self)

        # TODO extreure les dades
        self.ui.pieceBox.addItem('None')
        for name in NQueensController.get_pieces_attr('name'):
            self.ui.pieceBox.addItem(name)

        self.ui.pieceBox.currentTextChanged.connect(self.controller.piece_selected)
        self.ui.runButton.clicked.connect(self.controller.start)

    def get_dimension(self):
        return self.ui.dimBox.value()

    def _draw_panel(self, scene, dim):
        white = QtGui.QBrush(QtGui.QColor(100, 30, 30))
        black = QtGui.QBrush(QtGui.QColor(0, 0, 0))

        max_w = self.ui.graphics.width() - 20
        max_h = self.ui.graphics.height() - 20

        # Panel size, let's make it fit on the screen
        size = min(max_w, max_h)
        # Offset
        start_x = (max_w - size) // 2
        start_y = (max_h - size) // 2
        # Cell size
        incr = size // dim

        # Yea, zip of ranges instead of a variable... but this way is cooler
        # and more pythonic
        for i, xpos in zip(range(dim), range(start_x, size+start_x, incr)):
            for j, ypos in zip(range(dim), range(start_y, size+start_y, incr)):
                brush = black if (i+j) % 2 == 0 else white
                scene.addRect(xpos, ypos, incr, incr, brush=brush)
        return scene

    def _draw_pieces(self, scene, dim, pieces):
        max_w = self.ui.graphics.width() - 20
        max_h = self.ui.graphics.height() - 20

        # Panel size, let's make it fit on the screen
        size = min(max_w, max_h)
        # Start Offset
        start_x = (max_w - size) // 2
        start_y = (max_h - size) // 2
        # Cell size
        cs = size // dim
        # In cell offset
        inner_offset = cs // 40

        for pos, piece in pieces.values():
            real_start_x = pos[0] * cs + start_x + inner_offset
            real_start_y = pos[1] * cs + start_y + inner_offset
            pxmap = QtGui.QPixmap(piece.image).scaled(cs-inner_offset,
                                                      cs-inner_offset)
            pixmap = scene.addPixmap(pxmap)
            pixmap.setOffset(real_start_x, real_start_y)

    def update_panel(self, pieces):
        dim = self.get_dimension()
        scene = QtGui.QGraphicsScene(self.ui.graphics)
        self._draw_panel(scene, dim)
        if len(pieces) > 0:
            self._draw_pieces(scene, dim, pieces)
        self.ui.graphics.setScene(scene)

    def enable_run(self, enable):
        self.ui.runButton.setEnabled(enable)
