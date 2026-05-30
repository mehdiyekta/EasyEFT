from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5 import uic
from forms import exercisepage
from libs.handledatabase import HandleDataBase
import configparser
from PyQt5.QtCore import QTime
from libs.handledate import DateTools
class PostExercise(QMainWindow):
    def __init__(self,main_window,window,conn,cursor,sessionId,probId,endtime,resfolder):
        super(PostExercise,self).__init__()
        uic.loadUi("./ui/postexercise.ui",self)
        self.main_window = main_window
        self.basewindow = window
        self.conn = conn
        self.curs = cursor
        self.sessionId = sessionId
        self.probId = probId
        self.lastIntensity = 0
        self.endtime = endtime
        self.comment = ""
        self.duration =""
        self.problemname = ""
        self.problemfirstintensity =self.lastIntensity
        self.resfolder = resfolder

        self.btnfinish.clicked.connect(self.finish)
        self.btnrestart.clicked.connect(self.restart)
        self.btnfinish.setFocus()
    def restart(self):
        self.validateData()
        self.updateExcersise()
        self.addnew()
        self.restartex = exercisepage.PageExcerize(self,self.basewindow,self.conn,self.curs,self.sessionId,self.probId,self.duration,self.resfolder)
        self.restartex.show()
        self.hide()
    def finish(self):
        self.validateData()
        self.updateExcersise()
        self.basewindow.show()
        self.basewindow.newexcersice()
        self.hide()
    def updateExcersise(self):
        hndldatabase = HandleDataBase(self.conn,self.curs)
        self.resfolder = hndldatabase.fetchResFolderWithProblemId(self.probId)
        problemname = hndldatabase.fetchProblemWithProblemId(self.probId)
        self.problemname = problemname[0][1]
        sessionid = hndldatabase.lastSessionIdFromProblem(str(self.problemname))
        hndldatabase.updateProblemLastintensityWithProblemId(self.probId,self.lastIntensity)
        hndldatabase.updateSessionEndintensityWithSessionId(sessionid,self.lastIntensity)
        hndldatabase.updateSessionEndtimeWithSessionId(sessionid,self.endtime)
        if self.lastIntensity == 0:
            hndldatabase.updateSessionDoneWithSessionId(sessionid,'بله')
            hndldatabase.updateProblemDoneWithProblemId(self.probId,'بله')
        else:
            hndldatabase.updateSessionDoneWithSessionId(sessionid,'خیر')
            hndldatabase.updateProblemDoneWithProblemId(self.probId,'خیر')
        hndldatabase.addCommentTOSession(sessionid,self.comment)
    def addnew(self):
        current_time = QTime.currentTime()
        time_string = current_time.toString("hh:mm:ss")
        dbhandler = HandleDataBase(self.conn,self.curs)
        problemdata = dbhandler.fetchProblemWithProblemId(self.probId)
        self.problemattempts = problemdata[len(problemdata)-1][9]
        self.problemattempts = int(self.problemattempts) +1
        dbhandler.editExistingProblemAttempt(self.problemattempts,self.probId)
        dateobj = DateTools()
        current_date = dateobj.justDate()
        self.duration = dbhandler.fetchDurationBySessionId(sessionid=self.sessionId)
        dbhandler.addNewSession(self.problemname,self.duration,time_string,None,self.problemfirstintensity,None,None,current_date,None)
    def validateData(self):
        self.lastIntensity = self.sbfinalintensity.value()
        if self.lastIntensity == 0 :
            QMessageBox.information(None,"تبریک!","تبریک میگوییم، شما با موفقیت مشکل را خنثی نمودید!")
        else:
            pass
        tempcomment = self.tecomment.toPlainText()
        if tempcomment=="":
            self.comment = None
        else:
            self.comment = tempcomment
    def closeEvent(self,event):
        self.finish()