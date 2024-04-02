import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="test")
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = 'select * from mission_published where name="{}" and area="{}"'.format("Mission 3", "area C")
cursor.execute(sql)
result = cursor.fetchall()
print(result)