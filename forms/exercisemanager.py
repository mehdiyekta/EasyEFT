from PyQt5.QtWidgets import QMainWindow,QMessageBox,QTableWidgetItem,QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QTime
from forms import exercisepage
from libs.handledatabase import HandleDataBase
from libs.handledate import DateTools
import configparser

class ExcesiseManager(QMainWindow):
    def __init__(self,main_window,conn,cursor,problem):
        super(ExcesiseManager,self).__init__()
        uic.loadUi("./ui/exercisemanager.ui",self)
        self.main_window = main_window
        self.problem = problem
        self.curs = cursor
        self.conn = conn
        self.btnback.clicked.connect(self.back)
        self.btnrestart.clicked.connect(self.again)
        self.btnrestart.setFocus()
        self.btneditaddress.clicked.connect(self.showDialog)
        #variables
        self.problemid = ""
        self.problemname = ""
        self.problemtype = ""
        self.problemcategory = ""
        self.problemrelate = ""
        self.problemduration = ""
        self.problemadditional = ""
        self.problemfirstintensity = ""
        self.problemlastintensity=""
        self.problemattempts = ""
        self.problemdate = ""
        self.problemdone = ""
        self.problem_Id =""
        self.session_Id=""
        self.Resf = ""
        #

        self.getdata()
    def showDialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.Resf = folder
            self.leaddress.setText(str(self.Resf))
            dbhandler = HandleDataBase(self.conn,self.curs)
            probid = dbhandler.getProblemIdFromProblem(self.problem)
            dbhandler.updateResFolderWithProblemId(self.Resf,probid)
    def addData(self):
        current_time = QTime.currentTime()
        time_string = current_time.toString("hh:mm:ss")
        dbhandler = HandleDataBase(self.conn,self.curs)
        self.problemattempts = int(self.problemattempts) +1
        dbhandler.editExistingProblemAttempt(self.problemattempts,self.problemid)
        dateobj = DateTools()
        current_date = dateobj.justDate()
        # dbhandler.addNewExercise(self.problemname,self.problemtype,self.problemcategory,self.problemrelate,self.problemduration,self.problemadditional,self.problemfirstintensity,None,self.problemattempts
        #                          ,self.problemdate,None)
        dbhandler.addNewSession(self.problemname,self.problemduration,time_string,None,self.problemfirstintensity,None,None,current_date,None)
        self.problem_Id = dbhandler.getProblemIdFromProblem(self.problem)
        self.session_Id = dbhandler.getSessionIdFromProblem(self.problem)
    def again(self):
        self.addData()
        self.pexrcize = exercisepage.PageExcerize(self,self.main_window,self.conn,self.curs,self.session_Id,self.problem_Id,self.problemduration,self.Resf)
        self.pexrcize.show()
        self.hide()
    def back(self):
        self.main_window.show()
        self.hide()
    def getdata(self):
        dbobj = HandleDataBase(self.conn,self.curs)
        problemid = dbobj.getProblemIdFromProblem(self.problem)
        problemdata = dbobj.fetchProblemWithProblemId(problemid)
        sessiondata = dbobj.fetchSessionWithProblem(self.problem)
        self.Resf = dbobj.fetchResFolderWithProblemId(problemid)
        self.leaddress.setText(self.Resf)
        self.validatedata(problemdata,sessiondata)
    def showdata(self):
        self.lblmemory.setText(self.problemname)
        self.lbltype.setText(self.problemtype)
        self.lblcategory.setText(self.problemcategory)
        self.lbllastintensity.setText(self.problemfirstintensity)
        self.lblattempt.setText(self.problemattempts)
    def validatedata(self,data,data2):
        for dat in data:
            self.problemid = dat[0]
            self.problemname = dat[1]
            self.problemtype = dat[2]
            self.problemcategory = dat[3]
            self.problemrelate = dat[4]
            self.problemduration = dat[5]
            self.problemadditional = dat[6]
            self.problemfirstintensity = dat[7]
            self.problemlastintensity=dat[8]
            self.problemattempts = dat[9]
            self.problemdate = dat[10]
            self.problemdone = dat[11]
        self.twex.setRowCount(0)
        self.twex.setRowCount(len(data2))
        row2 = 0
        for dat2 in data2:
            problemid = dat[0]
            problemfirstintensity = dat2[5]
            problemfinalintensity = dat2[6]
            problemstarttime = dat2[3]
            problemendtime = dat2[4]
            problemduriation = dat2[2]
            problemdate = dat2[8]
            self.twex.setItem(row2, 0, QTableWidgetItem(str(problemid)))
            self.twex.setItem(row2, 1, QTableWidgetItem(str(problemfirstintensity)))
            self.twex.setItem(row2, 2, QTableWidgetItem(str(problemfinalintensity)))
            self.twex.setItem(row2, 3, QTableWidgetItem(str(problemstarttime)))
            self.twex.setItem(row2, 4, QTableWidgetItem(str(problemendtime)))
            self.twex.setItem(row2, 5, QTableWidgetItem(str(problemduriation)))
            self.twex.setItem(row2, 6, QTableWidgetItem(str(problemdate)))
            row2 += 1
        
        self.showdata()

    def closeEvent(self,event):
        self.main_window.show()
        self.hide()