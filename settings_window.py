from PyQt5 import QtCore, QtGui, QtWidgets
import user_settings


class SettingsWindow(QtWidgets.QWidget):

    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.setFixedSize(280, 405)
        self.setWindowTitle('settings')
        self.setWindowModality(QtCore.Qt.NonModal)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setStyleSheet('background-color: grey;')

        self.SizeLabel = QtWidgets.QLabel(self)
        self.SizeLabel.setText('field size:')
        self.SizeLabel.setFont(QtGui.QFont('Arial', 15))
        self.SizeLabel.setGeometry(QtCore.QRect(10, 10, 200, 20))

        self.WidthInput = QtWidgets.QLineEdit(self)
        self.WidthInput.setStyleSheet('background-color: white;')
        self.WidthInput.setText(str(user_settings.width))
        self.WidthInput.setValidator(QtGui.QIntValidator(1, 1000))
        self.WidthInput.setGeometry(QtCore.QRect(170, 13, 40, 20))

        self.XSepLabel = QtWidgets.QLabel(self)
        self.XSepLabel.setText('x')
        self.XSepLabel.setFont(QtGui.QFont('Arial', 15))
        self.XSepLabel.setGeometry(215, 10, 40, 20)

        self.HeightInput = QtWidgets.QLineEdit(self)
        self.HeightInput.setStyleSheet('background-color: white;')
        self.HeightInput.setText(str(user_settings.height))
        self.HeightInput.setValidator(QtGui.QIntValidator(1, 1000))
        self.HeightInput.setGeometry(QtCore.QRect(230, 13, 40, 20))

        self.FoodLabel = QtWidgets.QLabel(self)
        self.FoodLabel.setText('number of food:')
        self.FoodLabel.setFont(QtGui.QFont('Arial', 15))
        self.FoodLabel.setGeometry(QtCore.QRect(10, 50, 200, 20))

        self.FoodInput = QtWidgets.QLineEdit(self)
        self.FoodInput.setStyleSheet('background-color: white;')
        self.FoodInput.setText(str(user_settings.food_number))
        self.FoodInput.setValidator(QtGui.QIntValidator(1, 1000000))
        self.FoodInput.setGeometry(QtCore.QRect(200, 51, 40, 20))

        self.VenomLabel = QtWidgets.QLabel(self)
        self.VenomLabel.setText('number of venom:')
        self.VenomLabel.setFont(QtGui.QFont('Arial', 15))
        self.VenomLabel.setGeometry(QtCore.QRect(10, 90, 200, 20))

        self.VenomInput = QtWidgets.QLineEdit(self)
        self.VenomInput.setStyleSheet('background-color: white;')
        self.VenomInput.setText(str(user_settings.venom_number))
        self.VenomInput.setValidator(QtGui.QIntValidator(1, 1000000))
        self.VenomInput.setGeometry(QtCore.QRect(200, 91, 40, 20))

        self.WallLabel = QtWidgets.QLabel(self)
        self.WallLabel.setText('number of walls:')
        self.WallLabel.setFont(QtGui.QFont('Arial', 15))
        self.WallLabel.setGeometry(QtCore.QRect(10, 130, 200, 20))

        self.WallInput = QtWidgets.QLineEdit(self)
        self.WallInput.setStyleSheet('background-color: white;')
        self.WallInput.setText(str(user_settings.walls_number))
        self.WallInput.setValidator(QtGui.QIntValidator(1, 1000000))
        self.WallInput.setGeometry(QtCore.QRect(200, 131, 40, 20))

        self.CellLabel = QtWidgets.QLabel(self)
        self.CellLabel.setText('number of cells:')
        self.CellLabel.setFont(QtGui.QFont('Arial', 15))
        self.CellLabel.setGeometry(QtCore.QRect(10, 170, 200, 20))

        self.CellInput = QtWidgets.QLineEdit(self)
        self.CellInput.setStyleSheet('background-color: white;')
        self.CellInput.setText(str(user_settings.cells_number))
        self.CellInput.setValidator(QtGui.QIntValidator(1, 1000000))
        self.CellInput.setGeometry(QtCore.QRect(200, 171, 40, 20))

        self.StartHpLabel = QtWidgets.QLabel(self)
        self.StartHpLabel.setText('start hit points:')
        self.StartHpLabel.setFont(QtGui.QFont('Arial', 15))
        self.StartHpLabel.setGeometry(QtCore.QRect(10, 210, 200, 20))

        self.StartHpInput = QtWidgets.QLineEdit(self)
        self.StartHpInput.setStyleSheet('background-color: white;')
        self.StartHpInput.setText(str(user_settings.start_hp))
        self.StartHpInput.setValidator(QtGui.QIntValidator(1, 1000))
        self.StartHpInput.setGeometry(QtCore.QRect(200, 211, 40, 20))

        self.MaxHpLabel = QtWidgets.QLabel(self)
        self.MaxHpLabel.setText('maximum hit points:')
        self.MaxHpLabel.setFont(QtGui.QFont('Arial', 15))
        self.MaxHpLabel.setGeometry(QtCore.QRect(10, 250, 200, 20))

        self.MaxHpInput = QtWidgets.QLineEdit(self)
        self.MaxHpInput.setStyleSheet('background-color: white;')
        self.MaxHpInput.setText(str(user_settings.max_hp))
        self.MaxHpInput.setValidator(QtGui.QIntValidator(1, 1000))
        self.MaxHpInput.setGeometry(QtCore.QRect(200, 251, 40, 20))

        self.ChildrenLabel = QtWidgets.QLabel(self)
        self.ChildrenLabel.setText('children per parent:')
        self.ChildrenLabel.setFont(QtGui.QFont('Arial', 15))
        self.ChildrenLabel.setGeometry(QtCore.QRect(10, 290, 200, 20))

        self.ChildrenInput = QtWidgets.QLineEdit(self)
        self.ChildrenInput.setStyleSheet('background-color: white;')
        self.ChildrenInput.setText(str(user_settings.selection))
        self.ChildrenInput.setValidator(QtGui.QIntValidator(1, 1000))
        self.ChildrenInput.setGeometry(QtCore.QRect(200, 291, 40, 20))

        self.MutantLabel = QtWidgets.QLabel(self)
        self.MutantLabel.setText('children per parent:')
        self.MutantLabel.setFont(QtGui.QFont('Arial', 15))
        self.MutantLabel.setGeometry(QtCore.QRect(10, 330, 200, 20))

        self.MutantInput = QtWidgets.QLineEdit(self)
        self.MutantInput.setStyleSheet('background-color: white;')
        self.MutantInput.setText(str(user_settings.mutants_per_cell))
        self.MutantInput.setValidator(QtGui.QIntValidator(1, 1000))
        self.MutantInput.setGeometry(QtCore.QRect(200, 331, 40, 20))

        self.AcceptButton = QtWidgets.QPushButton(self)
        self.AcceptButton.setStyleSheet('background-color: white;')
        self.AcceptButton.setText('accept')
        self.AcceptButton.setGeometry(QtCore.QRect(95, 365, 90, 30))
        self.AcceptButton.clicked.connect(self.load)

    def load(self):

        if int(self.FoodInput.text()) + int(self.VenomInput.text()) +\
                int(self.WallInput.text()) + int(self.CellInput.text()) > \
                int(self.WidthInput.text()) * int(self.HeightInput.text()):
            return

        user_settings.width = int(self.WidthInput.text())
        user_settings.height = int(self.HeightInput.text())
        user_settings.food_number = int(self.FoodInput.text())
        user_settings.venom_number = int(self.VenomInput.text())
        user_settings.walls_number = int(self.WallInput.text())
        user_settings.cells_number = int(self.CellInput.text())
        user_settings.start_hp = int(self.StartHpInput.text())
        user_settings.max_hp = int(self.MaxHpInput.text())
        user_settings.selection = int(self.CellInput.text())
        user_settings.mutants_per_cell = int(self.MutantInput.text())

        self.destroy()
