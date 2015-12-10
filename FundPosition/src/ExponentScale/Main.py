# _*_coding:utf-8 _*_
from WindPy import w
from _datetime import date
from math import isnan
import pymysql
import xlrd


w.start()
print('connection wind success', w.isconnected())

db = pymysql.connect(host="localhost", user="root", passwd="A123123123", charset="utf8")
cursor = db.cursor()
"""季度数据  | 股票投资市值"""
def ExponentScale(fundid=None, begintime='2010-01-01', endtime=date.today()):
    if(fundid == None):
        fundid = FundID()
        
    param = (fundid, 'prt_totalasset', begintime, endtime, 'Period=Q', 'Fill=Previous')
    data = w.wsd(*param)
    Value = []
    for i in range(0, len(data.Codes)):
        for j in range(0, len(data.Data[0])):
            stockvalue = data.Data[i][j]
            print(stockvalue)
            if(stockvalue is None or isnan(stockvalue)):
                stockvalue = 0.0
            record = (data.Codes[i], data.Times[j].strftime("%Y-%m-%d"), stockvalue)
            print(record)
            Value.append(record)
            
    return Value

"""插入数据库，股票投资市值"""
def ExponentScaleSQL(param):
    sql = "INSERT INTO fund.exponentscale (fundid,time,value) VALUES (%s, %s, %s);"
    if(param == None):
        print("Error")
        return None
    print(sql)
    cursor.executemany(sql, param)
    db.commit()
    print('Finish!!!')

"""行业配置数据"""
def IndustryConfiguration(fundid=None, industry=None, begintime='2010-01-01', endtime=date.today()):
    if(fundid == None):
        print("没选择基金，默认为全部基金")
        fundid = FundID()
        
    if(industry == None):
        print("未选择行业，默认为全部19个新证监会行业指标")
        industry = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15,16, 17, 18, 19]

    Value = []
    for k in range(0, len(industry)):
        param = (fundid, 'prt_stockvalue_industrytoasset2', begintime, endtime,
                 'industry=' + str(industry[k]), 'Period=Q', 'Fill=Previous')
        data = w.wsd(*param)
        
        if(data.ErrorCode != 0):
            print("Wind  Error")
            
        for i in range(0, len(data.Codes)):
            for j in range(0, len(data.Data[0])):
                value = data.Data[i][j]
                if(value is None or isnan(value)):
                    value = 0.0
                record = (data.Codes[i], data.Times[j].strftime("%Y-%m-%d"), industry[k], value)
                Value.append(record)
    return Value


def IndustryConfigurationSQL(param):
    sql = "INSERT INTO fund.industryconfiguration (fundid,datatime,industryID,value) \
        VALUES (%s, %s, %s, %s);"
    if(param == None):
        print("Error")
        return None
    print(sql)
    cursor.executemany(sql, param)
    db.commit()
    print('Finish!!!')
    
def  FundID():
    fname = r'C:\Users\Administrator\Desktop\fundid.xls'
    bk = xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_name("fundid")
    except:
        print("no sheet in %s named Sheet1" % fname)
    nrows = sh.nrows
    row_list = []
    for i in range(1, nrows):
        row_data = sh.cell_value(i, 0)
        row_list.append(row_data)
    fundid = row_list
    fund = ''
    for item in  range(0, len(fundid)):
        fund = fund + str(fundid[item]) + ','
    fund = fund[:-1]
    return fund
   

#data = ExponentScale(begintime='2012-01-01')
# ExponentScaleSQL(data)

data = IndustryConfiguration(begintime='2013-01-01')
IndustryConfigurationSQL(data)

    





















