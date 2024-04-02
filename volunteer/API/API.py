import pymysql
from flask import Flask, request, jsonify
from volunteer.functions.blockchain import *
from volunteer.functions.Account import *

blockchain = BlockChain()

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



#返回交易的信息
@app.route("/ShowTX",methods=['GET'])
def STX():
    ''''
    传入json
    {"page":1}
    '''
    page = request.get_json()['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = 'select * from transaction where onchain="not" limit {},6;'.format(6 * (page - 1))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result), 200  # 返回消息的全部信息
    except Exception as e:
        return jsonify(e), 500



#发布交易A——表中自动返回签名
@app.route("/tx/publish",methods=['POST'])
def TxPublish():
    #返回对交易的签名
    '''
    {
    "private_key":,
    "sender_adress":,
    "amount":,
    "Fees":
    }
    :return:
    '''
    value = request.get_json()#得到表单中的数据
    sk = binascii.unhexlify(value['private_key'])
    pk = GenPk(sk) # 生成公钥
    #现在生成的sk与pk都是字节串格式
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
    cursor = db.cursor()
    sql = 'select adress from pkadress where adress="{}"'.format(value['sender_adress'])
    sql1 = 'select adress from pkadress where adress="{}"'.format(value['recipient'])
    cursor.execute(sql)
    result1 = cursor.fetchone()
    cursor.execute(sql1)
    result2 = cursor.fetchone()
    if (result1 or result2) == None:
        cursor.close()
        db.close()
        return "Account Not Exist!"
    else:
        sql2 = 'select tx_nonce from pkadress where adress="{}"'.format(value['sender_adress'])
        cursor.execute(sql2)
        tx_nonce = cursor.fetchone()[0]
        data = {
            "inputs": {
                "sender_adress": value['sender_adress'],
                "tx_nonce":tx_nonce+1,
            },
            "outputs": {
                "amount": value['amount'],
                "recipient":value['recipient'],
                "Fees":value['Fees']
            }
        }
        Sig = GenSig(sk,str(data))
        cursor.close()
        db.close()
        return jsonify(Sig),200

#发布交易，将交易加入数据库

@app.route("/TXPublish", methods=['GET'])
def TXPublish():
    '''
    传入
    {
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
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
        cursor = db.cursor()
        msql = 'select amount from pkadress where adress=%s'
        cursor.execute(msql, (sd,))
        sender_amount = cursor.fetchone()[0]
        if sender_amount >= (fees + am):
            sql1 = 'select pk from pkadress where adress=%s'
            sql2 = 'select adress from pkadress where adress=%s'
            sql3 = 'select tx_nonce from pkadress where adress=%s'
            cursor.execute(sql1, (sd,))
            result1 = cursor.fetchone()
            cursor.execute(sql2, (rep,))
            result2 = cursor.fetchone()
            cursor.execute(sql3, (sd,))
            result3 = cursor.fetchone()
            if None in (result1, result2, result3):  # 任何一个账户是不存在的
                cursor.close()
                db.close()
                return jsonify({"success": False}), 500
            else:
                sql4 = 'update pkadress set tx_nonce=%s where adress=%s'
                cursor.execute(sql4, (result3[0] + 1, sd))
                db.commit()
                sql = 'INSERT INTO transaction(`signature`,`senderadress`,`amount`,`fees`,`recipient`,`onchain`) VALUES (%s, %s, %s, %s, %s, %s)'
                values = (sig, sd, am, fees, rep, "not")
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


@app.route("/AddToMyBlock", methods=['GET'])
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
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'select miner from transaction where signature=%s and senderadress=%s and amount=%s and fees=%s and recipient=%s '
        value = (sig, sd, am, fees, rep)
        cursor.execute(sql, value)
        result = cursor.fetchone()
        result = result['miner']
        if result:
            new = result + miner + "?"
        else:
            new = miner+"?"
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

#用户查看自己加入的交易
@app.route("/SeeMyBlock",methods=['POST'])
def SMB():
    ''''
    传入json
    {
    “adress”:adress
    ""page":page
    }
    '''
    data =request.get_json()
    address= data['adress']
    page=data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql="SELECT signature,senderadress,amount,fees,recipient FROM transaction WHERE miner LIKE '{}%' and onchain='not' limit {},4".format(address,4*page-4)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result),200
    except Exception as e:
        return jsonify(str(e)), 500



@app.route('/PreHash',methods=['GET'])
def prehash():
    last_block = blockchain.blockchain[-1]
    return blockchain.hash(last_block),200

@app.route("/tx/merkleroot",methods=['GET'])
def TxRoot():#使用方法——输入交易返回最终root值
    ''''传入json
    {"id":adr}
    '''
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from transaction where miner like '{}%'".format(id)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    index = 0
    for data in result:
        response={

        }








    return blockchain.MerkleRoot(tx)




#给出侧边框的数据
@app.route("DetailInformation",methods=['POST'])
def DI():
    ''''
    "version":1.0,
    "prehash":调用'/PreHsh'这个API,
    "index":lenth(blockchain),
    "nonce":这个需要填入
    "merkle_root":调用'tx/merkleroot'这个API
    "target":也是自动生成
    '''







if __name__=="__main__":
    app.run()
