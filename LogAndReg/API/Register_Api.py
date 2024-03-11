import hashlib
from flask import Flask,request
import pymysql

app = Flask(__name__)
@app.route("/user_register",methods=['POST'])
def user_register():
    UserInfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
    except Exception as e:
        return e #如果数据库连接失败则返回错误原因
    cursor = db.cursor()
    #密码存入数据库中采用密文的形式
    CryptPasswd = hashlib.sha256(UserInfo["password"].encode("utf8")).hexdigest()#哈希函数加密使用utf8编码形式
    sql ='insert into UserInfo values("{}","{}")'.format(UserInfo['id'],CryptPasswd)#将user信息加入到数据库中
    #将注册信息加入到数据库中，或者返回id已被使用的错误
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return "注册成功"
    except Exception as e:
        return str(e)
@app.route("/admin_register",methods=['POST'])
def admin_register():
    admininfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
    except Exception as e:
        return str(e)
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    #首先判断注册码是否正确
    sql = "select code from register_code"
    cursor.execute(sql)
    result = cursor.fetchall()
    code = {'code':"{}".format(admininfo['register_code'])}
    if code not in result:
        return "Wrong Code!"
    else:#注册码正确则直接注册
        CryptPasswd = hashlib.sha256(admininfo["password"].encode("utf8")).hexdigest() #哈希函数加密使用utf8编码形式
        sql = 'insert into admininfo value("{}","{}")'.format(admininfo['id'],CryptPasswd)
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return "注册成功"
        except Exception as e:
            return str(e)

@app.route("/volunteer_register",methods=['POST'])
def volunteer_register():
    VolunteerInfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
    except Exception as e:
        return e #如果数据库连接失败则返回错误原因
    cursor = db.cursor()
    #密码存入数据库中采用密文的形式
    CryptPasswd = hashlib.sha256(VolunteerInfo["password"].encode("utf8")).hexdigest()#哈希函数加密使用utf8编码形式
    sql ='insert into VolunteerInfo values("{}","{}")'.format(VolunteerInfo['id'],CryptPasswd)#将user信息加入到数据库中
    #将注册信息加入到数据库中，或者返回id已被使用的错误
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return "注册成功"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()

'''
API说明：
传入数据为json格式（下面有一个user.json可以看看）
返回值 1，注册成功 2.注册失败的错误信息
PS:三种不同的用户使用了三张不同的表，但是密码加密保存（64位），id最长8位，建议前端再做一次不允许为空的方式
'''
