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
    sql = "select * from userinfo where checked='not' limit {},6".format(6*page-6)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result),200
    except Exception as e:
        return jsonify(e),500

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
    sql = "select * from userinfo where checked='yes' limit {},6".format(6*page-6)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
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


#这个api的作用是返回提交到管理员处的审核
@app.route("/SubmitMission",methods=['GET'])
def SM():
    ''''
    传入json
    {
    "name":name,
    "area":area
    }
    '''
    data = request.get_json()
    name = data['name']
    area = data['area']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select proof from proof_table where name='{}' and area = '{}'".format(name,area)
    try:
        cursor.execute(sql)
        proof = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(proof),200
    except Exception as e:
        return jsonify(e),500

#当管理员允许时
@app.route("/AdminPassMission",methods=['GET'])
def APM():
    ''''
    {
    "name":name,
    "area":area
    }
    '''
    data = request.get_json()
    name = data['name']
    area = data['area']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="test")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "update mission_published set status='finished' where name='{}' and area='{}'".format(name,area)
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return jsonify("Success!"), 200
    except Exception as e:
        return jsonify(e), 500









if __name__=="__main__":
    app.run()
