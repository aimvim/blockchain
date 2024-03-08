import pymysql

db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute('select * from userinfo where id="io"')
result = cursor.fetchone()#使用fetchall的时候会将元素放在统一的数组当中
print(result)

cursor.close()
db.close()
