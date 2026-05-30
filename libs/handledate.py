from jdatetime import datetime
import jdatetime
class DateTools():
    def is_valid_jalali_date(self,date_string):
        try:
            year, month, day = map(int, date_string.split('/'))
            jdatetime.date(year, month, day)
            return True
        except (ValueError, IndexError):
            return False
    def get_jalali_day_name(self,jalali_date_string):
        year, month, day = map(int, jalali_date_string.split('/'))
        jalali_date = jdatetime.date(year, month, day)
        day_of_week = jalali_date.weekday()
        day_names = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
        return day_names[day_of_week]
    def tarikhemrooz(self)->str:
        persian_date = datetime.now()
        persian_day_name = persian_date.strftime("%A")

        persian_day_name = persian_day_name.replace("Saturday", "شنبه") \
            .replace("Sunday", "یکشنبه") \
            .replace("Monday", "دوشنبه") \
            .replace("Tuesday", "سه‌شنبه") \
            .replace("Wednesday", "چهارشنبه") \
            .replace("Thursday", "پنجشنبه") \
            .replace("Friday", "جمعه")
        
        
        day = persian_date.strftime("%d") 
        month = persian_date.strftime("%m")  
        year = persian_date.strftime("%Y") 

        fulldate = {"day":day,"month":month,"year":year,"dayname":persian_day_name}
        return fulldate
    def justDate(self):
        fulldate = self.tarikhemrooz()
        day = fulldate['day']
        month = fulldate['month']
        year = fulldate['year']
        formatted = f"{year}/{month}/{day}"
        return formatted
    def calcTime(self,timeexercise):
        temp_time = 0
        temp = timeexercise.split(":")
        minutes = int(temp[0])
        secound = int(temp[1])
        ttltimesec = (minutes * 60 ) + secound
        temp_time += ttltimesec
        return temp_time

