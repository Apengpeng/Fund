#_*_coding:utf-8 _*_
from WindPy import w
from _datetime import date
import pymysql
from math import isnan

w.start()
print('connection wind success', w.isconnected())

db = pymysql.connect(host="localhost", user="root", passwd="A123123123", db="fund", charset="utf8")
cursor = db.cursor()

def GetSWexponent(ExponentID=None,BeginTime=None,EndTime=None):
    if(ExponentID==None):
        print("沒有传入申万之一指数代码，数据将返回所有申万一级指数的数据")
        ExponentID = '801010.SI,801020.SI,801030.SI,\
                     801040.SI,801050.SI,801080.SI,801110.SI,\
                     801120.SI,801130.SI,801140.SI,801150.SI,\
                     801160.SI,801170.SI,801180.SI,801200.SI,\
                     801210.SI,801230.SI,801710.SI,801720.SI,\
                     801730.SI,801740.SI,801750.SI,801760.SI,\
                     801770.SI,801780.SI,801790.SI,801880.SI,\
                     801890.SI'
    if(BeginTime==None):
        BeginTime = '2010-01-01'
        
    if(EndTime==None):
        EndTime=date.today();
    
    tmp = (ExponentID,'close',BeginTime,EndTime,'Fill=Previous')
    data = w.wsd(*tmp)
    
    Value = []
    for i in range(0,len(data.Codes)):
        for j in range(0,len(data.Data[0])):
            value = data.Data[i][j];
            if isnan(value):
                value=0.0
            Value.append((str(data.Codes[i]),data.Times[j].strftime("%Y-%m-%d"),str(value)))
    for n in Value:
        print(n)
    return Value

def MYsqlDB(param):
    sql = "INSERT INTO fund.swex (swid, datatime, value) VALUES (%s, %s, %s)"
    print("更新数据库")
    result = cursor.executemany(sql,param)
    print("Finish!!!",result)
    
MYsqlDB(GetSWexponent())