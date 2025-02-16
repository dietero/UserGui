from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap

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