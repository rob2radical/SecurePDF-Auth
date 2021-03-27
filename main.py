import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QPushButton
from PyQt5.uic import loadUi
from mail import sendMail

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./ui-Files/SecurePDF-Auth.ui", self)
        self.Browse.clicked.connect(self.browsefiles)
        self.sendEmail.clicked.connect(self.sendMailCode)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', '/home/', 'pdf (*.pdf)')
        self.pdfFileInput.setText(fname[0])

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
