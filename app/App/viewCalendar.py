from flask import Blueprint, request, redirect, current_app
from flask import Flask, render_template, request, url_for, redirect, make_response, json, jsonify
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
import uuid
import requests
# str(uuid.uuid4()) to generate random string, used as unique string. like id.

# from .models import *
import json
import jmespath
import os
from werkzeug.utils import *
import html
import markdown
# from mermaid import *
from .stringHandler import *
from .jsonFileHandler import *
from .actionHandler import *

from datetime import *
from .DateInfo import DateInfo


def day_lunar(ld):
    a = '初一 初二 初三 初四 初五 初六 初七 初八 初九 初十\
         十一 十二 十三 十四 十五 十六 十七 十八 十九 廿十\
         廿一 廿二 廿三 廿四 廿五 廿六 廿七 廿八 廿九 三十'.split()
    return a[ld - 1]


def numDay(m, leap):
    a = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (leap and m == 2):
        return 29
    else:
        return a[m - 1]


def month_lunar(le, lm):
    a = '正月 二月 三月 四月 五月 六月 七月 八月 九月 十月 十一月 十二月'.split()
    if le:
        return "闰" + a[lm - 1]
    else:
        return a[lm - 1]


def year_lunar(ly):
    y = ly
    tg = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split()
    dz = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split()
    sx = '鼠 牛 虎 兔 龙 蛇 马 羊 猴 鸡 狗 猪'.split()
    return tg[(y - 4) % 10] + dz[(y - 4) % 12] + '[' + sx[(y - 4) % 12] + ']' + '年'


def weekday_str(tm):
    a = '星期日 星期一 星期二 星期三 星期四 星期五 星期六'.split()
    return a[tm]


def outCalendar(dateInfo):
    g = dateInfo
    calendarInfo = \
        str(g.year) + "年" + str(g.month) + "月" + str(g.day) + "日" + " " \
        + weekday_str(g.weekday) + " 农历" + year_lunar(g.luYear) \
        + month_lunar(g.luIsleap, g.luMonth) \
        + day_lunar(g.luDay) + "\n"
    print(calendarInfo)
    return calendarInfo


# blueprint is used for route. Blueprint would be used at create_app, in __init__.py.
# We can have more blueprints, with different name, and at create_app side, register them one by one.
calendarBP = Blueprint('calendar', __name__)



@calendarBP.route('/calendar/', methods=['get'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def showCalendar():
    preList = []
    curList = []
    nxtList = []
    thisDay = date.today()
    year = thisDay.year
    month = thisDay.month
    day = thisDay.day
    selDay = {
        "year": year,
        "month": month,
        "day": day
    }

    dateStr = str(year) + "-" + str(month) + "-" + str(day);
    print(dateStr)
    ddd = datetime.strptime(dateStr, "%Y-%m-%d")
    selDay = DateInfo(ddd)
    selDay.cout()
    preMonth = 12 if (selDay.month == 1) else selDay.month - 1;
    print(preMonth)
    totalNumOfDayPreMonth = numDay(preMonth, selDay.leapYear)
    totalNumOfDayCurMonth = numDay(selDay.month, selDay.leapYear)
    mod7Temp = (8 - (selDay.day + 7 - selDay.weekday) % 7) % 7
    mod7 = 0
    for i in range(0, mod7Temp):
        preList.append(totalNumOfDayPreMonth + i - mod7Temp + 1)
        mod7 = mod7 + 1
    for i in range(0, totalNumOfDayCurMonth):
        curList.append(i + 1)
        mod7 = (mod7 + 1) % 7
    for i in range(0, (7 - mod7) % 7):
        curList.append(i + 1)

    print(selDay.firstdayWeek)
    print(selDay.lastweekDay)
    selectDayDetail = outCalendar(selDay)

    return render_template('calendar.html', preList=preList, curList=curList, nxtList=nxtList, date=selDay,
                           selectDayDetail=selectDayDetail)


@calendarBP.route('/preMCalendar/<int:year>/<int:month>/<int:day>/', methods=['get'])
def preMCalendar(year, month, day):
    preList = []
    curList = []
    nxtList = []
    if month == 1:
        month = 12
        year = year - 1
    else:
        month = month - 1
    selDay = {
        "year": year,
        "month": month,
        "day": day
    }
    dateStr = str(year) + "-" + str(month) + "-" + str(day);
    ddd = datetime.strptime(dateStr, "%Y-%m-%d")
    selDay = DateInfo(ddd)
    preMonth = 12 if (selDay.month == 1) else selDay.month - 1;
    totalNumOfDayPreMonth = numDay(preMonth, selDay.leapYear)
    totalNumOfDayCurMonth = numDay(selDay.month, selDay.leapYear)
    mod7Temp = (8 - (selDay.day + 7 - selDay.weekday) % 7) % 7
    mod7 = 0
    for i in range(0, mod7Temp):
        preList.append(totalNumOfDayPreMonth + i - mod7Temp + 1)
        mod7 = mod7 + 1
    for i in range(0, totalNumOfDayCurMonth):
        curList.append(i + 1)
        mod7 = (mod7 + 1) % 7
    for i in range(0, (7 - mod7) % 7):
        curList.append(i + 1)
    selectDayDetail = outCalendar(selDay)
    return render_template('calendar.html', preList=preList, curList=curList, nxtList=nxtList, date=selDay,
                           selectDayDetail=selectDayDetail)


@calendarBP.route('/nextMCalendar/<int:year>/<int:month>/<int:day>/', methods=['get'])
def nextMCalendar(year, month, day):
    preList = []
    curList = []
    nxtList = []
    if month == 12:
        month = 1
        year = year + 1
    else:
        month = month + 1
    selDay = {
        "year": year,
        "month": month,
        "day": day
    }
    dateStr = str(year) + "-" + str(month) + "-" + str(day);
    ddd = datetime.strptime(dateStr, "%Y-%m-%d")
    selDay = DateInfo(ddd)
    preMonth = 12 if (selDay.month == 1) else selDay.month - 1;
    totalNumOfDayPreMonth = numDay(preMonth, selDay.leapYear)
    totalNumOfDayCurMonth = numDay(selDay.month, selDay.leapYear)
    mod7Temp = (8 - (selDay.day + 7 - selDay.weekday) % 7) % 7
    mod7 = 0
    for i in range(0, mod7Temp):
        preList.append(totalNumOfDayPreMonth + i - mod7Temp + 1)
        mod7 = mod7 + 1
    for i in range(0, totalNumOfDayCurMonth):
        curList.append(i + 1)
        mod7 = (mod7 + 1) % 7
    for i in range(0, (7 - mod7) % 7):
        curList.append(i + 1)
    selectDayDetail = outCalendar(selDay)
    return render_template('calendar.html', preList=preList, curList=curList, nxtList=nxtList, date=selDay,
                           selectDayDetail=selectDayDetail)


@calendarBP.route('/today/', methods=['get'])
def today():
    preList = []
    curList = []
    nxtList = []
    thisDay = date.today()
    year = thisDay.year
    month = thisDay.month
    day = thisDay.day
    selDay = {
        "year": year,
        "month": month,
        "day": day
    }
    dateStr = str(year) + "-" + str(month) + "-" + str(day);
    ddd = datetime.strptime(dateStr, "%Y-%m-%d")
    selDay = DateInfo(ddd)
    preMonth = 12 if (selDay.month == 1) else selDay.month - 1;
    totalNumOfDayPreMonth = numDay(preMonth, selDay.leapYear)
    totalNumOfDayCurMonth = numDay(selDay.month, selDay.leapYear)
    mod7Temp = (8 - (selDay.day + 7 - selDay.weekday) % 7) % 7
    mod7 = 0
    for i in range(0, mod7Temp):
        preList.append(totalNumOfDayPreMonth + i - mod7Temp + 1)
        mod7 = mod7 + 1
    for i in range(0, totalNumOfDayCurMonth):
        curList.append(i + 1)
        mod7 = (mod7 + 1) % 7
    for i in range(0, (7 - mod7) % 7):
        curList.append(i + 1)
    selectDayDetail = outCalendar(selDay)
    return render_template('calendar.html', preList=preList, curList=curList, nxtList=nxtList, date=selDay,
                           selectDayDetail=selectDayDetail)


@calendarBP.route('/curMCalendar/<int:year>/<int:month>/<int:day>/', methods=['get'])
def curMCalendar(year, month, day):
    preList = []
    curList = []
    nxtList = []
    selDay = {
        "year": year,
        "month": month,
        "day": day
    }
    dateStr = str(year) + "-" + str(month) + "-" + str(day);
    ddd = datetime.strptime(dateStr, "%Y-%m-%d")
    selDay = DateInfo(ddd)
    preMonth = 12 if (selDay.month == 1) else selDay.month - 1;
    totalNumOfDayPreMonth = numDay(preMonth, selDay.leapYear)
    totalNumOfDayCurMonth = numDay(selDay.month, selDay.leapYear)
    mod7Temp = (8 - (selDay.day + 7 - selDay.weekday) % 7) % 7
    mod7 = 0
    for i in range(0, mod7Temp):
        preList.append(totalNumOfDayPreMonth + i - mod7Temp + 1)
        mod7 = mod7 + 1
    for i in range(0, totalNumOfDayCurMonth):
        curList.append(i + 1)
        mod7 = (mod7 + 1) % 7
    for i in range(0, (7 - mod7) % 7):
        curList.append(i + 1)
    selectDayDetail = outCalendar(selDay)
    return render_template('calendar.html', preList=preList, curList=curList, nxtList=nxtList, date=selDay,
                           selectDayDetail=selectDayDetail)
