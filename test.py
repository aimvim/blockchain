import pymysql

db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

cursor.execute("select pk from pkadress where adress='1LKzJ8UXzmrnfTv2PxDcMxUzR5irE7g8je'")
result = cursor.fetchone()
print(result['pk'])
print(type(result))
cursor.close()
db.close()

x= None
Y="123"
print(x and Y)