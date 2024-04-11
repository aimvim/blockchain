import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

#查看未审核的任务（只有已审核的任务才能被志愿者看到）
@app.route("/NotCheckedMission",methods=['GET'])
def NotCheckedMission():
    '''
    传入的json为
    {
    ”page":1
    }
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where checked = "not" and status="not finished" limit {},4;'.format(4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where checked = "not" and status="not finished"')
        num = cursor.fetchone()['num']
        if result==():
            response = [{'num': num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e),500


@app.route("/CheckedMission",methods=['GET'])
def CheckedMission():
    '''
    传入的json为
    {
    ”page":1
    }
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where checked = "yes" and status="not finished" limit {},4;'.format(4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where checked = "yes" and status="not finished"')
        num = cursor.fetchone()['num']
        print(num)
        if result == ():
            response=[{'num':num}]
            return jsonify(response)
        else:
            result.append({"num": num})
            cursor.close()
            db.close()
            return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e),500

#点开任务卡的信息应该是前端自己反馈的吧
#这里我就做一个通过任务的api
@app.route("/passmission",methods=['GET'])
def passmission():
    #onclick——当点击通过之后
    #{"id":id}   --这里的id是个序号，不是用户名哦，前面都会返回id的
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = 'update mission_published set checked="yes" where id = {}'.format(id)
    try:
        cursor.execute(sql)
        db.commit()
        return "Success!",200
    except Exception as e:
        return jsonify(e),500

@app.route("/SelectCheckedMission",methods=['GET'])
def SCM():
    ''''
    传入json为
    {
    "input":inout
    }
    '''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
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
        return jsonify(e),500

@app.route("/SelectNotCheckedMission",methods=['GET'])
def SNCM():
    ''''
    传入json为
    {
    "input":inout
    }
    '''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
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
        return jsonify(e),500

#这个API的作用是返回未审核的账户
@app.route("/NtUser")
def UN():
    ''''
    输入json
    {
    "page":page
    }'''
    page=request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from userinfo where checked='not' limit {},4".format(4*page-4)
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
            return jsonify(result),200
    except Exception as e:
        return jsonify(e),500

@app.route("/PassUser",methods=['GET'])
def passuser():
    '''
    {"id":id}  --这里的id是用户的用户名
    '''
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = 'update userinfo set checked = "yes" where id="{}"'.format(id)
        cursor.execute(sql)
        db.commit()
        return jsonify('Success!'),200
    except Exception as e:
        return jsonify(str(e)),500

#返回已经通过审核的用户
@app.route("/CtUser")
def CN():
    ''''
    输入json
    {
    "page":page
    }'''
    page=request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from userinfo where checked='yes' limit {},4".format(4*page-4)
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
            return jsonify(result),200
    except Exception as e:
        return jsonify(e),500

@app.route("/SelectNtUser")
def SUN():
    ''''
    输入json
    {
    "input":page
    }'''
    input=request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
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
        return jsonify(e),500

@app.route("/SelectCtUser")
def SCN():
    ''''
    输入json
    {
    "input":page
    }'''
    input=request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
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
        return jsonify(e),500

@app.route("/Check/SubmittedProof",methods=['GET'])
def CSP():
    ''''
    {"page":page}--编号
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where id in (select id from proof_table) and status="not finished" limit {},4'.format(4*page-4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where id in (select id from proof_table) and status="not finished"')
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
        return jsonify(str(e)),500

@app.route("/Finished/SubmittedProof",methods=['GET'])
def FSP():
    ''''
    {"page":page}--编号
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where id in (select id from proof_table) and status="finished" limit {},4'.format(4*page-4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute('select count(*) as num from mission_published where id in (select id from proof_table) and status="finished"')
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
        return jsonify(str(e)),500

#打开审核界面
@app.route("/CCpage")
def ccp():
    ''''
    传入
    {"id":id}
    '''
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where id={}'.format(id)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = 'select proof from proof_table where id={}'.format(id)
        cursor.execute(sql)
        proof = cursor.fetchone()['proof']
        result.update({"proof":proof})
        return jsonify(result),200
    except Exception as e:
        return jsonify(str(e)),500

#管理员通过proof
@app.route("/PassProof", methods=['GET'])
def PP():
    '''{"id":id}'''
    data = request.get_json()
    mission_id = data['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
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
            sql = 'select pk from pkadress where id = "{}"'.format(mission_id)
            cursor.execute(sql)
            sig = cursor.fetchone()['pk']
            sql = 'select senderadress from pkadress where id = "{}"'.format(mission_id)
            cursor.execute(sql)
            sed = cursor.fetchone()['senderadress']
            sql = 'INSERT INTO transaction VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (sig, sed, amount-0.1, 0.1, uploader, "not", None, 0))
            db.commit()
    except Exception as e:
        return jsonify(str(e)), 500
    finally:
        db.close()
    return jsonify({"success": True}), 200






if __name__=="__main__":
    app.run()
