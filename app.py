from PyQt5 import QtCore, QtGui, QtWidgets
import main_window
import settings_window
import matrix
import user_settings


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.__ui = main_window.UiMainWindow()
        self.__ui.setup_ui(self)

        self.__width = 1000
        self.__height = 600
        self.resize(self.__width, self.__height)
        self.setMinimumSize(self.__width, self.__height)

        self.__width_factor = 1
        self.__height_factor = 1

        self.setStyleSheet('background-color: grey;')

        self.__ui.slider.valueChanged[int].connect(self.change_speed)

        self.__food_brush = QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.SolidPattern)
        self.__venom_brush = QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern)
        self.__wall_brush = QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.SolidPattern)
        self.__cell_brush = QtGui.QBrush(QtCore.Qt.blue, QtCore.Qt.SolidPattern)

        self.__brush_dict = {'F': self.__food_brush, 'V': self.__venom_brush,
                             'W': self.__wall_brush, 'C': self.__cell_brush}

        self.__visualisation_disabled = False
        self.__started = False

        self.__speed = 990
        self.__matrix = matrix.Matrix(self, user_settings.width, user_settings.height)

        self.__objects = {}
        for __i in range(user_settings.width):
            self.__objects[__i] = {}

        self.__ui.StartButton.clicked.connect(self.start)
        self.__ui.SettingsButton.clicked.connect(self.open_settings_window)
        self.__ui.AverageInput.textChanged.connect(self.change_average_range)

        self.show()

    def resizeEvent(self, event):

        self.__width_factor = self.rect().width() / 1000
        self.__height_factor = self.rect().height() / 600

        width = self.__width * self.__width_factor
        height = self.__height * self.__height_factor

        self.__ui.view.setGeometry(QtCore.QRect(0, 0, width, 35 / 60 * height))
        self.__ui.textEdit.setGeometry(QtCore.QRect(0.02 * width, 36 / 60 * height, 0.13 * width, 17 / 60 * height))
        self.__ui.slider.setGeometry(QtCore.QRect(0.02 * width, 53 / 60 * height, 0.13 * width, 1 / 30 * height))
        self.__ui.VisModButton.setGeometry(QtCore.QRect(0.16 * width, 361 / 600 * height, 0.1 * width, 1 / 20 * height))
        self.__ui.StartButton.setGeometry(QtCore.QRect(0.02 * width, 560 / 600 * height, 0.95 * width, 1 / 30 * height))
        self.__ui.SettingsButton.setGeometry(QtCore.QRect(0.16 * width, 401 / 600 * height, 0.1 * width, 1 / 20 * height))
        self.__ui.AverageInput.setGeometry(QtCore.QRect(0.16 * width, 441 / 600 * height, 0.1 * width, 1 / 30 * height))
        self.__ui.pltCanvas.move(0.27 * width, 6 / 10 * height)
        self.__ui.pltCanvas.resize(0.7 * width, 19 / 60 * height)
        self.__ui.pltCanvas.draw()

        super(Window, self).resizeEvent(event)

    def open_settings_window(self):
        self.__settings = settings_window.SettingsWindow()
        self.__settings.show()

    def change_average_range(self):
        user_settings.average_range = int(self.__ui.AverageInput.text())

    def change_speed(self, speed):
        self.__speed = 990 - 10 * speed
        if self.__visualisation_disabled or not self.__started:
            return
        self.__timer.setInterval(self.__speed)

    def change_vis_mode(self):

        if self.__visualisation_disabled:

            list(map(lambda object: self.draw_object(*object.get_cords(), str(object)),
                     self.__matrix.get_all_objects()))
            self.__timer.setInterval(self.__speed)
            self.__ui.VisModButton.setText('vis off')

        else:

            list(map(lambda object: self.erase_object(*object.get_cords()), self.__matrix.get_all_objects()))
            self.__timer.setInterval(0)
            self.__ui.VisModButton.setText('vis on')

        self.__visualisation_disabled = not self.__visualisation_disabled

    def set_plot(self, xarray, yarray):
        self.__ui.ax.clear()
        self.__ui.ax.plot(xarray, yarray)
        self.__ui.pltCanvas.draw()

    def start(self):
        self.__started = True

        self.__ui.VisModButton.clicked.connect(self.change_vis_mode)
        self.__ui.SettingsButton.hide()

        self.create_gird()
        self.__timer = QtCore.QTimer(self)
        self.__timer.timeout.connect(self.run)
        self.__timer.start(self.__speed)

    def run(self):
        self.__matrix.run()

    def create_gird(self):
        for i in range(user_settings.height + 1):
            self.create_line(0, i * 10, 10 * user_settings.width, i * 10)
        for i in range(user_settings.width + 1):
            self.create_line(i * 10, 0, i * 10, 10 * user_settings.height)

    def draw_object(self, x, y, sym):
        if self.__visualisation_disabled:
            return
        self.__objects[x][y] = self.__ui.scene.addRect(10 * x, 10 * y, 10, 10, brush=self.__brush_dict[sym])
        self.__ui.view.show()

    def erase_object(self, x, y):
        if self.__visualisation_disabled:
            return
        try:
            self.__ui.scene.removeItem(self.__objects[x][y])
        except KeyError:
            pass

    def create_line(self, x1, y1, x2, y2):
        self.__ui.scene.addLine(x1, y1, x2, y2)
        self.__ui.view.show()

    def print_generation_info(self, generation_number, average_lifetime):
        self.__ui.textEdit.append('generation {}\naverage lifetime: {}\n\n'.format(generation_number, average_lifetime))
