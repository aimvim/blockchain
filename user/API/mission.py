import json

from flask import Flask, request, jsonify
from pymysql import MySQLError

from user.functions.func import *
import pymysql
app = Flask(__name__)


@app.route("/PublishedMission",methods=['GET'])
def PM():
    #针对传入信息
    '''
    {
    "id":id
    "page":123
    }
    '''
    #对具体返回消息的要求可以进行更改
    #完成对分页的要求
    '''此处返回的类型为list类型'''
    data = request.get_json()
    page = data['page']
    db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published_{} limit {},4;'.format(data['id'],4*(page-1))
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(result),200#返回消息的全部信息

@app.route("/FinishedMission",methods=['GET'])
def FM():
    #针对传入信息
    '''
    {
    "id":id,
    "page":123
    }
    '''
    #对具体返回消息的要求可以进行更改
    #完成对分页的要求
    data = request.get_json()
    page = data['page']
    db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_finished_{} where status="finished" limit {},4;'.format(data['id'],4*(page-1))
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(result),200

@app.route("/select", methods=['GET'])
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
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM mission_published_{} WHERE name="{}";'.format(data['id'], input_value)
        # 尝试执行SQL查询
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result:
            return jsonify({"error": "No results found"}), 400
        else:
            return jsonify(result), 200
    except MySQLError as e:
        # 处理数据库连接错误或查询错误
        return jsonify({"error": str(e)}), 400

@app.route("/Publish/Mission",methods=['GET'])
def publishMission():
    '''
    得到的文件格式为
    {
    "id":"id",
    "name":---,
    "area":---,
    "begintime":---,
    "endtime":---,
    "mcharacter":---,
    "details":---
    }
    '''
    value = request.get_json()
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor()
    cursor.execute("select count(*) from mission_published")
    result = cursor.fetchone()[0]
    sql = 'insert into mission_published_{}( `name`, `area`, `begintime`, `endtime`, `mcharacter`, `details`,`status`) value ("{}", "{}", "{}", "{}", "{}", "{}","not finished");'.format(value['id'],value['name'], value['area'], value['begintime'], value['endtime'], value['mcharacter'], value['details'])
    sql1 = 'insert into mission_published( `name`, `area`, `begintime`, `endtime`, `mcharacter`, `details`,`status`) value ( "{}", "{}", "{}", "{}", "{}", "{}","not finished");'.format( value['name'], value['area'], value['begintime'], value['endtime'], value['mcharacter'], value['details'])
    #sql将数据存入自己的表单，sql1将数据存总表单
    try:
        cursor.execute(sql)
        db.commit()
        cursor.execute(sql1)
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Mission published successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()