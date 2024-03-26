import hashlib
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

#user注册需要邀请码和证明材料，并且需要等待后才能进行
@app.route("/volunteer_register",methods=['POST'])
def volunteer_register():
    UserInfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
    except Exception as e:
        return e,400 #如果数据库连接失败则返回错误原因
    cursor = db.cursor()
    #密码存入数据库中采用密文的形式
    CryptPasswd = hashlib.sha256(UserInfo["password"].encode("utf8")).hexdigest()#哈希函数加密使用utf8编码形式
    sql ='insert into VolunteerInfo values("{}","{}")'.format(UserInfo['id'],CryptPasswd)#将user信息加入到数据库中
    #将注册信息加入到数据库中，或者返回id已被使用的错误
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return "注册成功",200
    except Exception as e:
        return str(e),400

#admin的注册需要邀请码和注册码

@app.route("/admin_register",methods=['POST'])
def admin_register():
    '''
    传入的文档
    {
    "id":id,
    "passwd":passwd,
    "invite_code":inco,
    "register_code":rco
    }
    '''
    admininfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
    except Exception as e:
        return str(e),400
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    #首先判断注册码是否正确
    sql = "select code from register_code"
    cursor.execute(sql)
    result = cursor.fetchall()
    code = {'code':"{}".format(admininfo['register_code'])}
    if code not in result:
        return "Wrong Register Code!",400
    else:#注册码正确则验证邀请码
        sql = "select invite_code from admininfo"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        InviteCode = {'invite_code':"{}".format(admininfo['invite_code'])}
        print(InviteCode)
        if InviteCode not in result:
            return "Wrong Invite Code!",400
        else:
            #随机为管理员生成邀请码，并将管理员信息加入数据库
            #只有status为0的管理员具有邀请码，邀请码之后可以设计为随时间改变的
            CryptPasswd = hashlib.sha256(admininfo["passwd"].encode("utf8")).hexdigest()  # 哈希函数加密使用utf8编码形式
            sql = 'insert into admininfo(`id`,`password`,`register_code`,`status`) value("{}","{}","{}",{});'.format(admininfo['id'],CryptPasswd,admininfo['register_code'],1)
            #之后可以为超级管理员添加更多的权限
            #register_code可以看管理员背靠哪一家公司
            #注册码为"system"的背靠系统
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return jsonify(True),200

#volunteer的登录注册是最简易的，不需要任何的审核
@app.route("/user_register",methods=['POST'])
def user_register():
    '''
    输入的json格式为
    {
    "id":id,
    "passwd":pwd,
    "register_code":rco,
    "proof":url
    }
    '''
    VolunteerInfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,charset="utf8",db="blockchain")
    except Exception as e:
        return e #如果数据库连接失败则返回错误原因
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    #密码存入数据库中采用密文的形式
    CryptPasswd = hashlib.sha256(VolunteerInfo["passwd"].encode("utf8")).hexdigest()#哈希函数加密使用utf8编码形式
    sql = "select code from register_code"
    cursor.execute(sql)
    result = cursor.fetchall()
    code = {'code': "{}".format(VolunteerInfo['register_code'])}
    if code not in result:
        return "Wrong Register Code!",400
    else:
        sql = 'insert into userinfo value("{}","{}","{}","{}","not");'.format(VolunteerInfo['id'],CryptPasswd,VolunteerInfo['register_code'],VolunteerInfo['proof'])
        # 将注册信息加入到数据库中，或者返回id已被使用的错误
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return "注册成功",200
        except Exception as e:
            return str(e),400

if __name__ == "__main__":
    app.run()

'''
API说明：
传入数据为json格式（下面有一个user.json可以看看）
返回值 1，注册成功 2.注册失败的错误信息
PS:三种不同的用户使用了三张不同的表，但是密码加密保存（64位），id最长8位，建议前端再做一次不允许为空的方式
'''
