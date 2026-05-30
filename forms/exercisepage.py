from PyQt5.QtWidgets import QMainWindow,QMessageBox,QLabel,QFileDialog
from PyQt5.QtCore import QTimer,QThread,QTime , QUrl , Qt
from PyQt5.QtGui import QImage , QPicture, QPixmap,QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import uic
from forms import afterexercise
from forms import aftereffect
from libs.handledatabase import HandleDataBase
import os,sys
from pathlib import Path
class PageExcerize(QMainWindow):
    def __init__(self,main_window,window,conn,curs,sessionid,problemid,duration,resfolder):
        super(PageExcerize,self).__init__()
        uic.loadUi("./ui/exercisepage.ui",self)
        #main window = window that we came from
        #base window = fist window
        self.main_window = main_window
        self.basewindow = window
        self.conn = conn
        self.curs = curs
        self.sessionid = sessionid
        self.problemid = problemid
        self.btnstop.clicked.connect(self.back)
        self.btnaddnew.clicked.connect(self.addnewafter)
        self.duration = duration
        self.folder = resfolder
        try:
            p = Path(self.folder)
            if p.is_dir and p.exists:
                print("Tre")
                pass
            else:
                self.folder ='.'
        except Exception as _e:
            self.folder = "."
            print(_e)
        self.clock =0
        self.minutes = 0
        self.seconds = 0
        self.is_running = False
        self.elapsed_time = 0
        self.video_widget = QVideoWidget(self)
        self.hl.addWidget(self.video_widget)
        self.calcduration()
        hndl = HandleDataBase(self.conn,self.curs)
        problemname = hndl.fetchProblemWithProblemId(self.problemid)[0][1]
        self.setWindowTitle(f"{problemname}")
        self.x = self.clock
        self.labeltimer = QTimer(self)
        self.labeltimer.timeout.connect(self.updatelabel)
        self.labeltimer.start(1000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.exercisetime)
        self.timer.setSingleShot(True)
        # self.timer.start(self.clock)
        self.gif_list = [
            QMovie("./assets/gifs/01.gif"),
            QMovie("./assets/gifs/02b.gif"),
            QMovie("./assets/gifs/03b.gif"),
            QMovie("./assets/gifs/04.gif"),
            QMovie("./assets/gifs/05.gif"),
            QMovie("./assets/gifs/06.gif"),
            QMovie("./assets/gifs/07.gif"),
            QMovie("./assets/gifs/08.gif")
        ]
        self.lblguid.setMovie(self.gif_list[0])
        self.gif_list[0].start()
        self.gifguid= QTimer(self)
        self.gifguid.timeout.connect(self.guid)
        self.gifguid.start(3750)
        self.current_gif_index = 0
        self.timer_2 = QTimer(self)
        self.timer_2.timeout.connect(self.show_next_media)
        self.timer_2.start(5000)
        if self.folder =="":
            self.folder = "."
        try:
            self.media_files = sorted(os.listdir(self.folder))
            self.media_files = [os.path.join(self.folder, f) for f in self.media_files]
        except Exception:
            QMessageBox.critical(None,"خطا","ظاهرا فایل های درون پوشه یا خود پوشه دچار تغییر شده اند لطفا از بخش تمرین و مدیریت تمرین آدرس پوشه جدید را به نرم افزار بدهید.")
            self.media_files = sorted(os.listdir("."))
            self.media_files = [os.path.join(".", f) for f in self.media_files]
            
        self.current_index = 0
        self.vmedia_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.vmedia_player.setVideoOutput(self.video_widget)


        self.media_player = QMediaPlayer(self)
        self.is_video = False

        self.show_next_media()  
    def addnewafter(self):
        hndl = HandleDataBase(self.conn,self.curs)
        data = hndl.getSessionDataInDict(sessionid=self.sessionid)
        data2 = hndl.getProblemDataInDict(self.problemid)
        self.addnewafterwin = aftereffect.AfterEffects(self,self.main_window,self.conn,self.curs,data,data2)
        self.addnewafterwin.show()
        self.gifguid.stop()
        self.timer_2.stop()
        self.labeltimer.stop()
        self.elapsed_time=self.timer.remainingTime()
    def resume(self):
        self.gifguid.start(3750)
        self.timer_2.start(5000)
        self.labeltimer.start(1000)
    def play_video(self, file_path):
        self.lblimage.clear()
        self.lblimage.setVisible(False)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.media_player.play()
        
        # Connect the finished signal to show the next media
        self.media_player.stateChanged.connect(self.video_finished)
    def showDialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folder = folder
    def video_finished(self, state):
        if state == QMediaPlayer.StoppedState:
            self.show_next_media()

    def show_next_media(self):
        try:
            if self.current_index >= len(self.media_files):
                self.current_index = 0  

            file_path = self.media_files[self.current_index]

        
            if file_path.endswith(('mp4', 'avi', 'mov')):
                pass
                # self.is_video = True
                # self.play_video(file_path)
            else:
                self.is_video = False
                self.show_image(file_path)

            self.current_index += 1
        except Exception as _e:
            print("show_Next_Media: ",_e)

    def show_image(self, file_path):
        try:
            self.media_player.stop()  
            self.lblimage.clear()
            self.lblimage.setVisible(True)

            # self.movie = QMovie(file_path)
            # self.lblimage.setMovie(self.movie)
            # self.movie.start()
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.lblimage.size(), aspectRatioMode=1)
            self.lblimage.setPixmap(scaled_pixmap)
        except Exception as _e:
            print("Show_Image",_e)
    def on_video_duration_changed(self, duration):
        self.timer.stop()
        self.timer.start(duration)  
        self.timer.timeout.connect(self.show_next_media) 


    def guid(self):
        self.gif_list[self.current_gif_index].stop()
        self.current_gif_index = (self.current_gif_index + 1) % len(self.gif_list)
        self.lblguid.setMovie(self.gif_list[self.current_gif_index])
        self.gif_list[self.current_gif_index].start()
        if self.current_gif_index ==8 :
            self.current_gif_index = 0

    def back(self):
        current_time = QTime.currentTime()
        time_string = current_time.toString("hh:mm:ss")
        self.postex = afterexercise.PostExercise(self,self.basewindow,self.conn,self.curs,self.sessionid,self.problemid,time_string,self.folder)
        self.postex.show()
        try:
            self.timer.disconnect()
            self.timer_2.disconnect()
            self.gifguid.disconnect()
        except Exception as _e:
            print(_e)
        self.hide()
        self.x = 0

    def exercisetime(self):
        self.back()

    def updatelabel(self):
        if self.secounds == 0 and  self.minutes >=1:
            self.minutes -=1
            self.secounds +=59
        else:
            self.secounds -= 1
        state = f"{self.minutes}:{self.secounds}"
        self.lbltime.setText(str(state))
        if self.minutes ==0 and self.secounds == 0:
            self.back()

    def calcduration(self):
        duration = self.duration
        splited = duration.split(":")
        self.minutes = int(splited[0])
        self.secounds = int(splited[1])
        min2sec = int(self.minutes * 60) + int(self.secounds)
        self.clock = int(min2sec)*1000

    def closeEvent(self,event):
        self.back()