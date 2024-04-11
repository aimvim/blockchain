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
    "username":username, -- 用户的名称
    "id":id,
    "name":name, -- 任务的name
    "area":area, -- 任务的area
    }
    '''
    data = request.get_json()  # 一次性获取请求数据
    username = data['username']
    id = data['id']
    try:
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain",cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        # 使用参数化查询
        sql = 'SELECT volunteer FROM mission_published WHERE id = {}'.format(id)
        cursor.execute(sql)
        volunteer = cursor.fetchone()['volunteer']
        print(volunteer)
        if volunteer==None:
            volunteer = username + "?"
        else:
            volunteer = volunteer + username + "?"
        cursor.execute('UPDATE mission_published SET volunteer = %s WHERE id = %s', (volunteer, id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify("Success"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#查询已接取的任务
@app.route("/MissionCatched", methods=['GET'])
def MS():
    ''''
    json
    {"id":id,"page":page}
    '''
    data = request.get_json()
    user_id = data['id']
    page = int(data['page'])
    offset = (page - 1) * 4  # 假设'page'从1开始
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT * FROM mission_published WHERE volunteer LIKE %s LIMIT %s, 4'
            cursor.execute(sql, (f'%{user_id}%', offset))
            result = cursor.fetchall()
            count_sql = 'SELECT COUNT(*) AS num FROM mission_published WHERE volunteer LIKE %s'
            cursor.execute(count_sql, (f'%{user_id}%',))
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
    user_id = data['id']
    page = int(data['page'])
    offset = (page - 1) * 4  # 假设'page'从1开始

    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT * FROM mission_published WHERE volunteer LIKE %s and status="finished" and id in (select id from proof_table where uploader = %s) LIMIT %s, 4'
            cursor.execute(sql, (f'%{user_id}%',user_id,offset))
            result = cursor.fetchall()
            count_sql = 'SELECT COUNT(*) AS num FROM mission_published WHERE volunteer LIKE %s and status="finished" and id in (select id from proof_table where uploader = %s)'
            cursor.execute(count_sql, (f'%{user_id}%',user_id))
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

#下面这个API的作用是完成任务的proof上传,即上传证明材料
@app.route("/UpdateProof",methods=['GET'])
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
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor()
    sql = "insert into proof_table value({},'{}','{}')".format(id,pu,uploader)
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



@app.route("/TXPublish", methods=['GET'])
def TXPublish():
    '''
    传入
    {
    "private_key":
    "Senderadress": sed,
    "Amount": am,
    "Fees": fees,
    "Recipient": rep
    }
    '''
    try:
        data = request.get_json()
        #sig = data['Signature']
        sd = data['Senderadress']  # Fixed typo
        am = data['Amount']
        fees = data['Fees']
        rep = data['Recipient']  # Fixed capitalization
        sk = data['private_key']
        value={"private_key":sk,"sender_adress":sd,"amount":am,"recipient":rep,"Fees":fees}
        print(value)
        sk = binascii.unhexlify(value['private_key'])  # 这里将私钥做成字节串格式
        print(sk)
        pk = GenPk(sk)  # 生成公钥
        # 现在生成的sk与pk都是字节串格式
        pk = binascii.hexlify(pk).decode()
        print(pk)
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'select adress from pkadress where adress="{}"'.format(value['sender_adress'])
        sql1 = 'select adress from pkadress where adress="{}"'.format(value['recipient'])
        # 检验私钥是否正确
        sql2 = 'select pk from pkadress where adress="{}"'.format(value['sender_adress'])
        try:
            print("12")
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
                print(tx_nonce)
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
                Sig = GenSig(sk, str(data))
                sig = Sig
                print(sig)
        except Exception as e:
            return jsonify(str(e)), 500


        # Check sender's balance
        msql = 'SELECT amount FROM pkadress WHERE adress=%s'
        cursor.execute(msql, (sd,))
        sender_amount = cursor.fetchone()
        if sender_amount is not None and sender_amount['amount'] >= (fees + am):
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
            print(result3)
            # Check if any necessary account is missing
            if None in (result1, result2, result3):
                cursor.close()
                db.close()
                return jsonify({"success": False}), 500
            else:
                # Update sender's transaction nonce
                sql4 = 'UPDATE pkadress SET tx_nonce=%s WHERE adress=%s'
                cursor.execute(sql4, (result3['tx_nonce'] + 1, sd))
                db.commit()

                # Insert transaction into database
                sql = 'INSERT INTO `transaction` (`signature`, `senderadress`, `amount`, `fees`, `recipient`, `onchain`, `tx_nonce`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                values = (sig, sd, am, fees, rep, "not", result3['tx_nonce'] + 1)
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
        cursor.execute('select adress from pkadress where id=%s',(miner))
        miner = cursor.fetchone()['adress']
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
    "username":
    ""page":page
    }
    '''
    data =request.get_json()
    username=data['username']
    page=data['page']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('select * from pkadress where id=%s',(username))
        address = cursor.fetchone()['adress']
        sql = "SELECT signature,senderadress,amount,fees,recipient FROM transaction WHERE miner LIKE '%{}%' and onchain='not' limit {},4".format(address, 4 * page - 4)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute("select count(*) as num FROM transaction WHERE miner LIKE '%{}%' and onchain='not'".format(address))
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
    {"id":user}
    '''
    tx = []
    id = request.get_json()['id']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from pkadress where id=%s',(id))
    id = cursor.fetchone()['adress']
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

@app.route("/chain")#该API可以直接访问所有区块
def chain():
    return jsonify(blockchain.blockchain),200

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
        db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'select signature,senderadress,amount,fees,recipient FROM transaction WHERE miner LIKE "%{}%"'.format(id)
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
                    cursor.execute('update pkadress set amount={} where adress="{}"'.format(ramount - amount - fees, senderadress))
                    db.commit()
                    cursor.execute('select amount from pkadress where adress=%s', (recipient))
                    rpamount = cursor.fetchone()['amount']
                    cursor.execute(
                        'update pkadress set amount={} where adress="{}"'.format(rpamount + amount + fees, recipient))
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
        return jsonify(str(e)),500

#下面这个api作用是查找交易信息
@app.route("/TxInfo",methods=['GET'])
def txinfo():
    ''''传入的消息
    json{"adress":}
    '''
    data = request.get_json()
    adress = data['adress']
    db = pymysql.connect(host="localhost", user="root", passwd="123456", port=3306, db="blockchain")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        sql = 'select signature,senderadress,amount,fees,recipient,tx_nonce from transaction where onchain="not" and (senderadress="{}" or recipient="{}")'.format(adress,adress)
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(result),200
    except Exception as e:
        return jsonify(e),500

@app.route("/AcCreate",methods=['GET'])
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
        adress = AdCre(private_key,id)
    except Exception as e:
        return e
    response = {
        "sk":binascii.hexlify(private_key).decode(),
        "pk":binascii.hexlify(publick_key).decode(),
        "adress":adress,
        "WARNING!":"请保存好你的私钥！"
    }
    return jsonify(response)


@app.route("/lll",methods=['GET'])
def lll():
    data = request.get_json()
    return jsonify(data)

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
