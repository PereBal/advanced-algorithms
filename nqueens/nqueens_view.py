from PyQt5 import QtCore, QtGui, QtWidgets

from base import BaseWidgetView

from nqueens.ui_nqueens_view import Ui_NQueensWidget

class NQueensView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(NQueensView, self).__init__(parent)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return NQueensView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_NQueensWidget()
        self.ui.setupUi(self)
