import pymysql

db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="blockchain")
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute("select code from register_code")
result = cursor.fetchall()
print(result)
cursor.close()
db.close()
