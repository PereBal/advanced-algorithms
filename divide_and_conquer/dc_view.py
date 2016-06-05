from queue import Empty
from PyQt5 import QtCore, QtGui, QtWidgets

from divide_and_conquer.ui_dc_view import Ui_DCWidget

class DCView(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(DCView, self).__init__(parent)
        self.setup_ui()

    @classmethod
    def as_view(cls, parent, *args, **kwargs):
        return DCView(parent, *args, **kwargs)

    def setup_ui(self):
        self.ui = Ui_DCWidget()
        self.ui.setupUi(self)

# class DCView(QtWidgets.QWidget):
#     def __init__(self, queue, **kwargs):
#         super(DCView, self).__init__(kwargs.get('parent', None))
#         width = kwargs.get('width', 400)
#         height = kwargs.get('height', 300)
#         # Shared queue with the controler
#         self._dim = (width, height)
#         self._goffset = (10,) * 2
#         self._gdim = (width-10, height-10)
#         self._nsamples = kwargs.get('nsamples', 20)
#         self._scale = (width // self._nsamples, height // self._nsamples)
#         self._queue = queue
# 
#         self._fast_path = QtGui.QPainterPath()
#         self._fast_path.moveTo(0, 0)
# 
#         self._slow_path = QtGui.QPainterPath()
#         self._slow_path.moveTo(0, 0)
# 
#         self.graphics = None
#         self.setup_ui(self, queue)
# 
#     def setup_ui(self, widget, queue):
#         widget.setObjectName("DCWidget")
#         widget.resize(*self._dim)
# 
#     def paintEvent(self, e):
#         try:
#             tick, fast, slow = self._queue.get_nowait()
#             fast = fast // self._scale
#             slow = slow // self._scale
#         except Empty:
#             pass
#         else:
#             self._fast_path.lineTo(tick, fast)
#             self._slow_path.lineTo(tick, slow)
# 
#         qp = QtGui.QPainter()
#         qp.begin(self)
#         qp.drawPath(self._fast_path)
#         qp.drawPath(self._slow_path)
#         qp.end()


