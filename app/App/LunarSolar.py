import datetime
from dateutil.relativedelta import relativedelta

import datetime
from .Info import Info

class LunarSolar():
    _startDate = datetime.date(1900, 1, 31)# don't modify it|| 1900 1 31

    def __init__(s):
        now = datetime.datetime.now()
        
    @staticmethod
    def _enumMonth(yearInfo):
        months = [(i, 0) for i in range(1, 13)]
        leapMonth = yearInfo % 16
        if leapMonth == 0:
            pass
        elif leapMonth <= 12:
            months.insert(leapMonth, (leapMonth, 1))
        else:
            raise ValueError("yearInfo %r mod 16 should in [0, 12]" % yearInfo)

        for month, isLeapMonth in months:
            if isLeapMonth:
                days = (yearInfo >> 16) % 2 + 29
            else:
                days = (yearInfo >> (16 - month)) % 2 + 29
            yield month, days, isLeapMonth

    @classmethod
    def _fromOffset(cls,year, month, day ):
        def _calcMonthDay(yearInfo, offset):
            for month, days, isLeapMonth in cls._enumMonth(yearInfo):
                if offset < days:
                    break
                offset -= days
            return (month, offset + 1, isLeapMonth)
        
        offset = (datetime.date(year, month, day) - cls._startDate).days

        offset = int(offset)

        for idx, yearDay in enumerate(Info.yearDays()):
            if offset < yearDay:
                break
            offset -= yearDay
        year = 1900 + idx

        yearInfo = Info.yearInfos[idx]
        month, day, isLeapMonth = _calcMonthDay(yearInfo, offset)
        return (year, month, day, isLeapMonth)
        

        
    @classmethod

    def Lunar2Solar(cls,LuYear,LuMonth,LuDay,LuLeapMonth):
        def _calcDays(yearInfo, month, day, isLeapMonth):
            isLeapMonth = int(isLeapMonth)
            res = 0
            ok = False
            for _month, _days, _isLeapMonth in cls._enumMonth(yearInfo):
                if (_month, _isLeapMonth) == (month, isLeapMonth):
                    if 1 <= day <= _days:
                        res += day - 1
                        return res
                    else:
                        raise ValueError("day out of range")
                res += _days

            raise ValueError("month out of range")
        yearDays = Info.yearDays()
        offset = 0
        if LuYear < 1900 or LuYear >= 2050:
            raise ValueError('year out of range [1900, 2050)')
        yearIdx = LuYear - 1900
        for i in range(yearIdx):
            offset += yearDays[i]

        offset += _calcDays(Info.yearInfos[yearIdx], LuMonth, LuDay, LuLeapMonth)
        print(cls._startDate + datetime.timedelta(days=offset))
        return cls._startDate + datetime.timedelta(days=offset)


if __name__ == '__main__':
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day-7)
    LunarSolar.Lunar2Solar(1984,10,12,1)
    
