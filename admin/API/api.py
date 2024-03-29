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
    sql = 'select * from mission_published where checked = "not" limit {},4;'.format(4 * (page - 1))
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
    sql = 'select * from mission_published where checked = "yes" limit {},4;'.format(4 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e),500

@app.route("/passmission",methods=['GET'])
def passmission():
    '''
    '''

if __name__=="__main__":
    app.run()
