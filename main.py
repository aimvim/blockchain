import pymysql

db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
cursor = db.cursor()
sql1 = 'select tx_nonce from pkadress where pk="c253670216e617ef702c411791e8e97e871b157088780ef37977e08252b91c1d0736e37cb93a4e157abdbd189ab85f4e308eed4ecde2c22a884a28e6dc910909"'
cursor.execute(sql1)
result = cursor.fetchone()[0]
print(result)