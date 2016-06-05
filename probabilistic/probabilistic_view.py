import os

from PyQt5 import QtWidgets, QtCore

from base import BaseWidgetView

from probabilistic.controller import ProbabilisticController
from probabilistic.ui_probabilistic_view import Ui_ProbabilisticWidget

class ProbabilisticView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(ProbabilisticView, self).__init__(parent, *args, **kwargs)
        self._fileDialog = None
        self._dbDialog = None
        self.controller = ProbabilisticController(self)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return ProbabilisticView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_ProbabilisticWidget()
        self.ui.setupUi(self)

        # Overriding some signals we'd need an instance only but whatever
        self._fileDialog = QtWidgets.QFileDialog(self)
        self._fileDialog.setNameFilters(['Images (*.png *.jpe *.jpg *.jpeg)',
                                         'Any file (*)'])
        self._fileDialog.fileSelected.connect(self.controller.file_selected)
        self.ui.filePickerButton.clicked.connect(self.show_file_dialog)

        self._dbDialog = QtWidgets.QFileDialog(self)
        self._dbDialog.setMimeTypeFilters(['application/json'])
        self._dbDialog.fileSelected.connect(self.controller.db_file_selected)
        self.ui.dbPickerButton.clicked.connect(self.show_db_dialog)

        self.ui.runButton.clicked.connect(self.controller.start)

    def show_file_dialog(self):
        self._fileDialog.show()

    def show_db_dialog(self):
        self._dbDialog.show()

    def update_filedata(self, fname, is_db, runnable):
        if is_db:
            self.ui.dbPickerButton.setText(os.path.basename(fname))
        else:
            self.ui.filePickerButton.setText(os.path.basename(fname))
        self.ui.runButton.setEnabled(runnable)

    def update_tabledata(self, items):
        self.ui.tableWidget.setRowCount(len(items))
        for row, item in enumerate(items):
            for col in range(2):
                self.ui.tableWidget.setCellWidget(row, col,
                                                  QtWidgets.QLabel(
                                                      text=str(item[col-1]),
                                                      alignment=QtCore.Qt.AlignCenter))


