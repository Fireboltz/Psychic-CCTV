from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton
from PyQt5 import uic
import sys

class UI_selection_screen(QMainWindow):
    def __init__(self):
        super(UI_selection_screen,self).__init__
        uic.loadUi('UI/main_screen.ui',self)
        self.show()
        
