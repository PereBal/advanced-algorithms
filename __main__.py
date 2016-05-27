if __name__ != '__main__':
    raise Exception('Wrong use mutherfucker, unimportable module!')
else:
    from utils import set_environment; set_environment()

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

app = QApplication(sys.argv)

screen = MainForm()
screen.show()

sys.exit(app.exec_())
