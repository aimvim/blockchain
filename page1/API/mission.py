import json

from flask import Flask, request, jsonify
from page1.functions.func import *
import pymysql
app = Flask(__name__)


@app.route("/PublishedMission",methods=['GET'])
def PM():
    #针对传入信息
    '''
    {
    "page":123
    }
    '''
    #对具体返回消息的要求可以进行更改
    #完成对分页的要求
    '''此处返回的类型为list类型'''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published limit {},4;'.format(4*(page-1))
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result,200

@app.route("/FinishedMission",methods=['GET'])
def FM():
    #针对传入信息
    '''
    {
    "page":123
    }
    '''
    #对具体返回消息的要求可以进行更改
    #完成对分页的要求
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost",user="root",passwd="123456",port=3306,db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_finished limit {},4;'.format(4*(page-1))
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result,200

@app.route("/select",methods=['GET'])
def select():
    '''
    输入格式为
    {
    "input":popo
    }
    '''
    input = request.get_json()['input']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from mission_published where name="{}";'.format(input)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result,200

@app.route("/Publish/Mission",methods=['GET'])
def publishMission():
    '''
    得到的文件格式为
    {
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
    sql = 'insert into mission_published (`id`, `name`, `area`, `begintime`, `endtime`, `mcharacter`, `details`) value ({}, "{}", "{}", "{}", "{}", "{}", "{}");'.format((result+1), value['name'], value['area'], value['begintime'], value['endtime'], value['mcharacter'], value['details'])
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Mission published successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()