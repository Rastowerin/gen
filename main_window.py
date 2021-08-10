from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import user_settings


class UiMainWindow(object):

    def __init__(self):
        super(UiMainWindow, self).__init__()

    def setup_ui(self, MainWindow):

        MainWindow.setObjectName('gen')
        MainWindow.setWindowModality(QtCore.Qt.NonModal)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        MainWindow.setCentralWidget(self.centralwidget)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, MainWindow)
        self.view.setStyleSheet('background-color: white;')
        self.view.setObjectName('view')

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet('background-color: white;')
        self.textEdit.setObjectName('textEdit')

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, MainWindow)
        self.slider.setObjectName('slider')

        self.VisModButton = QtWidgets.QPushButton(MainWindow)
        self.VisModButton.setStyleSheet('background-color: white;')
        self.VisModButton.setText('vis off')

        self.StartButton = QtWidgets.QPushButton(MainWindow)
        self.StartButton.setStyleSheet('background-color: white;')
        self.StartButton.setText('start')

        self.SettingsButton = QtWidgets.QPushButton(MainWindow)
        self.SettingsButton.setStyleSheet('background-color: white;')
        self.SettingsButton.setText('settings')

        self.AverageInput = QtWidgets.QLineEdit(MainWindow)
        self.AverageInput.setStyleSheet('background-color: white;')
        self.AverageInput.setText(str(user_settings.average_range))
        self.AverageInput.setValidator(QtGui.QIntValidator(1, 1000))

        self.SaveButton = QtWidgets.QPushButton(MainWindow)
        self.SaveButton.setStyleSheet('background-color: white;')
        self.SaveButton.setText('save')

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 20))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.pltCanvas = FigureCanvas(plt.Figure())
        self.ax = self.pltCanvas.figure.add_subplot(111)
        self.pltCanvas.setParent(MainWindow)
        self.pltCanvas.draw()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('gen', 'gen'))
