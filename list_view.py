from PyQt5 import QtWidgets

from ui_list_view import Ui_ListWidget

class ListView(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(ListView, self).__init__(parent)

        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return ListView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_ListWidget()
        self.ui.setupUi(self)
