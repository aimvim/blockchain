import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
from API.functions.Account import *
from API.functions.Account_OL import *
from API.functions.blockchain import *

blockchain = BlockChain()
blockchain.genesis_block()
app = Flask(__name__)
CORS(app)


# 查看未审核的任务（只有已审核的任务才能被志愿者看到）
@app.route("/NotCheckedMission", methods=['POST'])
def NotCheckedMission():
    '''
    传入的json为
    {
    ”page":1
    }
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where checked = "not" and status="not finished" limit {},4;'.format(
        4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where checked = "not" and status="not finished"')
        num = cursor.fetchone()['num']
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500


@app.route("/CheckedMission", methods=['POST'])
def CheckedMission():
    '''
    传入的json为
    {
    ”page":1
    }
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where checked = "yes" and status="not finished" limit {},4;'.format(
        4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where checked = "yes" and status="not finished"')
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500


# 点开任务卡的信息应该是前端自己反馈的吧
# 这里我就做一个通过任务的api
@app.route("/passmission", methods=['POST'])
def passmission():
    # onclick——当点击通过之后
    # {"id":id}   --这里的id是个序号，不是用户名哦，前面都会返回id的
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = 'update mission_published set checked="yes" where id = {}'.format(id)
    try:
        cursor.execute(sql)
        db.commit()
        return "Success!", 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/SelectCheckedMission", methods=['POST'])
def SCM():
    ''''
    传入json为
    {
    "input":inout
    }
    '''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where name="{}" and checked="yes" and status="not finished"'.format(input)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            return jsonify({"error": "No results found"}), 500
        else:
            return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/SelectNotCheckedMission", methods=['POST'])
def SNCM():
    ''''
    传入json为
    {
    "input":inout
    }
    '''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where name="{}" and checked="not" and status="not finished"'.format(input)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            return jsonify({"error": "No results found"}), 500
        else:
            return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


# 这个API的作用是返回未审核的账户
@app.route("/NtUser", methods=['POST'])
def UN():
    ''''
    输入json
    {
    "page":page
    }'''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from userinfo where checked='not' limit {},4".format(4 * page - 4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from userinfo where checked = "not"')
        num = cursor.fetchone()['num']
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/PassUser", methods=['POST'])
def passuser():
    '''
    {"id":id}  --这里的id是用户的用户名
    '''
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = 'update userinfo set checked = "yes" where id="{}"'.format(id)
        cursor.execute(sql)
        db.commit()
        return jsonify('Success!'), 200
    except Exception as e:
        return jsonify(str(e)), 500


# 返回已经通过审核的用户
@app.route("/CtUser", methods=['POST'])
def CN():
    ''''
    输入json
    {
    "page":page
    }'''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from userinfo where checked='yes' limit {},4".format(4 * page - 4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from userinfo where checked = "yes"')
        num = cursor.fetchone()['num']
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/SelectNtUser", methods=['POST'])
def SUN():
    ''''
    输入json
    {
    "input":page
    }'''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from userinfo where checked='not' and id='{}'".format(input)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result:
            return jsonify({"error": "No results found"}), 500
        else:
            return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/SelectCtUser", methods=['POST'])
def SCN():
    ''''
    输入json
    {
    "input":page
    }'''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from userinfo where checked='yes' and id='{}'".format(input)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result:
            return jsonify({"error": "No results found"}), 500
        else:
            return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/Check/SubmittedProof", methods=['POST'])
def CSP():
    ''''
    {"page":page}--编号
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where id in (select id from proof_table) and status="not finished" limit {},4'.format(
        4 * page - 4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute(
            'select count(*) as num from mission_published where id in (select id from proof_table) and status="not finished"')
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(str(e)), 500


@app.route("/Finished/SubmittedProof", methods=['POST'])
def FSP():
    ''''
    {"page":page}--编号
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where id in (select id from proof_table) and status="finished" limit {},4'.format(
        4 * page - 4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute(
            'select count(*) as num from mission_published where id in (select id from proof_table) and status="finished"')
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(str(e)), 500


# 打开审核界面
@app.route("/CCpage", methods=['POST'])
def ccp():
    ''''
    传入
    {"id":id}
    '''
    id = request.get_json()['id']
    print(id)
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where id={}'.format(id)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = 'select proof from proof_table where id={}'.format(id)
        cursor.execute(sql)
        proof = cursor.fetchone()['proof']
        result.update({"proof": proof})
        return jsonify(result), 200
    except Exception as e:
        return jsonify(str(e)), 500


# 管理员通过proof
@app.route("/PassProof", methods=['POST'])
def PP():
    data = request.get_json()
    mission_id = data['id']
    print(id)
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            # 使用参数化查询来更新状态
            sql = 'UPDATE mission_published SET status=%s WHERE id = %s'
            cursor.execute(sql, ("finished", mission_id))
            db.commit()

            # 获取奖励金额
            sql = 'SELECT award FROM mission_published WHERE id=%s'
            cursor.execute(sql, (mission_id,))
            amount = cursor.fetchone()['award']
            print(amount)

            # 获取上传者信息
            sql = "SELECT uploader FROM proof_table WHERE id = %s"
            cursor.execute(sql, (mission_id,))
            uploader = cursor.fetchone()['uploader']
            print(uploader)
            sql = 'select adress from pkadress where id="{}"'.format(uploader)
            print(sql)
            cursor.execute(sql)
            uploader = cursor.fetchone()['adress']
            # 插入交易记录
            sql = 'select signature from pkadress where id = "{}"'.format(mission_id)
            cursor.execute(sql)
            sig = cursor.fetchone()['signature']
            sql = 'select senderadress from pkadress where id = "{}"'.format(mission_id)
            cursor.execute(sql)
            sed = cursor.fetchone()['senderadress']
            sql = 'INSERT INTO transaction VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (sig, sed, amount - 0.1, 0.1, uploader, "not", None, 0))
            db.commit()
    except Exception as e:
        return jsonify(str(e)), 500
    finally:
        db.close()
    return jsonify({"success": True}), 200


@app.route("/UserLogin", methods=['POST'])
def userlogin():
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="Wu_CRH.0523", db="blockchain")
    cursor = db.cursor()
    userinfo = request.get_json()
    sql = 'select password from userinfo where id="{}"'.format(userinfo['id'])  # 查询的时候具体一列还是全部元素
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    sql = 'select checked from userinfo where id="{}"'.format(userinfo['id'])
    cursor.execute(sql)
    state_code = cursor.fetchone()[0]
    if result == None:
        return "Id not exist", 400
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
            msg = {"id": userinfo['id'],
                   "company": company}
            return jsonify(msg), 200
        else:
            return "Id or password is wrong!", 400


@app.route("/AdminLogin", methods=['POST'])
def adminlogin():
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="Wu_CRH.0523", db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    admininfo = request.get_json()
    sql = 'select * from admininfo where id="{}"'.format(admininfo['id'])  # 查询的时候具体一列还是全部元素
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return "Id not exist", 400
    else:
        CryptPassword = hashlib.sha256(admininfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result['password']:
            return "True!", 200
        else:
            return "Id or password is wrong!", 400


# volunteer登录成功后，会返回他的账户的信息
@app.route("/VolunteerLogin", methods=['POST'])
def volunteerlogin():
    '''
    {
    "id":id,
    "password":password
    }
    :return:
    '''
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="Wu_CRH.0523", db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    userinfo = request.get_json()
    sql = 'select * from volunteerinfo where id="{}"'.format(userinfo['id'])  # 查询的时候具体一列还是全部元素
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except Exception as e:
        return jsonify(str(e)), 500
    if result == None:
        return "Id not exist", 400
    else:
        CryptPassword = hashlib.sha256(userinfo['password'].encode("utf8")).hexdigest()
        if CryptPassword == result['password']:
            # 登录成功后返回信息
            sql = "select * from pkadress where id='{}'".format(userinfo['id'])
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close()  # 关闭数据库连接
            return jsonify(result), 200
        else:
            db.close()  # 关闭数据库连接
            return "Id or password is wrong!", 400


# user注册需要邀请码和证明材料，并且需要等待后才能进行
@app.route("/volunteer_register", methods=['POST'])
def volunteer_register():
    ''''
    {
    "id":id,
    "password":passwd
    }
    '''
    UserInfo = request.get_json()
    try:
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, charset="utf8",
                             db="blockchain")
    except Exception as e:
        return e, 400  # 如果数据库连接失败则返回错误原因
    cursor = db.cursor()
    # 密码存入数据库中采用密文的形式
    CryptPasswd = hashlib.sha256(UserInfo["password"].encode("utf8")).hexdigest()  # 哈希函数加密使用utf8编码形式
    sql = 'insert into VolunteerInfo values("{}","{}")'.format(UserInfo['id'], CryptPasswd)  # 将user信息加入到数据库中
    # 将注册信息加入到数据库中，或者返回id已被使用的错误
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return "注册成功", 200
    except Exception as e:
        return str(e), 400


# admin的注册需要邀请码和注册码

@app.route("/admin_register", methods=['POST'])
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
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, charset="utf8",
                             db="blockchain")
    except Exception as e:
        return str(e), 400
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # 首先判断注册码是否正确
    sql = "select code from register_code"
    cursor.execute(sql)
    result = cursor.fetchall()
    code = {'code': "{}".format(admininfo['register_code'])}
    if code not in result:
        return "Wrong Register Code!", 400
    else:  # 注册码正确则验证邀请码
        sql = "select invite_code from admininfo"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        InviteCode = {'invite_code': "{}".format(admininfo['invite_code'])}
        print(InviteCode)
        if InviteCode not in result:
            return "Wrong Invite Code!", 400
        else:
            print('s')
            # 随机为管理员生成邀请码，并将管理员信息加入数据库
            # 只有status为0的管理员具有邀请码，邀请码之后可以设计为随时间改变的
            CryptPasswd = hashlib.sha256(admininfo["passwd"].encode("utf8")).hexdigest()  # 哈希函数加密使用utf8编码形式
            sql = 'insert into admininfo(`id`,`password`,`register_code`,`status`) value("{}","{}","{}",{});'.format(
                admininfo['id'], CryptPasswd, admininfo['register_code'], 1)
            # 之后可以为超级管理员添加更多的权限
            # register_code可以看管理员背靠哪一家公司
            # 注册码为"system"的背靠系统
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return jsonify(True), 200


# volunteer的登录注册是最简易的，不需要任何的审核
@app.route("/user_register", methods=['POST'])
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
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, charset="utf8",
                             db="blockchain")
    except Exception as e:
        return str(e), 400  # 如果数据库连接失败则返回错误原因
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # 密码存入数据库中采用密文的形式
    CryptPasswd = hashlib.sha256(VolunteerInfo["passwd"].encode("utf8")).hexdigest()  # 哈希函数加密使用utf8编码形式
    sql = "select code from register_code"
    cursor.execute(sql)
    result = cursor.fetchall()
    code = {'code': "{}".format(VolunteerInfo['register_code'])}
    if code not in result:
        return "Wrong Register Code!", 400
    else:
        # 这里，每个人应该配备自己私人独立的表单(这里就已经创建好了私人的表单)
        sql = 'INSERT INTO userinfo VALUE ("{}","{}","{}","{}","not");'.format(VolunteerInfo['id'], CryptPasswd,
                                                                               VolunteerInfo['register_code'],
                                                                               VolunteerInfo['proof'])
        # 将注册信息加入到数据库中，或者返回id已被使用的错误
        try:
            cursor.execute(sql)
            db.commit()
            sk = GenSk_OL()
            pk = GenPk_OL(sk)
            adress = AdCre_OL(sk, volunteer_register['id'])
            cursor.close()
            db.close()
            return "注册成功", 200
        except Exception as e:
            return str(e), 400


@app.route("/PublishedMission", methods=['POST'])
def PM():
    # 针对传入信息
    '''
    {
    "id":id
    "page":1
    }
    '''
    # 对具体返回消息的要求可以进行更改
    # 完成对分页的要求
    '''此处返回的类型为list类型'''
    data = request.get_json()
    page = data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where uploader ="{}" limit {},4;'.format(data['id'], 4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where uploader=%s', (data['id']))
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500


@app.route("/FinishedMission", methods=['POST'])
def FM():
    # 针对传入信息
    '''
    {
    "id":id,
    "page":123
    }
    '''
    # 对具体返回消息的要求可以进行更改
    # 完成对分页的要求
    data = request.get_json()
    page = data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql1 = "select * from mission_published where status = 'finished' and uploader ='{}' limit {},4".format(data['id'],
                                                                                                            4 * page - 4)
    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where status = "finished" and uploader=%s',
                       (data['id']))
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(str(e)), 500


@app.route("/select", methods=['POST'])
def select():
    '''
    输入格式为
    {
        "input": "popo",
        "id": "id"
    }
    '''
    data = request.get_json()
    input_value = data['input']
    try:
        # 尝试连接数据库
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM mission_published WHERE name="{}" and uploader="{}";'.format(input_value, data['id'])
        # 尝试执行SQL查询
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result:
            return jsonify({"error": "No results found"}), 400
        else:
            return jsonify(result), 200
    except Exception as e:
        # 处理数据库连接错误或查询错误
        return jsonify({"error": str(e)}), 400


@app.route("/Publish/Mission", methods=['POST'])
def publishMission():
    '''
    得到的文件格式为
    {
    "id":"id",
    "name":---,
    "area":---,
    "begintime":---,
    "endtime":---,
    "activitytime":---,
    "award":---,
    "mcharacter":---,
    "details":---
    }
    '''
    value = request.get_json()
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = 'select register_code from userinfo where id ="{}"'.format(value['id'])
    try:
        cursor.execute(sql)
    except Exception as e:
        return jsonify(e), 500
    result = cursor.fetchone()[0]
    try:
        sql = 'select company from register_code where code = "{}"'.format(result)
        cursor.execute(sql)
    except Exception as e:
        return jsonify(e), 200
    company = cursor.fetchone()[0]
    print(company)
    sql = 'insert into mission_published( `name`, `area`, `begintime`, `endtime`, `mcharacter`, `details`,`status`,`uploader`,`activitytime`,`award`,`uploader_company`) value ("{}", "{}", "{}", "{}", "{}", "{}","not finished","{}","{}","{}","{}");'.format(
        value['name'], value['area'], value['begintime'], value['endtime'], value['mcharacter'], value['details'],
        value['id'], value['activitytime'], value['award'], company)
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Mission published successfully"}, value), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 这里显示已经被管理员审核后的内容，具有分页功能
@app.route("/TheMissionChecked", methods=['POST'])
def TMC():
    """
    传入的json为
    {
    ”page":1
    }
    """
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where checked = "yes" and status="not finished" and volunteer IS NULL limit {},4;'.format(
        4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute(
            'select count(*) as num from mission_published where checked = "yes" and status="not finished" and volunteer IS NULL')
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500

    # 将任务信息加入到自己的接取中


@app.route("/CatchTheMission", methods=['POST'])
def CTM():
    """
    传入的json为
    {
    "username":username, -- 用户的名称
    "id":id,
    "name":name, -- 任务的name
    "area":area, -- 任务的area
    }
    """
    data = request.get_json()  # 一次性获取请求数据
    username = data['username']
    id = data['id']
    try:
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain",
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        # 使用参数化查询
        sql = 'SELECT volunteer FROM mission_published WHERE id = {}'.format(id)
        cursor.execute(sql)
        volunteer = cursor.fetchone()['volunteer']
        cursor.execute('UPDATE mission_published SET volunteer = %s WHERE id = %s', (volunteer, id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify("Success"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 查询已接取的任务
@app.route("/MissionCatched", methods=['POST'])
def MS():
    ''''
    json
    {"id":id,"page":page}
    '''
    data = request.get_json()
    print(data)
    user_id = data['id']
    page = int(data['page'])
    offset = (page - 1) * 4  # 假设'page'从1开始

    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT * FROM mission_published WHERE volunteer = %s and status="not finished" LIMIT %s, 4'
            cursor.execute(sql, (user_id, offset))
            result = cursor.fetchall()
            count_sql = 'SELECT COUNT(*) AS num FROM mission_published WHERE volunteer = %s'
            cursor.execute(count_sql, (user_id,))
            num = cursor.fetchone()['num']
            if not result:
                result = [{'num': num}]
            else:
                result.append({"num": num})

            return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# 查询接取且已完成的任务
@app.route("/CatchMissionFinished", methods=['POST'])
def CMF():
    ''''
    传入的数据json为
    {
    ”id“:id,--id为用户名
    "page":page
    }'''
    data = request.get_json()
    user_id = data['id']
    page = int(data['page'])
    offset = (page - 1) * 4  # 假设'page'从1开始

    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT * FROM mission_published WHERE volunteer LIKE %s and status="finished" and id in (select id from proof_table where uploader = %s) LIMIT %s, 4'
            cursor.execute(sql, (user_id, user_id, offset))
            result = cursor.fetchall()
            count_sql = 'SELECT COUNT(*) AS num FROM mission_published WHERE volunteer LIKE %s and status="finished" and id in (select id from proof_table where uploader = %s)'
            cursor.execute(count_sql, (user_id, user_id))
            num = cursor.fetchone()['num']
            if not result:
                result = [{'num': num}]
            else:
                result.append({"num": num})

            return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# 下面这个API的作用是完成任务的proof上传,即上传证明材料
@app.route("/UpdateProof", methods=['POST'])
def UP():
    ''''
    传入的json为
    {
    "id":id
    "proof":pu --即上传的图片的url
    "uploader":
    }
    多传name和area是方便我定位使用的
    '''
    data = request.get_json()
    id = data['id']
    pu = data['proof']
    uploader = data['uploader']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = "insert into proof_table value({},'{}','{}')".format(id, pu, uploader)
    try:
        cursor.execute(sql)
        db.commit()
        return jsonify("Success!"), 200
    except Exception as e:
        return jsonify(e), 500


# 返回交易的信息
@app.route("/ShowTX", methods=['POST'])
def STX():
    ''''
    传入json
    {"page":1}
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from transaction where onchain="not" limit {},6;'.format(6 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from transaction where onchain="not"')
        num = cursor.fetchone()['num']
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500


# 发布交易A——表中自动返回签名
@app.route("/sig/tx/publish", methods=['POST'])
def TxPublish():
    # 返回对交易的签名
    '''
    {
    "private_key":,
    "sender_adress":,
    "amount":,
    "recipient":,
    "Fees":
    }
    :return:
    '''
    value = request.get_json()  # 得到表单中的数据
    sk = binascii.unhexlify(value['private_key'])  # 这里将私钥做成字节串格式
    pk = GenPk(sk)  # 生成公钥
    # 现在生成的sk与pk都是字节串格式
    pk = binascii.hexlify(pk).decode()
    print(sk)
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="Wu_CRH.0523", db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select adress from pkadress where adress="{}"'.format(value['sender_adress'])
    sql1 = 'select adress from pkadress where adress="{}"'.format(value['recipient'])
    # 检验私钥是否正确
    sql2 = 'select pk from pkadress where adress="{}"'.format(value['sender_adress'])
    try:
        cursor.execute(sql)
        result1 = cursor.fetchone()
        cursor.execute(sql1)
        result2 = cursor.fetchone()
        cursor.execute(sql2)
        result3 = cursor.fetchone()
        result3 = result3['pk']
        if result1 == None or result2 == None or result3 != pk:
            cursor.close()
            db.close()
            return "Account Not Exist!"
        else:
            sql2 = 'select tx_nonce from pkadress where adress="{}"'.format(value['sender_adress'])
            cursor.execute(sql2)
            tx_nonce = cursor.fetchone()['tx_nonce']
            data = {
                "inputs": {
                    "sender_adress": value['sender_adress'],
                    "tx_nonce": tx_nonce + 1,
                },
                "outputs": {
                    "amount": value['amount'],
                    "recipient": value['recipient'],
                    "Fees": value['Fees']
                }
            }
            print(str(data))
            Sig = GenSig(sk, str(data))
            cursor.close()
            db.close()
            return jsonify(Sig), 200
    except Exception as e:
        return jsonify(str(e)), 500


# 发布交易，将交易加入数据库

@app.route("/TXPublish", methods=['POST'])
def TXPublish():
    '''
    传入
    {
    “Signature”: sig,
    "Senderadress": sed,
    "Amount": am,
    "Fees": fees,
    "Recipient": rep
    }
    '''
    try:
        data = request.get_json()
        sig = data['Signature']
        sd = data['Senderadress']  # Fixed typo
        am = data['Amount']
        fees = data['Fees']
        rep = data['Recipient']  # Fixed capitalization
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
        cursor = db.cursor()

        # Check sender's balance
        msql = 'SELECT amount FROM pkadress WHERE adress=%s'
        cursor.execute(msql, (sd,))
        sender_amount = cursor.fetchone()
        if sender_amount is not None and sender_amount[0] >= (fees + am):
            # Get necessary data from database
            sql1 = 'SELECT pk FROM pkadress WHERE adress=%s'
            sql2 = 'SELECT adress FROM pkadress WHERE adress=%s'
            sql3 = 'SELECT tx_nonce FROM pkadress WHERE adress=%s'
            cursor.execute(sql1, (sd,))
            result1 = cursor.fetchone()
            cursor.execute(sql2, (rep,))
            result2 = cursor.fetchone()
            cursor.execute(sql3, (sd,))
            result3 = cursor.fetchone()

            # Check if any necessary account is missing
            if None in (result1, result2, result3):
                cursor.close()
                db.close()
                return jsonify({"success": False}), 500
            else:
                # Update sender's transaction nonce
                sql4 = 'UPDATE pkadress SET tx_nonce=%s WHERE adress=%s'
                cursor.execute(sql4, (result3[0] + 1, sd))
                db.commit()

                # Insert transaction into database
                sql = 'INSERT INTO `transaction` (`signature`, `senderadress`, `amount`, `fees`, `recipient`, `onchain`, `tx_nonce`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                values = (sig, sd, am, fees, rep, "not", result3[0] + 1)
                cursor.execute(sql, values)
                db.commit()
                cursor.close()
                db.close()
                return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 500
    except Exception as e:
        # Log the error for debugging
        app.logger.error("An error occurred: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/AddToMyBlock", methods=['POST'])
def ATMB():
    ''''
    传入json
    {
    "miner": miner,
    “Signature": sig,
    "Senderadress": sed,
    "Amount": am,
    "Fees": fees,
    "Recipient": rep
    }
    '''
    try:
        data = request.get_json()
        sig = data['Signature']
        sd = data['Senderadress']  # Fixed typo
        am = data['Amount']
        fees = data['Fees']
        rep = data['Recipient']  # Fixed capitalization
        miner = data['miner']
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'select miner from transaction where signature=%s and senderadress=%s and amount=%s and fees=%s and recipient=%s '
        value = (sig, sd, am, fees, rep)
        cursor.execute(sql, value)
        result = cursor.fetchone()
        result = result['miner']
        if result:
            new = result + miner + "?"
        else:
            new = miner + "?"
        print(new)
        sql = 'update transaction set miner=%s where signature=%s and senderadress=%s and amount=%s and fees=%s and recipient=%s'
        value = (new, sig, sd, am, fees, rep)
        cursor.execute(sql, value)
        db.commit()
        cursor.close()
        db.close()
        return jsonify("Success!"), 200
    except Exception as e:
        return jsonify(str(e)), 500


# 用户查看自己加入的交易
@app.route("/SeeMyBlock", methods=['POST'])
def SMB():
    ''''
    传入json
    {
    “adress”:adress
    ""page":page
    }
    '''
    data = request.get_json()
    address = data['adress']
    page = data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT signature,senderadress,amount,fees,recipient FROM transaction WHERE miner LIKE '%{}%' and onchain='not' limit {},4".format(
        address, 4 * page - 4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute(
            "select count(*) as num FROM transaction WHERE miner LIKE '%{}%' and onchain='not'".format(address))
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(str(e)), 500


# 返回prehash的值
@app.route('/PreHash', methods=['GET'])
def prehash():
    last_block = blockchain.blockchain[-1]
    return blockchain.hash(last_block), 200


@app.route('/index', methods=['GET'])
def index():
    return len(blockchain)


@app.route("/tx/merkleroot", methods=['POST'])
def TxRoot():
    ''''传入json
    {"id":adr}
    '''
    tx = []
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM transaction WHERE miner LIKE '%{}%'".format(id)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    index = 1
    for data in result:
        print(data)
        print(data['senderadress'])
        cursor.execute('SELECT tx_nonce FROM transaction WHERE senderadress=%s', (data['senderadress'],))
        tx_nonce_row = cursor.fetchone()
        tx_nonce = tx_nonce_row['tx_nonce']
        print(tx_nonce)
        response = {
            "index": index,
            "data": {
                "inputs": {
                    "sender_adress": data['senderadress'],
                    "tx_nonce": tx_nonce
                },
                "outputs": {
                    "amount": data['amount'],
                    "recipient": data['recipient'],
                    "Fees": data['fees']
                }
            },
            "signature": data["signature"]
        }
        index = index + 1
        tx.append(response)
    db.close()
    # Assuming blockchain.MerkleRoot is a valid function returning the Merkle root
    # Ensure this function exists and is correctly implemented
    print(tx)
    return blockchain.MerkleRoot(tx)


@app.route("/version", methods=['GET'])
def version():
    return "1.0"


@app.route("/chain")  # 该API可以直接访问所有区块
def chain():
    return jsonify(blockchain.blockchain), 200


@app.route("/mine", methods=['POST'])  # 最后了宝贝
def mine():
    ''''
    传入json为
    {"id": "id",--这个是miner的id
    "blockheader":{
    "version":1,
    "prehash":1,
    "index":1,
    "nonce":1,
    "merkle_root":1,
    "target":1
    }}
    '''
    try:
        data = request.get_json()
        indexx = data['blockheader']['index']
        version = data['blockheader']['version']
        prehash = data['blockheader']['prehash']
        nonce = data['blockheader']['nonce']
        merkle_root = data['blockheader']['merkle_root']
        target = data['blockheader']['target']
        tx = []
        id = data['id']
        db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'select signature,senderadress,amount,fees,recipient FROM transaction WHERE miner LIKE "%{}%"'.format(
            id)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        index = 1
        for data in result:
            cursor.execute('SELECT tx_nonce FROM transaction WHERE senderadress=%s', (data['senderadress'],))
            tx_nonce_row = cursor.fetchone()
            tx_nonce = tx_nonce_row['tx_nonce']
            print(tx_nonce)
            response = {
                "index": index,
                "data": {
                    "inputs": {
                        "sender_adress": data['senderadress'],
                        "tx_nonce": tx_nonce
                    },
                    "outputs": {
                        "amount": data['amount'],
                        "recipient": data['recipient'],
                        "Fees": data['fees']
                    }
                },
                "signature": data["signature"]
            }
            index = index + 1
            tx.append(response)
        block = {
            "blockheader": {
                "version": version,
                "prehash": prehash,
                "index": indexx,
                "nonce": nonce,
                "merkle_root": merkle_root,
                "target": target
            },
            "block": tx}
        if blockchain.TheBlokCheck(block):
            # 格式确认
            print("1")
            if blockchain.add_block(block):
                # 区块确认
                # 上链成功后实现所有的交易，并且实现出块奖励
                msg = "挖矿成功"
                print(msg)
                # 实现交易
                for data in result:
                    senderadress = data['senderadress']
                    recipient = data['recipient']
                    amount = data['amount']
                    fees = data['fees']
                    signature = data['signature']
                    cursor.execute('update transaction set onchain="yes" where signature=%s', (signature))
                    db.commit()
                    cursor.execute('select amount from pkadress where adress=%s', (senderadress))
                    ramount = cursor.fetchone()['amount']
                    cursor.execute('update pkadress set amount={} where adress="{}"'.format(ramount - amount - fees,
                                                                                            senderadress))
                    db.commit()
                    cursor.execute('select amount from pkadress where adress=%s', (recipient))
                    rpamount = cursor.fetchone()['amount']
                    cursor.execute(
                        'update pkadress set amount={} where adress="{}"'.format(rpamount + amount + fees,
                                                                                 recipient))
                    db.commit()
                    cursor.execute('select amount from pkadress where adress=%s', (id))
                    mamount = cursor.fetchone()['amount']
                    cursor.execute('update pkadress set amount = {} where adress="{}"'.format(mamount + fees, id))
                # 实现出块奖励
                cursor.execute(
                    'insert into transaction(`signature`,`senderadress`,`amount`,`fees`,`recipient`,`tx_nonce`) value("{}","{}",{},{},"{}",{})'.format(
                        "system", "system", 9.9, 0.1, id, 0))
                db.commit()
                return jsonify("Success"), 200
            else:
                msg = "错误区块"
                return msg, 200
        else:
            return "区块格式错误", 200
    except Exception as e:
        return jsonify(str(e)), 500


# 下面这个api作用是查找交易信息
@app.route("/TxInfo", methods=['POST'])
def txinfo():
    ''''传入的消息
    json{"adress":}
    '''
    data = request.get_json()
    adress = data['adress']
    db = pymysql.connect(host="localhost", user="root", passwd="Wu_CRH.0523", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        sql = 'select signature,senderadress,amount,fees,recipient,tx_nonce from transaction where onchain="not" and (senderadress="{}" or recipient="{}")'.format(
            adress, adress)
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        return jsonify(e), 500


@app.route("/AcCreate", methods=['POST'])
def AcCreate():
    '''
    传入json
    {
    "id":id --传入用户名
    '''
    id = request.get_json()['id']
    private_key = GenSk()
    publick_key = GenPk(private_key)
    try:
        adress = AdCre(private_key, id)
    except Exception as e:
        return e
    response = {
        "sk": binascii.hexlify(private_key).decode(),
        "pk": binascii.hexlify(publick_key).decode(),
        "adress": adress,
        "WARNING!": "请保存好你的私钥！"
    }
    return jsonify(response)


@app.route("/lll", methods=['GET'])
def lll():
    data = request.get_json()
    return jsonify(data)


# 这里不同纯粹是数据类型的问题
tx = [{
    "index": 0,
    "data": {
        "inputs": {
            "sender_adress": "123",
            "tx_nonce": 0
        },
        "outputs": {
            "amount": 1.0,
            "recipient": "mcosmocmosmcosm,ocmsomcosdm",
            "Fees": 0.1
        }
    },
    "signature": "dih"
},

    {
        "index": 1,
        "data": {
            "inputs": {
                "sender_adress": '123',
                "tx_nonce": 0
            },
            "outputs": {
                "amount": 1.0,
                "recipient": "mcosmocmosmcosm,ocmsomcosdm",
                "Fees": 0.1
            }
        },
        "signature": "dih"
    }]
print(tx)
print(blockchain.MerkleRoot(tx))

# 给出侧边框的数据


if __name__ == "__main__":
    app.run()
