import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="A123123123", db="fund", charset="utf8")
cursor = db.cursor()

def FundAvgProfit():
    fundid = Fundid()
    print("Fundid")
    
    for i in range(0, len(fundid)):
        Value = []
        print(fundid[i][0])
        sql = "SELECT id,value FROM fund_nav.fund where fundid ='" + fundid[i][0] + "' order by datatime"
        cursor.execute(sql)
        results = cursor.fetchall()
        for j in range(1, len(results)):
            newvalue = float(results[j][1])
            beforevalue = float(results[j - 1][1])
            if(newvalue==0 or beforevalue==0):
                profit = 0
            else:   
                profit = (newvalue - beforevalue) / beforevalue
            record = (profit, results[j][0])
            Value.append(record)
        MysqlDB(Value)

def Fundid():
    sql = "SELECT distinct fundid FROM fund_nav.fund;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def MysqlDB(param):
    sql = "update fund_nav.fund set profit=%s where id=%s"
    cursor.executemany(sql, param)
    db.commit()
    
FundAvgProfit()
