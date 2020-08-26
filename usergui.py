import sys
import io
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap
from database.dbuser import User 
import pyqrcode
import png

global usernameVal
global passwordVal
global confpwdVal

usernameVal = ''
usernameMinLength=8
usernameMaxLength=20

passwordVal = ''
confpwdVal = ''
pwdMinLength=8
pwdMaxLength=20

class QRWindow(QWidget):
    def __init__(self, qrImage):
        self.qrimage = qrImage
        
        parent=None
        super(QRWindow,self).__init__(parent)
        
        self.setWindowTitle("MFA QR code")
        
        mainLayout = QVBoxLayout()
        imageLayout = QHBoxLayout()
        imageLayout.setAlignment(Qt.AlignCenter)
        
        label1 = QLabel("Scan the following with your phone's OTP app")
        label2 = QLabel("In practice this QR code will be e-mailed to the user")
        
        imageLabel = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(self.qrimage)
        imageLabel.setPixmap(pixmap)
        imageLayout.addWidget(imageLabel)
        
        okButton = QPushButton("OK",  self)
        okButton.clicked.connect(self.dismissWindow)
        
        mainLayout.addWidget(label1)
        mainLayout.addWidget(label2)
        mainLayout.addLayout(imageLayout)
        mainLayout.addWidget(okButton)
        
        self.setLayout(mainLayout)
        self.resize(300, 300)
        self.move(400, 300)
        
    def dismissWindow(self):
        print("OK button clicked")
        self.close()
        

class UserGui(QWidget):
    def MainWindow(self):
        window = QWidget()
        window.setWindowTitle('Add User')
        window.setGeometry(100, 100, 280, 80)
        window.move(300, 300)

        mainLayout = QVBoxLayout()

        editFieldsLayout = QFormLayout()

        global usernameEdit
        usernameEdit = QLineEdit()
        usernameEdit.textChanged.connect(self.usernameEditChanged)
        editFieldsLayout.addRow('User Name:', usernameEdit)

        global firstPasswordEdit
        firstPasswordEdit = QLineEdit()
        firstPasswordEdit.setEchoMode(QLineEdit.Password)
        firstPasswordEdit.textChanged.connect(self.firstPasswordEditChanged)
        editFieldsLayout.addRow('Password:', firstPasswordEdit)

        global secondPasswordEdit
        secondPasswordEdit = QLineEdit()
        secondPasswordEdit.setEchoMode(QLineEdit.Password)
        editFieldsLayout.addRow('Confirm Password:', secondPasswordEdit)
        secondPasswordEdit.textChanged.connect(self.secondPasswordEditChanged)
        mainLayout.addLayout(editFieldsLayout)

        global buttonsLayout
        buttonsLayout = QDialogButtonBox()
        buttonsLayout.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
        buttonsLayout.accepted.connect(self.okButtonHandler)
        buttonsLayout.rejected.connect(self.cancelButtonHandler)
        mainLayout.addWidget(buttonsLayout)

        window.setLayout(mainLayout)

        window.show()

        sys.exit(app.exec_())

    def cancelButtonHandler(self):
        print('Cancel button clicked!')
        QCoreApplication.quit()
        
    def okButtonHandler(self):
        if passwordVal != confpwdVal:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Password error")
            msg.setInformativeText('Passwords do not match!')
            msg.setWindowTitle("Error")
            msg.exec()
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
         
        dbuser = User();
        dbuser.addUser(usernameVal, passwordVal)
         
        QApplication.restoreOverrideCursor()
        
        self.generateQR()
        
    def usernameEditChanged(self, text):
        global usernameVal, passwordVal, confpwdVal
        
        if len(text)>usernameMaxLength:
            text = text[:usernameMaxLength]
            
        if len(text)>=usernameMinLength and len(text)<=usernameMaxLength:
            usernameVal = text
        else:
            usernameVal = ''
            buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('usernameEditChanged:', usernameVal)
        
        usernameEdit.setText(usernameVal)
        
        if len(usernameVal)>0 and len(passwordVal)>0 and len(confpwdVal)>0:
            buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)

    def firstPasswordEditChanged(self, text):
        global usernameVal, passwordVal, confpwdVal
        
        if len(text)>pwdMaxLength:
            text = text[:pwdMaxLength]
            
        if len(text)>=pwdMinLength and len(text)<=pwdMaxLength:
            passwordVal = text
        else:
            passwordVal = ''
            buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('firstPasswordEditChanged:', passwordVal)
        
        firstPasswordEdit.setText(passwordVal)
        
        if len(usernameVal)>0 and len(passwordVal)>0 and len(confpwdVal)>0:
            buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)

    def secondPasswordEditChanged(self, text):
        global usernameVal, passwordVal, confpwdVal

        if len(text)>pwdMaxLength:
            text = text[:pwdMaxLength]
            
        if len(text)>=pwdMinLength and len(text)<=pwdMaxLength:
            confpwdVal = text
        else:
            confpwdVal = ''
            buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        print('secondPasswordEditChanged:', confpwdVal)
        
        secondPasswordEdit.setText(confpwdVal)
        
        print('usernameVal['+usernameVal+'] passwordVal['+passwordVal+'] confpwdVal['+confpwdVal+']')
        
        if len(usernameVal)>0 and len(passwordVal)>0 and len(confpwdVal)>0:
            buttonsLayout.button(QDialogButtonBox.Ok).setEnabled(True)
            
    def generateQR(self):
        global usernameVal
        
        user = User()
        secret = user.getOtpSecret(usernameVal)
        
        if secret==None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Processing error")
            msg.setInformativeText('Failed to generate QR code!')
            msg.setWindowTitle("Error")
            msg.exec()
            return
            
        myqrcode = pyqrcode.create('otpauth://totp/'+usernameVal+'?secret='+secret)
        
        imgbuffer = io.BytesIO()
        myqrcode.svg(imgbuffer, scale=6)
        self.qrwindow = QRWindow(imgbuffer.getvalue())
        self.qrwindow.show()    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    usergui = UserGui()
    usergui.MainWindow()
