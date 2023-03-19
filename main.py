# GRAPHS' PROJECT
# DANIEL EDUARDO MACIAS ESTRADA (danma22)
# MAURICIO HERNÁNDEZ CEPEDA (mauriciohc02)

import sys
from utils.appUI import AppUI
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Graphs')

    myApp = AppUI()
    myApp.show()

    sys.exit(app.exec())
