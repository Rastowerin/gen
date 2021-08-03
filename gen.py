from PyQt5 import QtWidgets
import sys
import app

application = QtWidgets.QApplication(sys.argv)
window = app.Window()
sys.exit(application.exec())
