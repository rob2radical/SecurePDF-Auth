import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
from mail import sendMail
from drawSig import signaturePad


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./ui-Files/SecurePDF-Auth.ui", self)
        self.Browse.clicked.connect(self.browsefiles)
        self.sendEmail.clicked.connect(self.sendMailCode)
        self.signature.clicked.connect(self.Signature)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', '/home/', 'pdf (*.pdf)')
        self.pdfFileInput.setText(fname[0])

    def Signature(self):
        signaturePad()
        print("signature tab open")

    def sendMailCode(self):
        sendMail()
        print("message sent")

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(600)
widget.setFixedHeight(500)
widget.show()
sys.exit(app.exec_())
