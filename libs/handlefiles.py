import os
class HandleFiles():
    def __init__(self,filepath):
        self.filepath = filepath
    def checkDatabaseExist(self):
        file = os.listdir("db\\")
        if file[0]=="userdata.db":
            return True
        else:
            return False