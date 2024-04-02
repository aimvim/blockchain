import pymysql
import hashlib
from flask import Flask,request

app = Flask(__name__)
#注册的时候应该考虑一下身份验证的问题
#管理员，志愿者，用户应该使用不同的数据库
@app.route("/UserLogin",methods=['POST'])
def userlogin():
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    userinfo = request.get_json()
    sql = 'select * from userinfo where id="{}"'.format(userinfo['id'])# 查询的时候具体一列还是全部元素
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return "Id not exist"
    else:
        CryptPassword = hashlib.sha256(userinfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result['password']:
            return "True!"
        else:
            return "Id or password is wrong!"


@app.route("/AdminLogin",methods=['POST'])
def adminlogin():
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    admininfo = request.get_json()
    sql = 'select * from admininfo where id="{}"'.format(admininfo['id'])  # 查询的时候具体一列还是全部元素
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return "Id not exist"
    else:
        CryptPassword = hashlib.sha256(admininfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result['password']:
            return "True!"
        else:
            return "Id or password is wrong!"

if __name__ == "__main__":
    app.run()

'''
这个api就是登录时使用，返回值有：
"Id not exist!"
"True!"
"Id or password is wrong!"
针对返回值可以进行修改
id设置的是最长8位
前端最好要求一下不允许空白
'''