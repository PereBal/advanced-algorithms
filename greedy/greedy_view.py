import os
from PyQt5 import QtWidgets, QtGui, QtQuick

from greedy.controllers import to_png, run
from greedy.ui_greedy_view import Ui_GreedyWidget

class GreedyView(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(GreedyView, self).__init__(parent)
        self._file = 'None'
        self._parent = parent
        self._fileDialog = None
        self.setup_ui()

    def file_selected(self, fname):
        self._file = fname if fname else 'None'
        self.ui.filePickerButton.setText(os.path.basename(self._file))
        if fname:
            self._set_enabled(True, 'startBox', 'endBox', 'runButton')
            self._load_graph()
        else:
            self._set_enabled(False, 'startBox', 'endBox', 'runButton')

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return GreedyView(parent, *args, **kwargs)

    def pre_switch(self):
        if self._file != 'None':
            self._load_graph()

    def _set_enabled(self, value, *args):
        # XXX Reflection here :3
        for elem in args:
            ui_elem = getattr(self.ui, elem)
            ui_elem.setEnabled(value)

    def _load_graph(self, colored_arrows=[]):
        pixmap = QtGui.QPixmap.fromImage(
                QtGui.QImage(to_png(self._file, colored_arrows)))
        self.ui.contentLabel.setPixmap(pixmap)
        # Porcada...
        size = (pixmap.width()+20, pixmap.height()+80)
        self._parent._old_size = self._parent.size()
        self._parent.resize(*size)
        self.ui.contentLabel.setScaledContents(True)

    def start(self):
        origin = self.ui.startBox.value()
        destination = self.ui.endBox.value()
        path = run(self._file, origin, destination)
        arrows = [(path[i], path[i+1]) for i in range(len(path)-1)]
        self._load_graph(arrows)

    def show_file_dialog(self):
        self._fileDialog.show()

    def setup_ui(self):
        self.ui = Ui_GreedyWidget()
        self.ui.setupUi(self)

        self._fileDialog = QtWidgets.QFileDialog(self)

        self._fileDialog.fileSelected.connect(self.file_selected)
        self.ui.filePickerButton.clicked.connect(self.show_file_dialog)
        self.ui.runButton.clicked.connect(self.start)


