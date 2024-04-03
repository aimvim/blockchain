import pymysql
from flask import Flask, request, jsonify
from volunteer.functions.blockchain import *
from volunteer.functions.Account import *

blockchain = BlockChain()
blockchain.genesis_block()
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
@app.route("/MissionCatched",methods=['GET'])
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
        cursor.execute('select count(*) as num from mission_published_{} where checked = "yes" and status="not finished"'.format(id))
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
        cursor.execute('select count(*) as num from mission_published_{} where checked = "yes" and status="not finished"'.format(id))
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

#下面这个API的作用是完成任务的proof上传,即上传证明材料
@app.route("/UpdateProof",methods=['GET'])
def UP():
    ''''
    传入的json为
    {
    "id":id
    "proof":pu --即上传的图片的url
    }
    多传name和area是方便我定位使用的
    '''
    data = request.get_json()
    id = data['id']
    pu = data['proof']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = "insert into proof_table value({},'{}')".format(id,pu)
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
@app.route("/sig/tx/publish",methods=['POST'])
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
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
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


#返回prehash的值
@app.route('/PreHash',methods=['GET'])
def prehash():
    last_block = blockchain.blockchain[-1]
    return blockchain.hash(last_block),200

@app.route('/index',methods=['GET'])
def index():
    return len(blockchain)

@app.route("/tx/merkleroot", methods=['GET'])
def TxRoot():
    ''''传入json
    {"id":adr}
    '''
    tx = []
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM transaction WHERE miner LIKE '{}%'".format(id)
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
        index = index+1
        tx.append(response)
    db.close()
    # Assuming blockchain.MerkleRoot is a valid function returning the Merkle root
    # Ensure this function exists and is correctly implemented
    print(tx)
    return blockchain.MerkleRoot(tx)

@app.route("/version",methods=['GET'])
def version():
    return "1.0"

@app.route("/mine",methods=['GET'])#最后了宝贝
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
    data = request.get_json()
    indexx = data['blockheader']['index']
    version = data['blockheader']['version']
    prehash = data['blockheader']['prehash']
    nonce = data['blockheader']['nonce']
    merkle_root = data['blockheader']['merkle_root']
    target = data['blockheader']['target']
    tx = []
    id = data['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select SELECT signature,senderadress,amount,fees,recipient FROM transaction WHERE miner LIKE "{}%"'.format(id)
    cursor.execute(sql)
    result = cursor.fetchall()
    index = 1
    for data in result:
        cursor.execute('SELECT tx_nonce FROM transaction WHERE senderadress=%s', (data['senderadress'],))
        tx_nonce_row = cursor.fetchone()
        tx_nonce = tx_nonce_row['tx_nonce']
        response = {
            "index": indexx,
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
    "blockheader":{
    "version":version,
    "prehash":prehash,
    "index":index,
    "nonce":nonce,
    "merkle_root":merkle_root,
    "target":target
    },
    "block":tx}
    if blockchain.TheBlokCheck(block):
        # 格式确认
        if blockchain.add_block(block):
            # 区块确认
            #上链成功后实现所有的交易，并且实现出块奖励
            msg = "挖矿成功"
            print(msg)
            #实现交易
            for data in result:
                senderadress = data['senderadress']
                recipient = data['recipient']
                amount = data['amount']
                fees = data['fees']
                signature = data['signature']
                cursor.execute('update transaction set onchain="yes" where signature=%s',(signature))
                db.commit()
                cursor.execute('select amount from pkadress where adress=%s',(senderadress))
                ramount = cursor.fetchone()['amount']
                cursor.execute('update pkadress set amount={} where adress="{}"'.format(ramount-amount-fees,senderadress))
                db.commit()
                cursor.execute('select amount from pkadress where adress=%s', (recipient))
                rpamount= cursor.fetchone()['amount']
                cursor.execute('update pkadress set amount={} where adress="{}"'.format(rpamount + amount + fees, recipient))
            cursor()
            #实现出块奖励
            cursor('insert into transaction(`signature`,`senderadress`,`amount`,`fees`,`recipient`,`tx_nonce`) value("{}","{}",{},{},"{}",{})'.format("system","system",9.9,0.1,id,0))
            db.commit()
            return jsonify("Success"), 200
        else:
            msg = "错误区块"
            return msg, 200
    else:
        return "区块格式错误", 200








#这里不同纯粹是数据类型的问题
tx= [{
            "index": 0,
            "data": {
                "inputs": {
                    "sender_adress":"123",
                    "tx_nonce": 0
                },
                "outputs": {
                    "amount":1.0,
                    "recipient":"mcosmocmosmcosm,ocmsomcosdm",
                    "Fees":0.1
                }
            },
            "signature":"dih"
        },


    {
            "index": 1,
            "data": {
                "inputs": {
                    "sender_adress":'123',
                    "tx_nonce": 0
                },
                "outputs": {
                    "amount":1.0,
                    "recipient":"mcosmocmosmcosm,ocmsomcosdm",
                    "Fees":0.1
                }
            },
            "signature":"dih"
        }]
print(tx)
print(blockchain.MerkleRoot(tx))

#给出侧边框的数据







if __name__=="__main__":
    app.run()
