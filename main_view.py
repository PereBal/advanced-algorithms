from functools import partial
from PyQt5 import QtWidgets

from ui_main_view import Ui_MainWindow
from list_view import ListView

from nqueens.nqueens_view import NQueensView
from divide_and_conquer.dc_view import DCView
from greedy.greedy_view import GreedyView
from spelling_checker.sp_view import SpCheckerView
from probabilistic.probabilistic_view import ProbabilisticView

class MainView(QtWidgets.QMainWindow):
    WIDGETS = {
        'QU': NQueensView,
        'DC': DCView,
        'GR': GreedyView,
        'SP': SpCheckerView,
        'PR': ProbabilisticView,
    }

    def __init__(self, controller, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.controller = controller
        self._old_size = None
        self.setup_ui()

    def switch_to(self, widget_key):
        instance = self.instances[widget_key]

        if instance != self.ui.stackedWidget.currentWidget():
            if self._old_size:
                self.resize(self._old_size)
                self._old_size = None

            instance.controller.pre_switch()

            self.ui.stackedWidget.setCurrentWidget(instance)

    def setup_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.instances = {key: widget.as_view(self)
                          for key, widget in self.WIDGETS.items()}

        for instance in self.instances.values():
            self.ui.stackedWidget.addWidget(instance)

        func = {widget: partial(self.switch_to, widget)
                for widget in self.WIDGETS}

        self.ui.action_queens.triggered.connect(func['QU'])
        self.ui.action_dc.triggered.connect(func['DC'])
        self.ui.action_greedy.triggered.connect(func['GR'])
        self.ui.action_sp.triggered.connect(func['SP'])
        self.ui.action_probabilistic.triggered.connect(func['PR'])

        # Let's add the list view!
        lview = ListView.as_view(self)
        self.ui.stackedWidget.addWidget(lview)
        self.ui.stackedWidget.setCurrentWidget(lview)
