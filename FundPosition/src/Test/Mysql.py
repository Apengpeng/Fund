import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="A123123123",  charset="utf8")
cur = db.cursor()

sql = "SELECT time,sum(value) FROM fund.exponentscale group by time;"
number=cur.execute(sql)
results=cur.fetchall()
for i in range(0,len(results)):
    sql = "UPDATE fund.exponentscale SET percent =value/"+str(results[i][1])+"  where time='"+str(results[i][0])+"';"
    print(sql)
    cur.execute(sql)
    db.commit()
