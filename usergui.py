import sys
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from adduserwindow import AddUserGui
from checkuserwindow import CheckUserGui

class AppGui(QWidget):
    def __init__(self):
        super().__init__()

        self.addusergui = AddUserGui()
        self.checkusergui = CheckUserGui()

        self.window = QWidget()
        self.window.setWindowTitle('User Management')
        self.window.setGeometry(100, 100, 280, 80)
        self.window.move(300, 300)

        self.mainLayout = QVBoxLayout()

        self.editFieldsLayout = QFormLayout()

        self.addUserButton = QPushButton(self.tr("&Add User"))
        self.addUserButton.clicked.connect(self.ButtonHandler)

        self.checkUserButton = QPushButton(self.tr("&Check User"))
        self.checkUserButton.clicked.connect(self.ButtonHandler)

        self.exitButton = QPushButton(self.tr("&Exit"))
        self.exitButton.clicked.connect(self.ButtonHandler)

        self.buttonsLayout = QDialogButtonBox()
        self.buttonsLayout.addButton(self.addUserButton, QDialogButtonBox.ActionRole)
        self.buttonsLayout.addButton(self.checkUserButton, QDialogButtonBox.ActionRole)
        self.buttonsLayout.addButton(self.exitButton, QDialogButtonBox.ActionRole)

        self.mainLayout.addWidget(self.buttonsLayout)

        self.setLayout(self.mainLayout)
        self.show()

    def ButtonHandler(self):
        sender = self.sender()

        if sender.text() == '&Add User':
            print('Add user button pressed')
            self.addusergui.show()
        elif sender.text() == '&Check User':
            print('Check user button pressed')
            self.checkusergui.show()
        elif sender.text() == '&Exit':
            print('Exit button pressed')
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    usergui = AppGui()
    sys.exit(app.exec())
    
