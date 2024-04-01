import pymysql
from flask import Flask, request, jsonify

app=Flask(__name__)

#这里显示已经被管理员审核后的内容，具有分页功能
@app.route("/TheMissionChecked",methods=['GET'])
def TMC():
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


#将任务信息加入到自己的接取中
@app.route("/CatchTheMission", methods=['GET'])
def CTM():
    '''
    传入的json为
    {
    "id":id, -- 用户的名称
    "name":name, -- 任务的name
    "area":area, -- 任务的area
    }
    '''
    data = request.get_json() # 一次性获取请求数据
    id = data['id']
    name = data['name']
    area = data['area']
    try:
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain", cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        # 使用参数化查询
        sql = 'SELECT * FROM mission_published WHERE name=%s AND area=%s'
        cursor.execute(sql, (name, area))
        result = cursor.fetchone()  # 假设只有一条记录匹配
        if result:
            # 使用参数化查询防止SQL注入
            sql = '''INSERT INTO mission_published_{0}(name,area,begintime,endtime,activitytime,award,mcharacter,details,status,checked,uploader,uploader_company) 
                     VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''.format(id)
            print(sql)
            cursor.execute(sql, (
                result['name'], result['area'], result['begintime'],
                result['endtime'], result['activitytime'], result['award'],
                result['mcharacter'], result['details'], result['status'],
                result['checked'], result['uploader'], result['uploader_company']
            ))
            db.commit()
            return jsonify("Success!"), 200
        else:
            return jsonify("No matching mission found."), 404
    except Exception as e:
        return jsonify(str(e)), 500
    finally:
        cursor.close()
        db.close()

#查询已接取的任务
@app.route("/MissionSelected",methods=['GET'])
def MS():
    ''''
    传入的数据json为
    {
    ”id“:id,--id为用户名
    "page":page
    }'''
    data = request.get_json()
    id = data['id']
    page = data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published_{} where checked = "yes" and status="not finished" limit {},4;'.format(
        id,4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500

#查询接取且已完成的任务
@app.route("/CatchMissionFinished",methods=['Get'])
def CMF():
    ''''
    传入的数据json为
    {
    ”id“:id,--id为用户名
    "page":page
    }'''
    data = request.get_json()
    id = data['id']
    page = data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published_{} where checked = "yes" and status="finished" limit {},4;'.format(
        id,4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500

#下面这个API的作用是完成任务的proof上传,即上传证明材料
@app.route("/UpdateProof",methods=['GET'])
def UP():
    ''''
    传入的json为
    {
    "name":name,
    "area":area,
    "proof_url":pu --即上传的图片的url
    }
    多传name和area是方便我定位使用的
    '''
    data = request.get_json()
    name = data['name']
    area = data['area']
    pu = data['proof_url']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = "insert into proof_table value('{}','{}','{}')".format(name,area.pu)
    try:
        cursor.execute(sql)
        db.commit()
        return jsonify("Success!"),200
    except Exception as e:
        return jsonify(e),500


if __name__=="__main__":
    app.run()
