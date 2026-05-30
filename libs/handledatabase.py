import sqlite3
from libs.handledate import DateTools
class HandleDataBase():

    def __init__(self,conn,cursor):
            self.conn = conn
            self.cursor = cursor
            self.db_path = "db\\userdata.db"
        
            
    def createdb(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                            password TEXT PRIMARY KEY,
                            name TEXT,
                            weight TEXT,
                            age TEXT,
                            hint TEXT
                )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                            sessionid INTEGER PRIMARY KEY,
                            totalsession TEXT,
                            mood TEXT,
                            spo2 TEXT,
                            hr TEXT,
                            hrv TEXT,
                            probdone Text,
                            date Text
                )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS probs (
                            problemid INTEGER PRIMARY KEY,
                            problem TEXT,
                            type TEXT,
                            category TEXT,
                            relate TEXT,
                            duration TEXT,
                            additional TEXT,
                            firstintensity TEXT,
                            lastintensity TEXT,
                            attempts TEXT,
                            date TEXT,
                            done TEXT,
                            res TEXT
                )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS session (
                            sessionid INTEGER PRIMARY KEY,
                            problem TEXT,
                            duration TEXT,
                            starttime TEXT,
                            endtime TEXT,
                            startintensity TEXT,
                            endintensity TEXT,
                            comment TEXT,
                            date TEXT,
                            done TEXT
                )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                            catid INTEGER PRIMARY KEY,
                            category TEXT,
                            dateadded TEXT

                )
        ''')
        self.conn.commit()

    def fetchResFolderByProblemId(self,problemid):
        try:
            self.cursor.execute('''SELECT res FROM probs WHERE problemid=?''',(problemid,))
            resfolder = self.cursor.fetchone()[0]
            return resfolder
        except Exception as _e:
            print("fetchResFolderByProblemId: ",_e)
    def fetchUserName(self):
        try:
            self.cursor.execute("SELECT name FROM user")
            name = self.cursor.fetchone()[0]
        except Exception as _p:
            print("this happend(name)",_p)
            return None
        return name
    def fetchattempts(self,problem):
        try:
            self.cursor.execute("SELECT MAX(attempts) FROM probs WHERE problem =?",(problem,))
            max_value = self.cursor.fetchone()[0]
            max_value = max_value +1
            print("found: ",max_value)
        except Exception:
            max_value = 1
        return max_value
    def fetchUserPassword(self):
        try:
            self.cursor.execute("SELECT password FROM user")
            password = self.cursor.fetchone()[0]
        except Exception as _p:
            print("this happend(pass)",_p)
            return None
        return password

    def fetchProblemId(self):
        try:
            self.cursor.execute("SELECT MAX(problemid) FROM probs")
            max_value = self.cursor.fetchone()[0]
            max_value = max_value +1
        except Exception:
            max_value = 1
        return max_value
    def fetchSessionId(self):
        try:
            self.cursor.execute("SELECT MAX(sessionid) FROM session")
            max_value = self.cursor.fetchone()[0]
            max_value = max_value +1
        except Exception:
            max_value = 1
        return max_value
    def addNewExercise(self,problem,problemtype,category,problemrelateto,duration,additional,firstintensity,lastintensity,attempts,date,done,resfolder):
        lastprobid = self.fetchProblemId()
        try:
            self.cursor.execute('''
                INSERT INTO probs (problemid, problem, type, category, relate, duration, additional, firstintensity, lastintensity, attempts, date, done,res)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                ''', (lastprobid, problem, problemtype, category, problemrelateto, duration, additional, firstintensity, lastintensity, attempts, date, done,resfolder))
        except Exception as _o:
            print(_o)
        self.conn.commit()
    def editExistingProblemAttempt(self,attempt,problemid):
        try:
            self.cursor.execute('''UPDATE probs SET attempts = ? WHERE problemid = ?''', (attempt, problemid))
            self.conn.commit()
        except Exception as _e:
            print("editExistingProblemAttempt: ",_e)
    def editExistingProblem(self,problem,probid):
        self.cursor.execute('''UPDATE probs SET problem = ? WHERE problemid = ?''', (problem, probid))
        self.conn.commit()
    def editExistingProblemType(self,type,probid):
        self.cursor.execute('''UPDATE probs SET type = ? WHERE problemid = ?''', (type, probid))
        self.conn.commit()
    def editExistingProblemCategory(self,category,probid):
        self.cursor.execute('''UPDATE probs SET category = ? WHERE problemid = ?''', (category, probid))
        self.conn.commit()
    def editExistingProblemRelate(self,relate,probid):
        self.cursor.execute('''UPDATE probs SET relate = ? WHERE problemid = ?''', (relate, probid))
        self.conn.commit()
    def addLoginData(self,name,password):
        self.cursor.execute('''INSERT INTO user (name,password) VALUES(?,?)''',(name,password))
        self.conn.commit()
    def addNewSession(self,problem,duration,starttime,endtime,startintensity,endintensity,comment,date,done):
        lastsessionbid = self.fetchSessionId()
        self.cursor.execute('''
            INSERT INTO session (sessionid, problem, duration, starttime, endtime, startintensity, endintensity, comment, date, done)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (lastsessionbid,problem,duration,starttime,endtime,startintensity,endintensity,comment,date,done))
    def getAllExcersiseData(self)->tuple:
        self.cursor.execute('''SELECT * FROM probs''')
        excersisedata = self.cursor.fetchall()
        return excersisedata
    def getAllSessionData(self)->tuple:
        self.cursor.execute('''SELECT * FROM session''')
        sessiondata = self.cursor.fetchall()
        return sessiondata
    def getSessionIdFromProblem(self,problem):
        self.cursor.execute('''SELECT sessionid FROM session WHERE problem =?''',(problem,))
        sessionId = self.cursor.fetchone()[0]
        return sessionId
    def getProblemIdFromProblem(self,problem):
        try:
            self.cursor.execute('''SELECT problemid FROM probs WHERE problem =?''',(problem,))
            problemid = self.cursor.fetchone()[0]
            return problemid
        except Exception as _p:
            print(_p)
    def fetchProblemWithProblemId(self,problemid):
        try:
            self.cursor.execute('''SELECT * FROM probs WHERE problemid =?''',(problemid,))
            data = self.cursor.fetchall()
            return data
        except Exception as _e:
            print("fetchProblemWithProblemId:",_e)
    def fetchProblemWithProblem(self,problem):
        try:
            self.cursor.execute('''SELECT * FROM probs WHERE problem =?''',(problem,))
            data = self.cursor.fetchall()
            return data
        except Exception as _e:
            print("fetchProblemWithProblem:",_e)
    def fetchSessionWithProblem(self,problem):
        try:
            self.cursor.execute('''SELECT * FROM session WHERE problem =?''',(problem,))
            data = self.cursor.fetchall()
            return data
        except Exception as _e:
            print("fetchSessionWithProblem:",_e)
    
    def updateSessionEndtimeWithSessionId(self,sessionid,endtime):
        self.cursor.execute('''UPDATE session SET endtime=? WHERE sessionid=?''',(endtime,sessionid))
        self.conn.commit()
    def updateSessionEndintensityWithSessionId(self,sessionid,endintensity):
        self.cursor.execute('''UPDATE session SET endintensity= ? WHERE sessionid=?''',(endintensity,sessionid))
        self.conn.commit()
    def updateSessionDoneWithSessionId(self,sessionid,stat):
        self.cursor.execute('''UPDATE session SET done= ? WHERE sessionid=?''',(stat,sessionid))
        self.conn.commit()
    def updateProblemDoneWithProblemId(self,problemid,stat):
        try:
            self.cursor.execute('''UPDATE probs SET done= ? WHERE problemid=?''',(stat,problemid))
            self.conn.commit()
        except Exception as _e:
            print("updateProblemDoneWithProblemId:", _e)
    def addCommentTOSession(self,sessionid,comment):
        self.cursor.execute('''UPDATE session SET comment= ? WHERE sessionid=?''',(comment,sessionid))
        self.conn.commit()
    def updateProblemLastintensityWithProblemId(self,problemid,lastintensity):
        self.cursor.execute('''UPDATE probs SET lastintensity= ? WHERE problemid=?''',(lastintensity,problemid))
        self.conn.commit()
    def removeExcersiseByProblemId(self,problemid):
        self.cursor.execute('''DELETE FROM probs WHERE problemid= ?''',(problemid,))
        self.conn.commit()
    def removeSessionBySessionId(self,sessionid):
        self.cursor.execute('''DELETE FROM session WHERE sessionid= ?''',(sessionid,))
        self.conn.commit()
    def fetchCategoryStatics(self):
        self.cursor.execute('''SELECT category FROM probs''')
        types = self.cursor.fetchall()
        category_count = {}
        for row in types:
            category = row[0]
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1
        return category_count
    def fetchTotalExcersiseTime(self):
        self.cursor.execute('''SELECT duration FROM session''')
        ttlduration = self.cursor.fetchall()
        temp_time = 0
        for time in ttlduration:
            temp = time[0].split(":")
            minutes = int(temp[0])
            secound = int(temp[1])
            ttltimesec = (minutes * 60 ) + secound
            temp_time += ttltimesec
        return temp_time
    def fetchTotalExcersiseToday(self):
        dateobj = DateTools()
        date = dateobj.justDate()
        self.cursor.execute('''SELECT duration FROM session WHERE date = ?''',(date,))
        todayexercise = self.cursor.fetchall()
        temp_time = 0
        for time in todayexercise:
            temp = time[0].split(":")
            minutes = int(temp[0])
            secound = int(temp[1])
            ttltimesec = (minutes * 60 ) + secound
            temp_time += ttltimesec
        return temp_time
    def returnTotalExcersiseInMinutes(self):
        totalexcersiseinsec = self.fetchTotalExcersiseTime()
        minutes = str(totalexcersiseinsec/60).split(".")
        if len(minutes) >1:
            secound = int(totalexcersiseinsec)% 60
            if secound <10 :
                secound =f"0{secound}"
            formated =f"{minutes[0]}:{secound}"
        else:
            formated = f"00:{minutes[0]}"
        return formated
    def returnTodayExcersiseInMinutes(self):
        totalexcersiseinsec = self.fetchTotalExcersiseToday()
        minutes = str(totalexcersiseinsec/60).split(".")
        if len(minutes) >1:
            secound = int(totalexcersiseinsec)% 60
            if secound <= 9:
                secound = f"0{secound}"
            formated =f"{minutes[0]}:{secound}"
        else:
            formated = f"00:{minutes[0]}"
        return formated
    def fetchTotalSession(self):
        self.cursor.execute('''SELECT sessionid FROM session''')
        tempcount = self.cursor.fetchall()
        return len(tempcount)
    def fetchTotalMemmories(self):
        self.cursor.execute('''SELECT problemid FROM probs''')
        tempcount = self.cursor.fetchall()
        return len(tempcount)
    def fetchNeutrelizedMemories(self):
        self.cursor.execute('''SELECT problemid FROM probs where done=?''',("بله",))
        tempcount = self.cursor.fetchall()
        return len(tempcount)
    def fetchMood(self):
        self.cursor.execute('''SELECT mood FROM stats''')
        allmoods = self.cursor.fetchall()
        averagemood = 0.0
        for moods in allmoods:
            averagemood += float(moods)
        return averagemood
    def fetchOnlyProblems(self):
        self.cursor.execute('''SELECT problem from probs''')
        problems = self.cursor.fetchall()
        return problems
    def lastSessionIdFromProblem(self,problem):
        try:
            self.cursor.execute("SELECT MAX(sessionid) FROM session WHERE problem= ?",(problem,))
            sessionid = self.cursor.fetchone()[0]
            return sessionid
        except Exception as _e:
            print("lastSessionIdFromProblem:",_e)
    def fetchDateAndDuration(self):
        self.cursor.execute("SELECT date,duration FROM session")
        data = self.cursor.fetchall()
        dttol = DateTools()
        dateanddure = {}
        for dat in data:
            date = dat[0]
            time = dttol.calcTime(dat[1])
            if date in dateanddure:
                dateanddure[date] += time
            else:
                dateanddure[date] = time
        return dateanddure
    def fetchDurationBySessionId(self,sessionid):
        self.cursor.execute('select duration from session where sessionid=?',(sessionid,))
        duration = self.cursor.fetchone()[0]
        return duration
    def updateResFolderWithProblemId(self,res,problemid):
        self.cursor.execute('UPDATE probs SET res=? WHERE problemid=?',(res,problemid))
        self.conn.commit()
    def fetchResFolderWithProblemId(self,problemid):
        self.cursor.execute('SELECT res FROM probs WHERE problemid=?',(problemid,))
        resfolder = self.cursor.fetchone()[0]
        print(resfolder)
        return resfolder
    def getSessionDataInDict(self,sessionid)->dict:
        self.cursor.execute('SELECT * from session WHERE sessionid=?',(sessionid,))
        data = self.cursor.fetchall()
        dataindict = {}
        for dat in data:
            sessionid = dat[0]
            problem  = dat[1]
            duration = dat[2]
            starttime = dat[3]
            endtime = dat[4]
            startintensity = dat[5]
            endintensity =dat[6]
            comment = dat[7]
            date = dat[8]
            done = dat[9]
        dataindict['sessionid'] = sessionid
        dataindict['problem'] = problem
        dataindict['duration']= duration
        dataindict['starttime'] = starttime
        dataindict['endtime'] = endtime
        dataindict['startintensity'] = startintensity
        dataindict['endintensity'] = endintensity
        dataindict['comment'] = comment
        dataindict['date'] = date
        dataindict['done'] = done
        return dataindict
        
    def getProblemDataInDict(self,problemid)->dict:
        self.cursor.execute('SELECT * from probs WHERE problemid=?',(problemid,))
        data = self.cursor.fetchall()
        dataindict = {}
        for dat in data:
            problemid =dat[0]
            problem =dat[1]
            type =dat[2]
            category =dat[3]
            relate =dat[4]
            duration =dat[5]
            additional =dat[6]
            firstintensity =dat[7]
            lastintensity =dat[8]
            attempts =dat[9]
            date =dat[10]
            done =dat[11]
            res=dat[12]
        dataindict['problemid'] = problemid
        dataindict['problem']= problem
        dataindict['type'] = type
        dataindict['category'] = category
        dataindict['relate'] = relate
        dataindict['duration'] = duration
        dataindict['additional'] = additional
        dataindict['firstintensity'] = firstintensity
        dataindict['lastintensity'] = lastintensity
        dataindict['attempts'] = attempts
        dataindict['date'] = date
        dataindict['done'] = done
        dataindict['res'] = res
        return dataindict