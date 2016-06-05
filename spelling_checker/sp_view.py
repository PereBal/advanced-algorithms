from queue import Empty
from PyQt5 import QtCore, QtGui, QtWidgets

from spelling_checker.ui_sp_view import Ui_SpCheckerWidget

class SpCheckerView(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(SpCheckerView, self).__init__(parent)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return SpCheckerView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_SpCheckerWidget()
        self.ui.setupUi(self)
