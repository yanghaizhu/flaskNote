import datetime
from dateutil.relativedelta import relativedelta
from .LunarSolar import LunarSolar

class DateInfo():
    def __init__(s,now):
        s.year = now.year
        s.month = now.month
        s.day = now.day
        s.hour = now.hour
        s.minute = now.minute
        s.second = now.second
        #weekday = 0--6 sunday monday ... saturday
        s.weekday = (now.weekday()+1) % 7
        s.firstdayWeek = (now.weekday() - now.day + 2) % 7
#        s.lastDay = (datetime.date(now.year, now.month+1, 1) - relativedelta(days = 1)).day
        #print(s.firstdayWeek)
        #week num of the year : 1:53....
        s.weeknumYear = now.isocalendar()[1]
        if s.month == 12 and s.weeknumYear == 1:
            s.weeknumYear = datetime.date(now.year, now.month, now.day-7).isocalendar()[1] + 1
        #week num in the month: 1:6  first second ....
        s.weeknumMon = 1 + s.weeknumYear - datetime.date(now.year, now.month, 1).isocalendar()[1]
        s.weekDayNum = 1 + s.day // 7
        s.lastWeekNum = 1 if (datetime.date(now.year, now.month, 1) + relativedelta(months=1) - relativedelta(days = 1)).isocalendar()[1] == now.isocalendar()[1] else 0
        s.lastweekDay = 1 if (datetime.date(now.year, now.month, 1) + relativedelta(months=1) - relativedelta(days = 1)).day - s.day < 7 else 0
        s.leapYear = 1 if s.year % 400 == 0 or (s.year % 100 != 0 and s.year % 4 == 0) else 0
        s.luYear,s.luMonth,s.luDay,s.luIsleap = LunarSolar._fromOffset(s.year, s.month, s.day)
        
    def cout(s):
        print("year",s.year)
        print("month",s.month)
        print("day",s.day)
        print("weeknumYear",s.weeknumYear)
        print("weekday",s.weekday)
        print("weeknumMon",s.weeknumMon)
        print("weekDayNum",s.weekDayNum)
        print("lastWeekNum",s.lastWeekNum)
        print("lastweekDay",s.lastweekDay)
        print("LuYear",s.luYear)
        print("LuMonth",s.luMonth)
        print("LuDay",s.luDay)
        print("LuIsLeap",s.luIsleap)


    

if __name__ == '__main__':
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day)
    DateInfo(now).cout()
