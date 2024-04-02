import pymysql
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
#注册的时候应该考虑一下身份验证的问题
#管理员，志愿者，用户应该使用不同的数据库
#user登录成功后返回id信息和背靠的公司信息
@app.route("/UserLogin",methods=['POST'])
def userlogin():
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="blockchain")
    cursor = db.cursor()
    userinfo = request.get_json()
    sql = 'select password from userinfo where id="{}"'.format(userinfo['id'])# 查询的时候具体一列还是全部元素
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    sql = 'select checked from userinfo where id="{}"'.format(userinfo['id'])
    cursor.execute(sql)
    state_code =cursor.fetchone()[0]
    if result == None:
        return "Id not exist",400
    elif state_code == "not":
        return "Id not exist", 400
    else:
        CryptPassword = hashlib.sha256(userinfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result:
            sql = 'select register_code from userinfo where id ="{}"'.format(userinfo['id'])
            cursor.execute(sql)
            register_code = cursor.fetchone()[0]
            sql = 'select company from register_code where code = "{}"'.format(register_code)
            cursor.execute(sql)
            company = cursor.fetchone()[0]
            msg={"id":userinfo['id'],
                 "company":company}
            return jsonify(msg),200
        else:
            return "Id or password is wrong!",400


@app.route("/AdminLogin",methods=['POST'])
def adminlogin():
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    admininfo = request.get_json()
    sql = 'select * from admininfo where id="{}"'.format(admininfo['id'])  # 查询的时候具体一列还是全部元素
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return "Id not exist",400
    else:
        CryptPassword = hashlib.sha256(admininfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result['password']:
            return "True!",200
        else:
            return "Id or password is wrong!",400



#volunteer登录成功后，会返回他的账户的信息
@app.route("/VolunteerLogin",methods=['POST'])
def volunteerlogin():
    '''
    {
    "id":id,
    "password":password
    }
    :return:
    '''
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    userinfo = request.get_json()
    sql = 'select * from volunteerinfo where id="{}"'.format(userinfo['id'])# 查询的时候具体一列还是全部元素
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except Exception as e:
        return jsonify(e),500
    if result == None:
        return "Id not exist",400
    else:
        CryptPassword = hashlib.sha256(userinfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result['password']:
            #登录成功后返回信息
            sql = "select * from pkadress where id='{}'".format(userinfo['id'])
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close() # 关闭数据库连接
            return jsonify(result),200
        else:
            db.close() # 关闭数据库连接
            return "Id or password is wrong!",400



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