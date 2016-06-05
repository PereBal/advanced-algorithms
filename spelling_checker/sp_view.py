from PyQt5 import QtCore, QtGui, QtWidgets

from base import BaseWidgetView

from spelling_checker.ui_sp_view import Ui_SpCheckerWidget

class SpCheckerView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(SpCheckerView, self).__init__(parent, *args, **kwargs)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return SpCheckerView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_SpCheckerWidget()
        self.ui.setupUi(self)
