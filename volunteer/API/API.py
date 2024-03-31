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
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="test")
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

if __name__=="__main__":
    app.run()
