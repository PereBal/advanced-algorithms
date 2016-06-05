from PyQt5 import QtWidgets

from probabilistic.ui_probabilistic_view import Ui_ProbabilisticWidget

class ProbabilisticView(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(ProbabilisticView, self).__init__(parent)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return ProbabilisticView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_ProbabilisticWidget()
        self.ui.setupUi(self)
