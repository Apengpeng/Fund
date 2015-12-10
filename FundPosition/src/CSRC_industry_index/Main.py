# _*_coding:utf-8 _*_

import xlrd
import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="A123123123",  charset="utf8")
cursor = db.cursor()

def  CSRC():
    index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18]
    row_list = []
    for i in range(0,len(index)):
        fname = "C:\\Users\\Administrator\\Desktop\\CSRC\\"+str(index[i])+".xls"
        print(fname)
        bk = xlrd.open_workbook(fname)  
        try:
            sh = bk.sheet_by_index(0)
        except:
            print("no sheet in %s named Sheet1" % fname)
        nrows = sh.nrows
       
        for i in range(1,nrows-6):
            indexid = sh.cell_value(i,0)
            time = xlrd.xldate.xldate_as_datetime(sh.cell_value(i,2),0)
            value = sh.cell_value(i,6)
            print((indexid,time,value))
            row_list.append((indexid,time.strftime("%Y-%m-%d"),value))
    return row_list

def CSRCSQL(param):
    sql = "INSERT INTO fund.csrc_industry_index (indexid, datatime, value) VALUES (%s, %s, %s);"
    if(param == None):
        print("Error")
        return None
    print(sql)
    cursor.executemany(sql,param)
    db.commit()
    print('Finish!!!')

data = CSRC()
CSRCSQL(data)