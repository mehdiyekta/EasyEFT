from PyQt5.QtWidgets import QMainWindow,QMessageBox,QFileDialog
from PyQt5.QtCore import QTime
from PyQt5 import uic
from forms import exercisepage
from libs.handledatabase import HandleDataBase
from libs.handledate import DateTools
from libs.handleai import HandleAI
from pathlib import Path
import sys
import os
import configparser
class NewExcerize(QMainWindow):
    def __init__(self,main_window,conn,curs):
        super(NewExcerize,self).__init__()
        uic.loadUi("./ui/newexcersize.ui",self)
        self.main_window = main_window
        self.conn = conn
        self.curs = curs
        self.frmd.setVisible(False)
        self.btnstart.clicked.connect(self.validateEnteries)
        self.btnback.clicked.connect(self.backmainpage)
        self.frmmanualtime.setVisible(False)
        self.sbsec.valueChanged.connect(self.controllSpinBox)
        self.sbminut.valueChanged.connect(self.controllSpinBox)
        self.lesearchmem.textChanged.connect(self.searchmem)
        self.btnfiledialog.clicked.connect(self.showDialog)
        #variables:
        self.problem = ""
        self.problemtype = ""
        self.problemcategory = ""
        self.problemintensity = 0
        self.problemrelateto = ""
        self.additionaldata = ""
        self.duration = "00:30"
        self.date = ""
        self.sessionId = ""
        self.problemId = ""
        self.resfolder = "."
    def showDialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.resfolder = folder
            self.leadress.setText(str(self.resfolder))
    def searchmem(self):
        memforsearch = self.lesearchmem.text()
        hndlai = HandleAI(self.conn,self.curs)
        res =hndlai.search_similar_text(memforsearch)
        if res:
            self.lwsearch.clear()
            self.lwsearch.addItem(res)
        else:
            pass
    def startexercise(self):
        self.pexrcize = exercisepage.PageExcerize(self,self.main_window,self.conn,self.curs,self.sessionId,self.problemId,self.duration,self.resfolder)
        self.pexrcize.show()
        self.hide()
    def backmainpage(self):
        self.hide()
        self.main_window.show()
    def validateEnteries(self):
        problame = self.leprobname.text()
        if problame == "":
            QMessageBox.critical(None,"خطا","لطفا نام خاطره یا مشکل را وارد کنید")
            return
        else:
            self.problem = problame
        problemtype,tid = self.getProblemType()
        if tid == 0:
            QMessageBox.critical(None,"خطا","لطفا نوع مشکل خود را انتخاب نمایید")
            return
        else:
            self.problemtype = problemtype
        problemcategory,cid = self.getProblemCategory()
        if cid == 0:
            QMessageBox.critical(None,"خطا","لطفا برای مشکل خود یک دسته بندی انتخاب کنید.")
            return
        else:
            self.problemcategory = problemcategory
        self.problemintensity = self.getProblemIntensity()
        if self.cbrelate.isChecked()== True:
            try:
                self.problemrelateto =  self.lwsearch.currentItem().text()
                if self.problemrelateto is None:
                    raise Exception
            except Exception:
                QMessageBox.warning(None,"توجه","تیک گزینه ثبت دنباله زده شده اما خاطره اصلی انتخاب نشده است در نتیجه به عنوان خاطره ی اصلی و نه دنباله ذخیره میشود")
                self.problemrelateto = "اصلی"
        else:
            self.problemrelateto = "اصلی"
        path = self.leadress.text()
        p = Path(path)
        if p.exists:
            self.resfolder = path
        else:
            self.resfolder = '.'

        self.additionaldata = self.getAdditionalData()
        self.duration = self.getCustomTime()
        self.attempts = self.getAttempts(self.problem)
        self.date = self.getDate()
        

        self.updateDatabase()

    def updateDatabase(self):
        current_time = QTime.currentTime()
        time_string = current_time.toString("hh:mm:ss")
        dbhandler = HandleDataBase(self.conn,self.curs)
        dbhandler.addNewExercise(self.problem,self.problemtype,self.problemcategory,self.problemrelateto,self.duration,self.additionaldata,self.problemintensity,None,self.attempts
                                 ,self.date,None,self.resfolder)
        dbhandler.addNewSession(self.problem,self.duration,time_string,None,self.problemintensity,None,None,self.date,None)
        self.problemId = dbhandler.getProblemIdFromProblem(self.problem)
        self.sessionId = dbhandler.getSessionIdFromProblem(self.problem)
        self.startexercise()
    def getProblemType(self):
        problemtype = self.cbtype.currentText()
        tid = self.cbtype.currentIndex()
        return problemtype, tid
    def getProblemCategory(self):
        problemcategory = self.cbcateg.currentText()
        cid= self.cbcateg.currentIndex()
        return problemcategory , cid
    def getProblemIntensity(self):
        problemintensity = self.sbintensity.value()
        if problemintensity >=7 :
            message = '''
برای خاطراتی که شدت آنها بالای 7 است، ممکن است باعث بروز مشکلات جدی و احساسات شدید شود\nلذا حدالامکان سعی کنید با یک روانشناس/مشاور حاذق گفت و گو کنید و تمرین را زیر نظر یک شخص آموزش دیده و ورزیده انجام دهید.
'''
            QMessageBox.warning(None,"توجه",str(message))
        elif problemintensity == 0:
            QMessageBox.information(None,"توجه","در صورتی که بار احساسی خاصی نسبت به این مسئله ندارید بهتر است روی یک مسئله دیگر کار کنید.")
        else:
            pass
        return problemintensity
    def getAdditionalData(self):
        additional = self.teadditionaldescription.toPlainText()
        if additional != "":
            return additional
        else:
            return None
    def getCustomTime(self):
        if self.chkbxmanualduration.isChecked():
            sec= self.sbsec.value()
            minut = self.sbminut.value()
            customtime = f"{minut}:{sec}"
            return customtime
        else:
            return "00:30"
    def getAttempts(self,problem):
        hndldb = HandleDataBase(self.conn,self.curs)
        try:
            attempts = hndldb.fetchattempts(problem)
            return attempts
        except Exception:
            return int(1)
    def getDate(self):
        hndldate = DateTools()
        date =hndldate.justDate()
        return date
    def controllSpinBox(self):
        if self.sbminut.value() >=1 :
            self.sbsec.setMinimum(0)
        else:
            self.sbsec.setMinimum(30)
    def closeEvent(self,event):
        self.backmainpage()