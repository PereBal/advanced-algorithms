import os
from PyQt5 import QtWidgets, QtGui, QtQuick

from base import BaseWidgetView

from greedy.controller import GreedyController
from greedy.ui_greedy_view import Ui_GreedyWidget

class GreedyView(BaseWidgetView):

    def __init__(self, parent, *args, **kwargs):
        super(GreedyView, self).__init__(parent)
        self._parent = parent
        self._fileDialog = None
        self.controller = GreedyController(self)

        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return GreedyView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_GreedyWidget()
        self.ui.setupUi(self)

        self._fileDialog = QtWidgets.QFileDialog(self)
        self._fileDialog.setNameFilters(['JSON (*.json)'])
        self._fileDialog.fileSelected.connect(self.controller.file_selected)

        self.ui.filePickerButton.clicked.connect(self.show_file_dialog)
        self.ui.runButton.clicked.connect(self.controller.start)

    @property
    def origin(self):
        return self.ui.startBox.value()

    @property
    def destination(self):
        return self.ui.endBox.value()

    def _set_enabled(self, value, *args):
        # XXX Reflection here :3
        for elem in args:
            ui_elem = getattr(self.ui, elem)
            ui_elem.setEnabled(value)

    def _load_graph(self, colored_arrows=set()):
        pixmap = QtGui.QPixmap.fromImage(
                QtGui.QImage(self.controller.to_png(colored_arrows)))
        self.ui.contentLabel.setPixmap(pixmap)
        # Porcada...
        size = (pixmap.width()+20, pixmap.height()+80)
        self._parent._old_size = self._parent.size()
        self._parent.resize(*size)
        self.ui.contentLabel.setScaledContents(True)

    def update_filedata(self, fname, enable):
        self.ui.filePickerButton.setText(os.path.basename(fname))
        if 'all' in enable['items']:
            items = ['startBox', 'endBox', 'runButton']
        else:
            raise NotImplementedError('[\'all\'] Expected')

        if enable['status']:
            self._set_enabled(True, *items)
        else:
            self._set_enabled(False, *items)

        self._load_graph()

    def reload_graph(self):
        self._load_graph()

    def display_graph(self, path):
        arrows = set([(path[i], path[i+1]) for i in range(len(path)-1)])
        self._load_graph(arrows)

    def show_file_dialog(self):
        self._fileDialog.show()



