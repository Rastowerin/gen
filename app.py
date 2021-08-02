import config
from PyQt5 import QtCore, QtGui, QtWidgets

import matrix


class UiMainWindow(object):

    def __init__(self):
        super(UiMainWindow, self).__init__()

    def setup_ui(self, MainWindow):

        MainWindow.setObjectName('gen')
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1920, 1080)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        MainWindow.setCentralWidget(self.centralwidget)

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 730, 130, 270))
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet('background-color: white;')
        self.textEdit.setObjectName('textEdit')

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, MainWindow)
        self.slider.setGeometry(160, 750, 100, 20)
        self.slider.setObjectName('slider')

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 20))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('gen', 'gen'))


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.__ui = UiMainWindow()
        self.__ui.setup_ui(self)

        self.setStyleSheet('background-color: grey;')

        self.__scene = QtWidgets.QGraphicsScene()
        self.__view = QtWidgets.QGraphicsView(self.__scene, self)
        self.__view.setGeometry(QtCore.QRect(0, 0, 1920, 720))
        self.__view.setStyleSheet('background-color: white;')
        self.__view.setObjectName('view')

        self.__ui.slider.valueChanged[int].connect(self.change_speed)

        self.__food_brush = QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.SolidPattern)
        self.__venom_brush = QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern)
        self.__wall_brush = QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.SolidPattern)
        self.__cell_brush = QtGui.QBrush(QtCore.Qt.blue, QtCore.Qt.SolidPattern)

        self.__brush_dict = {'F': self.__food_brush, 'V': self.__venom_brush,
                             'W': self.__wall_brush, 'C': self.__cell_brush}

        self.__speed = 1000
        self.__matrix = matrix.Matrix(self, config.width, config.height)

        self.__objects = {}
        for __i in range(config.width):
            self.__objects[__i] = {}

        self.create_gird()
        self.showFullScreen()

        self.__timer = QtCore.QTimer(self)
        self.__timer.timeout.connect(self.run)
        self.__timer.start(self.__speed)

    def change_speed(self, speed):
        self.__speed = 1000 - 10 * speed
        self.__timer.setInterval(self.__speed)

    def run(self):
        self.__matrix.run()

    def create_gird(self):
        for i in range(config.height + 1):
            self.create_line(0, i * 10, 10 * config.width, i * 10)
        for i in range(config.width + 1):
            self.create_line(i * 10, 0, i * 10, 10 * config.height)

    def draw_object(self, x, y, sym):

        self.__objects[x][y] = self.__scene.addRect(10 * x, 10 * y, 10, 10, brush=self.__brush_dict[sym])
        self.__view.show()

    def erase_object(self, x, y):
        self.__scene.removeItem(self.__objects[x][y])

    def create_line(self, x1, y1, x2, y2):
        self.__scene.addLine(x1, y1, x2, y2)
        self.__view.show()

    def print_generation_info(self, generation_number, average_lifetime):
        self.__ui.textEdit.append('generation {}\naverage lifetime: {}\n\n'.format(generation_number, average_lifetime))
