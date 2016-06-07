import os

from PyQt5 import QtCore, QtGui, QtWidgets

from base import BaseWidgetView

from spelling_checker.controller import SpCheckerController
from spelling_checker.ui_sp_view import Ui_SpCheckerWidget

class SpCheckerView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(SpCheckerView, self).__init__(parent, *args, **kwargs)
        self._fileDialog = None
        self.controller = SpCheckerController(self)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return SpCheckerView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_SpCheckerWidget()
        self.ui.setupUi(self)

        self._fileDialog = QtWidgets.QFileDialog(self)
        self._fileDialog.setNameFilters(['DIC (*.dic)'])
        self._fileDialog.fileSelected.connect(self.controller.file_selected)

        self.ui.filePickerButton.clicked.connect(self.show_file_dialog)
        self.ui.runButton.clicked.connect(self.controller.start)
        # XXX
        self.ui.runButton.setEnabled(True)

    def get_text_lines(self):
        # Clean the output
        self.ui.outputText.setText('')
        # Return the input
        return self.ui.inputText.toPlainText().split('\n')

    def show_file_dialog(self):
        self._fileDialog.show()

    def update_filedata(self, fname, enable):
        self.ui.filePickerButton.setText(os.path.basename(fname))
        self.ui.runButton.setEnabled(enable)

    def update_suggestions(self, word, suggestions):
        pr_text = self.ui.outputText.toPlainText()
        suggestions_as_str = ','.join(suggestions)
        self.ui.outputText.setText(
            '{pr_text}\n'
            '{word}:\n'
            '\t{suggestions_as_str}\n'.format(**locals())
        )
