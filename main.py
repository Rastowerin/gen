from PyQt5 import QtWidgets
import sys
import matrix
import config
import app

application = QtWidgets.QApplication([])
window = app.Window()
sys.exit(application.exec())
