import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute('select * from transaction')
result = cursor.fetchall()
for x in result:
    print(x['amount'])
    print("avbd")