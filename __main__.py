if __name__ != '__main__':
    raise Exception('Wrong use mutherfucker, unimportable module!')
else:
    import sys

    from utils import set_environment
    set_environment()

    from PyQt5 import QtWidgets

    from controllers import MainController
    from main_view import MainView

    class MainApp(QtWidgets.QApplication):
        def __init__(self, sys_argv):
            super(MainApp, self).__init__(sys_argv)

            self.controller = MainController()
            # The view will instantiate each subview?
            self.view = MainView(self.controller)
            self.view.show()

    app = MainApp(sys.argv)
    sys.exit(app.exec_())
