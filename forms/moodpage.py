from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class MoodPage(QMainWindow):
    def __init__(self,mainwindow,conn,curs):
        super(MoodPage,self).__init__()
        uic.loadUi("./ui/moodpage.ui",self)
        self.basewindow  =mainwindow
        self.conn = conn
        self.curs = curs
    def closeEvent(self, event):
        self.basewindow.show()
        self.hide()
        