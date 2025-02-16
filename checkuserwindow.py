import sys
import io
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from database.dbuser import User
import globals

class CheckUserGui(QWidget):
    def __init__(self):
        super().__init__()

        self.usernameVal = ''
        self.passwordVal = ''

        self.window = QWidget()
        self.window.setWindowTitle('Check User')
        self.window.setGeometry(100, 100, 280, 80)
        self.window.move(300, 300)

        self.mainLayout = QVBoxLayout()

        self.editFieldsLayout = QFormLayout()

        self.usernameEdit = QLineEdit()
        self.usernameEdit.textChanged.connect(self.usernameEditChanged)
        self.editFieldsLayout.addRow('User Name:', self.usernameEdit)

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.textChanged.connect(self.passwordEditChanged)
        self.editFieldsLayout.addRow('Password:', self.passwordEdit)

        self.mainLayout.addLayout(self.editFieldsLayout)

        self.buttonsLayout = QDialogButtonBox()
        self.buttonsLayout.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonsLayout.accepted.connect(self.okButtonHandler)
        self.buttonsLayout.rejected.connect(self.cancelButtonHandler)
        self.mainLayout.addWidget(self.buttonsLayout)

        self.setLayout(self.mainLayout)

    def cancelButtonHandler(self):
        print('Cancel button clicked!')
        self.closeWindow()
        
    def okButtonHandler(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
         
        dbuser = User();

        if(dbuser.validateUser(self.usernameVal, self.passwordVal)==False):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("User validation failed")
            msg.setInformativeText('Incorrect user details or user does not exist')
            msg.setWindowTitle("Error")
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("User validated")
            msg.setInformativeText('User is valid')
            msg.setWindowTitle("User")
            msg.exec()

        QApplication.restoreOverrideCursor()
        self.closeWindow()

    def usernameEditChanged(self, text):
        if len(text)>globals.usernameMaxLength:
            text = text[:globals.usernameMaxLength]
            
        if len(text)>=globals.usernameMinLength and len(text)<=globals.usernameMaxLength:
            self.usernameVal = text
        else:
            self.usernameVal = ''
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('usernameEditChanged:', self.usernameVal)
        
        self.usernameEdit.setText(self.usernameVal)
        
        if len(self.usernameVal)>0 and len(self.passwordVal)>0:
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)

    def passwordEditChanged(self, text):
        if len(text)>globals.pwdMaxLength:
            text = text[:globals.pwdMaxLength]
            
        if len(text)>=globals.pwdMinLength and len(text)<=globals.pwdMaxLength:
            self.passwordVal = text
        else:
            self.passwordVal = ''
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('firstPasswordEditChanged:', self.passwordVal)
        
        self.passwordEdit.setText(self.passwordVal)
        
        if len(self.usernameVal)>0 and len(self.passwordVal)>0:
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)

    def closeWindow(self):
        self.usernameVal = ''
        self.passwordVal = ''
        
        self.usernameEdit.setText('')
        self.passwordEdit.setText('')
        
        self.close()
