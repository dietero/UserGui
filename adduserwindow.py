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
import pyqrcode
from qrwindow import QRWindow
import globals

class AddUserGui(QWidget):
    def __init__(self):
        super().__init__()

        self.usernameVal = ''
        self.passwordVal = ''
        self.confpwdVal = ''

        self.window = QWidget()
        self.window.setWindowTitle('Add User')
        self.window.setGeometry(100, 100, 280, 80)
        self.window.move(300, 300)

        self.mainLayout = QVBoxLayout()

        self.editFieldsLayout = QFormLayout()

        self.usernameEdit = QLineEdit()
        self.usernameEdit.textChanged.connect(self.usernameEditChanged)
        self.editFieldsLayout.addRow('User Name:', self.usernameEdit)

        self.firstPasswordEdit = QLineEdit()
        self.firstPasswordEdit.setEchoMode(QLineEdit.Password)
        self.firstPasswordEdit.textChanged.connect(self.firstPasswordEditChanged)
        self.editFieldsLayout.addRow('Password:', self.firstPasswordEdit)

        self.secondPasswordEdit = QLineEdit()
        self.secondPasswordEdit.setEchoMode(QLineEdit.Password)
        self.editFieldsLayout.addRow('Confirm Password:', self.secondPasswordEdit)
        self.secondPasswordEdit.textChanged.connect(self.secondPasswordEditChanged)
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
        if self.passwordVal != self.confpwdVal:
            self.passwordVal = ''
            self.firstPasswordEdit.setText(self.passwordVal)

            self.confpwdVal = ''
            self.secondPasswordEdit.setText(self.passwordVal)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Password error")
            msg.setInformativeText('Passwords do not match!')
            msg.setWindowTitle("Error")
            msg.exec()
            self.closeWindow()
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
         
        dbuser = User();
        if(dbuser.addUser(self.usernameVal, self.passwordVal)==False):
            print('Failed to add user!')
         
        QApplication.restoreOverrideCursor()
        
        self.generateQR()
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
        
        if len(self.usernameVal)>0 and len(self.passwordVal)>0 and len(self.confpwdVal)>0:
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)

    def firstPasswordEditChanged(self, text):
        if len(text)>globals.pwdMaxLength:
            text = text[:globals.pwdMaxLength]
            
        if len(text)>=globals.pwdMinLength and len(text)<=globals.pwdMaxLength:
            self.passwordVal = text
        else:
            self.passwordVal = ''
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('firstPasswordEditChanged:', self.passwordVal)
        
        self.firstPasswordEdit.setText(self.passwordVal)
        
        if len(self.usernameVal)>0 and len(self.passwordVal)>0 and len(self.confpwdVal)>0:
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)

    def secondPasswordEditChanged(self, text):
        if len(text)>globals.pwdMaxLength:
            text = text[:globals.pwdMaxLength]
            
        if len(text)>=globals.pwdMinLength and len(text)<=globals.pwdMaxLength:
            self.confpwdVal = text
        else:
            self.confpwdVal = ''
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('secondPasswordEditChanged:', self.confpwdVal)
        
        self.secondPasswordEdit.setText(self.confpwdVal)
        
        print('usernameVal['+self.usernameVal+'] passwordVal['+self.passwordVal+'] confpwdVal['+self.confpwdVal+']')
        
        if len(self.usernameVal)>0 and len(self.passwordVal)>0 and len(self.confpwdVal)>0:
            self.buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)
            
    def generateQR(self):
        user = User()
        secret = user.getOtpSecret(self.usernameVal)
        
        if secret==None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Processing error")
            msg.setInformativeText('Failed to generate QR code!')
            msg.setWindowTitle("Error")
            msg.exec()
            return
            
        myqrcode = pyqrcode.create('otpauth://totp/'+self.usernameVal+'?secret='+secret)
        
        imgbuffer = io.BytesIO()
        myqrcode.svg(imgbuffer, scale=6)
        self.qrwindow = QRWindow(imgbuffer.getvalue())
        self.qrwindow.show()

    def closeWindow(self):
        self.usernameVal = ''
        self.passwordVal = ''
        self.confpwdVal = ''

        self.usernameEdit.setText('')
        self.firstPasswordEdit.setText('')
        self.secondPasswordEdit.setText('')

        self.close()