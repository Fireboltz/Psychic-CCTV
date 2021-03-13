from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QAction,QTextBrowser
from PyQt5 import uic
import sys
from Selection_screen import UI_selection_screen

class Ui(QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('UI/intro_screen.ui',self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.main_screen)
        self.show()
    def main_screen(self):
         uic.loadUi('UI/main_screen.ui',self)
         self.button = self.findChild(QTextBrowser,"textBrowser")
         self.button.QAction("&Editor",self)
         self.button.clicked.connect(self.file_open)
         
         self.show()
        
    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        file = open(name,'r')

        self.editor()

        with file:
            text = file.read()
            self.textEdit.setText(text)
app = QApplication(sys.argv)
window = Ui()
sys.exit(app.exec_())