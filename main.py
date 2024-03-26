import pymysql

try:
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, charset="utf8", db="blockchain")
except Exception as e:
    print(str(e))
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
# 首先判断注册码是否正确
sql = "select code from register_code"
cursor.execute(sql)
result = cursor.fetchall()
print(result)