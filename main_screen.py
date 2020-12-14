import sys

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,QPushButton, QApplication,QFileDialog,QLabel)
from PyQt5.QtGui import QFont

class window_builder(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('Open_File ',self)
        btn1.clicked.connect(self.getfiles)
        file_label = QLabel("Selected_File")
        file_label.move(50,50)
        btn1.move(50,100)
        self.setGeometry(300,300,380,250)
        self.setWindowTitle('Tooltips')
        self.show()
    
    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        
        filenames = []
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            return filenames
        else:
            return 0


def main():

    app = QApplication(sys.argv)
    wd = window_builder()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    

