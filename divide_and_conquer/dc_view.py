from queue import Empty

from PyQt5 import QtCore, QtGui, QtWidgets

from base import BaseWidgetView

from divide_and_conquer.ui_dc_view import Ui_DCWidget

class DCView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(DCView, self).__init__(parent)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return DCView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_DCWidget()
        self.ui.setupUi(self)
