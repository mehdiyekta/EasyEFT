from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QLabel,QVBoxLayout,QTableWidgetItem,QMessageBox,QLineEdit,QPushButton
from PyQt5.QtCore import QTimer,QThread
from PyQt5 import uic
from forms import newexerciz
from forms import exercisemanager
from forms import moodpage
import sys
from PyQt5.QtCore import QCoreApplication
import sqlite3
from libs.doughnut_widget import DoughnutWidget
from libs.handledatabase import HandleDataBase
from libs.handlepass import HandlePassword
from libs.handlefiles import HandleFiles
from libs.handledate import DateTools
from libs.handlecahrt import HandleChart
import socket
PORT_TO_USE = 9999
class SingleInstance:
    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def acquire(self):
        try:
            self.socket.bind(('127.0.0.1', self.port))
            return True
        except socket.error:
            return False

    def cleanup(self):
        if self.socket:
            self.socket.close()
            self.socket = None
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("ui/mainwindow.ui",self)
        self.frame.setVisible(False)
        self.frame_2.setVisible(False)
        self.frame_12.setVisible(False)
        self.lblhint.setVisible(False)
        self.lbldesc1.setVisible(False)
        self.lbldesc2.setVisible(False)
        self.stackedWidget.setCurrentIndex(0)
        self.pswrdentry.setEchoMode(QLineEdit.Password)
        self.pswrdentry.textChanged.connect(self.check_password_strength)
        self.hsbtn.clicked.connect(self.Togglehidenshow)
        self.btnexit.clicked.connect(self.closeapp)
        self.btnexit_2.clicked.connect(self.closeapp)
        self.btnlgin.clicked.connect(self.Login)
        self.btnlgin.setDefault(True)
        self.btnlgin.setAutoDefault(True)
        self.btnlgin.setFocus()
        self.btnnewex.clicked.connect(self.newexcersice)
        self.btnhome.clicked.connect(self.home)
        self.btnnewex_2.clicked.connect(self.newexcersice)
        self.btnhome_2.clicked.connect(self.home)
        self.btnexhis.clicked.connect(self.exhistory)
        self.btnexhis_2.clicked.connect(self.exhistory)
        self.btnexmngmnt.clicked.connect(self.exmngmnt)
        self.btnexmngmnt_2.clicked.connect(self.exmngmnt)
        self.btnnewmemmory.clicked.connect(self.newexerc)
        self.lwexcersisedata.itemClicked.connect(self.openExercisePage)
        self.btnnavnewex.clicked.connect(self.btnnewex.click)
        self.btndelex.clicked.connect(self.deleteex)
        self.btneditex.clicked.connect(self.modifydb)
        self.btndelsession.clicked.connect(self.delsession)
        self.btnlock.clicked.connect(self.lockpage)
        self.btnnewemotion.clicked.connect(self.openMoodPage)
        #Variables:
        self.attempt = 0
        self.db_path = "db\\userdata.db"
        self.conn = ""
        self.curs = ""
        self.modified_rows = set() 
        #init minit
        self.initmainui()
    def openMoodPage(self):
        self.moodpage = moodpage.MoodPage(self,self.conn,self.curs)
        self.moodpage.show()
        self.hide()
    def trackchange(self,item):
        self.modified_rows.add(item.row())
    def todayDate(self):
        dt = DateTools()
        today = dt.justDate()
        name = dt.get_jalali_day_name(today)
        fulldate = f"{name}-{today}"
        self.lbldate.setText(fulldate)
    def newexerc(self):
        self.newexrcize = newexerciz.NewExcerize(self,self.conn,self.curs)
        self.newexrcize.show()
        self.hide()
    def createConnection(self,path):
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()
    def openExercisePage(self,item):
        item = item.text()
        self.exercisemanager = exercisemanager.ExcesiseManager(self,self.conn,self.curs,item)
        self.exercisemanager.show()
        self.hide()
        
    def createdb(self):
        hndldb = HandleDataBase(conn=self.conn,cursor=self.curs)
        hndldb.createdb()
    def newexcersice(self):
        self.stackedWidget.setCurrentIndex(2)
        hndlr = HandleDataBase(self.conn,self.curs)
        excersisedatas = hndlr.getAllExcersiseData()
        try:
            self.lwexcersisedata.clear()
            for datas in excersisedatas:
                self.lwexcersisedata.addItem(str(datas[1]))
        except IndexError:
            self.lwexcersisedata.clear()
            self.lwexcersisedata.addItem("تمرینی یافت نشد !")
        except Exception as _p:
            print(_p)
    def home(self):
        self.uiStaticValidator()
        self.stackedWidget.setCurrentIndex(1)
    
    def deleteitems(self,layout):
        '''
        delete items from a layout to prevent duplication
        stuff when a chart or something is displayed
        morethan once.
        '''
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
    def exhistory(self):
        self.deleteitems(self.verticalLayout_16)
        self.twexhist.setRowCount(0)
        hndldt = HandleDataBase(self.conn,self.curs)
        exdata = hndldt.getAllExcersiseData()
        self.twexhist.setRowCount(len(exdata))
        for row, row_data in enumerate(exdata):
            for column, item in enumerate(row_data):
                self.twexhist.setItem(row, column, QTableWidgetItem(str(item)))
        self.stackedWidget.setCurrentIndex(3)
        #PlaceHolder
        dw = DoughnutWidget(font_path=r".\\fonts\B Zar.ttf", show_legend=False)
        self.verticalLayout_16.addWidget(dw)
        stuff =hndldt.fetchCategoryStatics()
        sizes=[]
        labels =[]
        colors =[]
        for category, count in stuff.items():
            sizes.append(count)
            labels.append(category)
            c = dw.generate_random_color()
            colors.append(c)
        
        dw.set_data(sizes, labels, colors, hole_size=0.5)
        dnd = hndldt.fetchDateAndDuration()
        dates = []
        dures = []
        for date,duration in dnd.items():
            dates.append(date)
            dures.append(duration/60)

        chrt = HandleChart(dures,dates)
        ye = chrt.create()
        self.verticalLayout_16.addWidget(ye)
        

    def exmngmnt(self):
        self.stackedWidget.setCurrentIndex(4)
        hndl = HandleDataBase(self.conn,self.curs)
        exdata = hndl.getAllExcersiseData()
        self.twedit.setRowCount(0)
        self.twedit.setRowCount(len(exdata))
        row = 0
        for data in exdata:
            problemid = data[0]
            problemname = data[1]
            problemtype = data[2]
            problemcategory = data[3]
            problemrelateto = data[4]

            self.twedit.setItem(row, 0, QTableWidgetItem(str(problemid)))
            self.twedit.setItem(row, 1, QTableWidgetItem(str(problemname)))
            self.twedit.setItem(row, 2, QTableWidgetItem(str(problemtype)))
            self.twedit.setItem(row, 3, QTableWidgetItem(str(problemcategory)))
            self.twedit.setItem(row, 4, QTableWidgetItem(str(problemrelateto)))
            row += 1
        self.twedit.itemChanged.connect(self.trackchange)
        self.twsession.setRowCount(0)
        exdata = hndl.getAllSessionData()
        self.twsession.setRowCount(len(exdata))
        for row, row_data in enumerate(exdata):
            for column, item in enumerate(row_data):
                self.twsession.setItem(row, column, QTableWidgetItem(str(item)))
    def modifydb(self):
        hndl = HandleDataBase(self.conn,self.curs)
        if len(self.modified_rows) !=0 :
            pass
        else:
            QMessageBox.critical(None,"خطا","لطفا در جدول سمت راست تغییرات مورد نظر را اعمال کنید و سپس کلید ثبت ویرایش را بزنید، در حال حاضر تغییری در جدول اعمال نشده است.")
            return
        for item in self.modified_rows:
            problemid = self.twedit.item(item,0).text()
            problemname = self.twedit.item(item,1).text()
            problemtype =self.twedit.item(item,2).text()
            problemcategory = self.twedit.item(item,3).text()
            problemrelateto = self.twedit.item(item,4).text()
            hndl.editExistingProblem(problemname,problemid)
            hndl.editExistingProblemType(problemtype,problemid)
            hndl.editExistingProblemCategory(problemcategory,problemid)
            hndl.editExistingProblemRelate(problemrelateto,problemid)
        QMessageBox.information(None,"موفق","تغییرات با موفقیت ذخیره شدند!")


    def deleteex(self):
        problemrow = self.twedit.currentRow()
        if self.twedit.item(problemrow,0):
            problemid = self.twedit.item(problemrow,0).text()
        else:
            return
        problemname = self.twedit.item(problemrow,1).text()
        cnfrmdelete = QMessageBox()
        cnfrmdelete.setWindowTitle("تایید حذف")
        cnfrmdelete.setText(f"آیا مطمئن هستید تمرین شماره {problemid} با موضوع \'{problemname}\' را حذف کنید؟")
        cnfrmdelete.setIcon(4)
        buttonyes = QPushButton ("بله")
        buttonno = QPushButton ("خیر")
        cnfrmdelete.addButton(buttonyes,QMessageBox.ButtonRole.AcceptRole)
        cnfrmdelete.addButton(buttonno,QMessageBox.ButtonRole.RejectRole)
        cnfrmdelete.exec()
        if cnfrmdelete.clickedButton()==buttonyes:
            hndl = HandleDataBase(self.conn,self.curs)
            hndl.removeExcersiseByProblemId(problemid)
            self.exmngmnt()
        else:
            pass
    def delsession(self):
        
        sessionrow = self.twsession.currentRow()
        if self.twsession.item(sessionrow,0):
            sessionid = self.twsession.item(sessionrow,0).text()
        else:
            return
        sessionname = self.twsession.item(sessionrow,1).text()
        cnfrmdelete = QMessageBox()
        cnfrmdelete.setWindowTitle("تایید حذف")
        cnfrmdelete.setText(f"آیا مطمئن هستید تمرین شماره {sessionid} با موضوع \'{sessionname}\' را حذف کنید؟")
        cnfrmdelete.setIcon(4)
        buttonyes = QPushButton ("بله")
        buttonno = QPushButton ("خیر")
        cnfrmdelete.addButton(buttonyes,QMessageBox.ButtonRole.AcceptRole)
        cnfrmdelete.addButton(buttonno,QMessageBox.ButtonRole.RejectRole)
        cnfrmdelete.exec()
        if cnfrmdelete.clickedButton()==buttonyes:
            hndl = HandleDataBase(self.conn,self.curs)
            hndl.removeSessionBySessionId(sessionid)
            self.exmngmnt()
        else:
            pass
    def Togglehidenshow(self):
        if self.hsbtn.isChecked():
            self.pswrdentry.setEchoMode(QLineEdit.Normal)
            self.hsbtn.setText("مخفی")
        else:
            self.pswrdentry.setEchoMode(QLineEdit.Password)
            self.hsbtn.setText("مشاهده")
    def initmainui(self):
        pose_x = 500
        pose_y = 100
        width = 1000
        height = 780
        self.setGeometry(pose_x+200, pose_y, round(width/2), height)
        db_valid = False
        try:
            self.createConnection(self.db_path)
            self.createdb()
            filecheck = HandleFiles(self.db_path)
            db_valid = filecheck.checkDatabaseExist()
            if db_valid:   
                usename = HandleDataBase(self.conn,self.curs)
                usename = usename.fetchUserName()
                if usename:
                    self.nameentry.setText(str(usename))
                    self.nameentry.setEnabled(False)
                else:
                    self.btnlgin.setText("ساخت حساب")
            else:
                raise Exception

        except Exception as _p:
            
            print(_p)
        
    #Cool Password Strength Border Effect :D
    def update_stylesheet(self, attempts):
        if attempts == 0:
            border_color = "green"
        elif attempts == 1:
            border_color = "yellow"
        elif attempts == 2:
            border_color = "orange"
        else:
            border_color = "red"

        stylesheet = f"QLineEdit {{ border: 2px solid {border_color}; }} "
        self.pswrdentry.setStyleSheet(stylesheet)

    def check_password_strength(self):
        password = self.pswrdentry.text()
        strength = self.evaluate_password_strength(password)
        strengths = {
            '1': {'color': 'red', 'labels': [1], 'text': 'پسورد ضعیف است'},
            '2': {'color': 'orange', 'labels': [1, 2], 'text': 'پسورد ضعیف است'},
            '3': {'color': 'yellow', 'labels': [1, 2, 3], 'text': 'پسورد متوسط است'},
            '4': {'color': '#aaff00', 'labels': [1, 2, 3, 4], 'text': 'پسورد بد نیست'},
            '5': {'color': '#00b600', 'labels': [1, 2, 3, 4, 5], 'text': 'پسورد عالیه'}
        }
        config = strengths[strength]
        for i in range(1, 6):
            if i in config['labels']:
                getattr(self, f'pwsl{i}').setStyleSheet(f"QLabel{{background-color: {config['color']}}}")
            else:
                getattr(self, f'pwsl{i}').setStyleSheet("QLabel{background-color: gray}")
        self.psrdstrng.setText(config['text'])
        self.psrdstrng.setStyleSheet(f"QLabel{{color: {config['color']}}}")

    def evaluate_password_strength(self, password):
        hndlpss = HandlePassword()
        result = hndlpss.passwordstrength(password)
        return result
    def uiStaticValidator(self):
        dbhndobj = HandleDataBase(self.conn,self.curs)
        totalexcersize =dbhndobj.returnTotalExcersiseInMinutes()
        self.lblttlexercise.setText(totalexcersize)
        todaystotal = dbhndobj.returnTodayExcersiseInMinutes()
        self.lbltoday.setText(todaystotal)
        totalsession = dbhndobj.fetchTotalSession()
        self.lblttlsessions.setText(str(totalsession))
        totalmemories = dbhndobj.fetchTotalMemmories()
        self.lblsavedmemories.setText(str(totalmemories))
        neutmem = dbhndobj.fetchNeutrelizedMemories()
        self.lblneutrializedmem.setText(str(neutmem))
        avermood = dbhndobj.fetchMood()
        self.lblmood.setText(str(avermood))
    def lockpage (self):
        self.frame.setVisible(False)
        self.frame_2.setVisible(False)
        self.frame_12.setVisible(False)
        self.frame_13.setVisible(True)
        self.frame_11.setVisible(True)
        self.lblhint.setVisible(False)
        self.lbldesc1.setVisible(False)
        self.lbldesc2.setVisible(False)
        self.stackedWidget.setCurrentIndex(0)
        self.pswrdentry.setText("")
        self.initmainui()

    def Login(self):
        try:
            dbhndobj = HandleDataBase(self.conn,self.curs)
        except Exception:
            pass
        password = self.pswrdentry.text()
        hint ="ناموجود"
        nam = dbhndobj.fetchUserName()
        pas = dbhndobj.fetchUserPassword()
        if nam == None:
            lgin = self.nameentry.text()
            pswrd = self.pswrdentry.text()
            dbhndobj.addLoginData(str(lgin),str(pswrd))
            QMessageBox.information(None,"موفق!","حساب با موفقیت ایجاد شد لطفا دوباره اطلاعات را وارد کرده و وارد صفحه خود شوید.")
            self.nameentry.setText(lgin)
            self.nameentry.setEnabled(False)
            self.pswrdentry.setText("")
            self.btnlgin.setText("ورود")
            return
        else:
            pass
        if password ==pas:
            self.frame_13.setVisible(False)
            self.frame_2.setVisible(True)
            self.stackedWidget.setCurrentIndex(1)
            self.lblusername.setText(str(self.nameentry.text()))
            self.todayDate()
            self.uiStaticValidator()
            

        else:
            if self.attempt == 3:
                QMessageBox.critical(None,"خطا",f"شما4 بار رمز را اشتباه وارد کردید، برنامه به دلایل امنیتی قفل خواهد شد.")
                self.frame_13.setVisible(False)
                self.frame_12.setVisible(True)
                return
            else:
                pass
            self.attempt += 1
            QMessageBox.critical(None,"خطا",f"پسورد وارد شده نادرست است. تعداد دفعات وارد کردن رمز : {self.attempt}")
            self.lblhint.setText(f"*راهنما: {hint}")
            self.lblhint.setVisible(True)
            self.lbldesc1.setVisible(True)
            self.lbldesc2.setVisible(True)
            self.update_stylesheet(self.attempt)
    def closeapp(self):
        cnfrmexit = QMessageBox()
        cnfrmexit.setWindowTitle("تایید خروج")
        cnfrmexit.setText("آیا از خروج مطمئن هستید؟")
        cnfrmexit.setIcon(4)
        buttonyes = QPushButton ("بله")
        buttonno = QPushButton ("خیر")
        cnfrmexit.addButton(buttonyes,QMessageBox.ButtonRole.AcceptRole)
        cnfrmexit.addButton(buttonno,QMessageBox.ButtonRole.RejectRole)
        cnfrmexit.exec()
        if cnfrmexit.clickedButton()==buttonyes:
            self.close()
        else:
            pass

    def closeEvent(self,event):
        try:
            self.conn.close()
            single_instance.cleanup()
            print("Done.")
        except Exception as _p:
            print("No Connection/or failed:",_p)

if __name__ =='__main__':
    app = QApplication(sys.argv)
    single_instance = SingleInstance(PORT_TO_USE)
    if not single_instance.acquire():
        QMessageBox.critical(None, "توجه", "این برنامه بر پایگاه داده متکی است و جهت جلوگیری از تداخل و از بین رفتن داده ها بهتر است صرفا از یک جلسه استفاده شود\nلطفا جلسه ی قبل را کامل ببندید و سپس اقدام به بازکردن جلسه جدید نمایید.")
        sys.exit(1)
    QCoreApplication.instance().aboutToQuit.connect(single_instance.cleanup)

    window = MainWindow()
    window.show()
    r = app.exec_()
    single_instance.cleanup()
    sys.exit(r)


    # sys.exit(app.exec_())