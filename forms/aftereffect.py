from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from libs.handledatabase import HandleDataBase
from libs.handledate import DateTools
class AfterEffects(QMainWindow):
    def __init__(self,mainwindow,basewindow,conn,curs,data,data2):
        super(AfterEffects,self).__init__()
        uic.loadUi("./ui/aftereffects.ui",self)
        self.main_window = mainwindow
        self.basewindow = basewindow
        self.data = data
        self.data2 = data2
        self.conn = conn
        self.curs = curs
        self.btnsubmit.clicked.connect(self.ok)
        self.problem = ""
        self.problemtype = ""
        self.problemcategory = ""
        self.lemother.setText(str(self.data2['problem']))
    def ok(self):
        self.validateData()
        self.updatedb()
        self.main_window.resume()
        self.hide()
    def validateData(self):
        dt = DateTools()
        after = self.leaftereffect.text()
        if after== "":
            return
        else:
            self.problem = after
        intensity = self.spinBox.value()
        self.problemcategory = self.data2['category']
        self.problemrelateto = self.data2['problem']
        self.duration = self.data2['duration']
        self.additionaldata = ""
        self.problemintensity = intensity
        self.attempts = 1
        self.date = dt.justDate()
        self.resfolder = "."
    def updatedb(self):
        dbhandler = HandleDataBase(self.conn,self.curs)
        dbhandler.addNewExercise(self.problem,self.problemtype,self.problemcategory,self.problemrelateto,self.duration,self.additionaldata,self.problemintensity,None,self.attempts
                                 ,self.date,None,self.resfolder)