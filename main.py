#实现溯源与查找交易记录的功能#
#实现钱包注册功能——直接把用户密码设置为种子来进行使用#
#区块链需要的功能——交易上链、挖矿(挖矿时提供区块的验证)、pow、验证交易、多节点、使用公钥来进行验证（将存在的用户信息保存在数据库中）#
#挖矿假定目标是直接上传一个json的block文件#
import hashlib
import json
import time
from argparse import ArgumentParser
from urllib.parse import urlparse
from flask import Flask, request, jsonify

blockchain = [] #blockchain中存在多个区块
nodes = []
transaction = []#出块奖励的交易信息都将存放在这里，更多交易信息自由决定
TheBlockAward = 50
def add_block(block):
    last_block = blockchain[-1]
    if block['blockheader']['index'] == blockchain[-1]['blockheader']['index']+1:
        if POW(last_block, block):
            block['timestamp'] = time.time()
            blockchain.append(block)
            return True
        else:
            return False
    else:
        return False

#生成创世区块
def genesis_block():
    genesis = {
            "blockheader": {#timestamp->不同时间下值还不同
                "version": 1.0,
                "prehash": "00000000000000000000000000000000000000000000000000000000000000000",
                "index":0,
                "nonce":"0",
                "merkle_root":"0",
                "target":"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            },
            "block":[],
            "timestamp": time.time()#时间戳应该不参与hash#写的时候不写出timestamp，但是实际操作时需要加入
    }
    blockchain.append(genesis)

def POW(last_block,block):#直接工作量证明#目前想法——返回True/False
    if block['blockheader']['prehash'] == hash(last_block):#直接return True/False
        if(hash(block)<block['blockheader']['target']):#根据出块时间实时更新target的值
            return True
        else:
            return False
    else:
        return False

def hash(block):
    block_hash = hashlib.sha256(str(block['blockheader']).encode("utf8"))# 字符串进行UTF-8编码之后才能进行哈希
    return block_hash.hexdigest()

    # 注册节点
def register_node(address):
    parsed_url = urlparse(address)
    # 如果网络地址不为空，那么就添加没有http://之类修饰的纯的地址，如：www.baidu.com
    if parsed_url.netloc:
        nodes.append(parsed_url.netloc)
    # 如果网络地址为空，那么就添加相对Url的路径
    elif parsed_url.path:
        # Accepts an URL without scheme like '192.168.0.5:5000'.
        nodes.append(parsed_url.path)
    else:
        raise ValueError('Invalid URL')  # 说明这是一个非标准的Url

def longest_chain():
    neighbours = nodes
    new_chain = None
    pass#需要先知道访问哪个位置

def TheBlokCheck(block):#这是针对单个区块的检查，还需要对整个链上的区块进行检查
    required = ["blockheader","block"]
    blockheader_required = ["version","prehash","index","nonce","merkle_root","target"]
    block_required=[]#block由多个交易组成数组 block=[transaction1,transaction2,...]
    value = True
    if not all(k in block for k in required):
        return False
    elif not all(l in block['blockheader'] for l in blockheader_required):
        return False#已经完成对区块头部的验证
    else:
            value = CheckTransactions(block['block'])#完成对整个区块的检验
    return value



def TheTransactionCheck(new_transaction):#判断交易格式是否符合要求
    #应该设置单个交易检查与整体交易检查
    required = ["inputs","outputs","Fees","index"]
    inputs_required = ["sender_signature","transaction_reference"]
    outputs_required = ["amount","recipient"]
    if not all(k in new_transaction for k in required):
        return False
    elif not all(l in new_transaction["inputs"] for l in inputs_required):
        return False
    elif not all(p in new_transaction['outputs'] for p in outputs_required):
        return False
    else:
        return True

def CheckTransactions(tx):#这里是check，自动排序等会儿重写
    length = len(tx)
    for i in range(0,length):
        if TheTransactionCheck(tx[i]):#首先检查交易的格式
            #交易格式合格
            if i+1 != tx[i]['index']:
                # 下标不合格
                return False
        else:
            #交易格式不合格
            return False
    return True


def AddTheTransaction(transaction):#根据用户提交的交易内容，返回整个交易的信息
    if TheTransactionCheck(transaction):
        #格式正确
        #之后需要继续检测签名是否合法
        transaction.append(transaction)#将交易信息全部放入
        return True
    else:
         return False


def MerkleRoot(tx):
    # 该函数的最终返回值为根哈希值
    pass


genesis_block()
app = Flask(__name__)
print(hash(blockchain[0]))

#交易验证交给API内部来处理
@app.route("/AddNewBlock",methods=["POST"])
def AddNewBlock():
    block = request.get_json()
    #还应该检查block的格式
    if TheBlokCheck(block):
        #格式确认
        if add_block(block):
            #区块确认
            msg = "挖矿成功"
            print(msg)
            Award_Transaction = {
                "inputs": {
                    "index":len(transaction)+1,# 变量名和函数名不要同名，否则会引起冲突
                    "sender_signature": 0,
                    "transaction_reference:": "NULL"
                },
                "outputs": {
                    "amount": TheBlockAward,
                    "recipient": "recipident"
                },
                "Fees": 0
            }
            transaction.append(Award_Transaction)#只有这一步是必须的，后面的返回值可以修改
            value = {"msg":msg,
                     "Award_Transaction":Award_Transaction}
            return jsonify(value),200
        else:
            msg = "错误区块"
            return msg,200
    else:
        return "区块格式错误",200

@app.route("/chain")#该API可以直接访问所有区块
def chain():
    return jsonify(blockchain),200

@app.route('/PreHash',methods=['GET'])
def prehash():
    last_block = blockchain[-1]
    return hash(last_block),200

@app.route('/transaction',methods=['Get'])
def TransactionInfo():#返回所有交易信息
    pass


if __name__ == "__main__":
    app.run()
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(debug=True, host='0.0.0.0', port=port)