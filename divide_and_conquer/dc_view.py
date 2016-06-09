import os
import time

import pyqtgraph
from PyQt5 import QtCore, QtGui, QtWidgets

from base import BaseWidgetView

from divide_and_conquer.controller import DCController
from divide_and_conquer.ui_dc_view import Ui_DCWidget

class DCView(BaseWidgetView):
    def __init__(self, parent, *args, **kwargs):
        super(DCView, self).__init__(parent)
        self._fileDialog = None
        self._num_samples = []
        self._times_O2 = []
        self._times_Olog = []
        self._max_samples = 2000
        self.controller = DCController(self, self._max_samples)

        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return DCView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_DCWidget()
        self.ui.setupUi(self)

        self.ui.graphics.setLabels(
            **{
                'left': 'seconds',
                'bottom': 'number of samples'
            }
        )
        self.ui.graphics.setLimits(**{
            'xMin': 0, 'xMax': self._max_samples,
            'yMin': 0,
            'minXRange': 0, 'maxXRange': self._max_samples,
            'minYRange': 0,
        })
        self.ui.graphics.showGrid(x=True, y=True)
        self.ui.graphics.addLegend()

        self._fileDialog = QtWidgets.QFileDialog(self)
        self._fileDialog.setNameFilters(['JSON (*.json)'])
        self._fileDialog.fileSelected.connect(self.controller.file_selected)

        self.ui.filePickerButton.clicked.connect(self.show_file_dialog)
        self.ui.runButton.clicked.connect(self.controller.start)

    def update_filedata(self, fname, enable):
        self.ui.filePickerButton.setText(os.path.basename(fname))
        self.ui.runButton.setEnabled(enable)

    def update_graphic(self, num_samples, time_O2, time_Olog):
        print('{num_samples} :: {time_O2} vs {time_Olog}'.format(**locals()))
        if num_samples == 0:
            self._num_samples = []
            self._times_O2 = []
            self._times_Olog = []
        else:
            self._num_samples.append(num_samples)
            self._times_O2.append(time_O2)
            self._times_Olog.append(time_Olog)

    def plot_graphic(self):
            self.ui.graphics.plot(
                x=self._num_samples,
                y=self._times_O2,
                pen=pyqtgraph.mkPen(color='r', width=3),
                antialias=True,
                name='O(2)_algorithm',
                clear=True,
            )
            self.ui.graphics.plot(
                x=self._num_samples,
                y=self._times_Olog,
                pen=pyqtgraph.mkPen(color='b', width=3),
                name='O(log-n)_algorithm',
                antialias=True,
            )


    def show_file_dialog(self):
        self._fileDialog.show()

