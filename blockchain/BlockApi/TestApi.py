import hashlib
import json
import time
from argparse import ArgumentParser
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from blockchain.functions.blockchain import *

blockchain = BlockChain()
blockchain.genesis_block()
app = Flask(__name__)
print(blockchain.hash(blockchain.blockchain[0]))

# 交易验证交给API内部来处理
########################################
#这里api还挺麻烦的，写的时候可能需要两边对接下
########################################
@app.route("/AddNewBlock", methods=["POST"])
def AddNewBlock():
    block = request.get_json()
    # 还应该检查block的格式
    if blockchain.TheBlokCheck(block):
        # 格式确认
        if blockchain.add_block(block):
            # 区块确认
            msg = "挖矿成功"
            print(msg)
            Award_Transaction = {
                "inputs": {
                    "index": len(blockchain.transaction) + 1,  # 变量名和函数名不要同名，否则会引起冲突
                    "sender_signature": 0,
                    "transaction_reference:": "NULL"
                },
                "outputs": {
                    "amount": blockchain.TheBlockAward,
                    "recipient": "recipident"
                },
                "Fees": 0
            }
            blockchain.transaction.append(Award_Transaction)  # 只有这一步是必须的，后面的返回值可以修改
            value = {"msg": msg,
                     "Award_Transaction": Award_Transaction}
            return jsonify(value), 200
        else:
            msg = "错误区块"
            return msg, 200
    else:
        return "区块格式错误", 200

@app.route("/chain")#该API可以直接访问所有区块
def chain():
    return jsonify(blockchain.blockchain),200

@app.route('/PreHash',methods=['GET'])
def prehash():
    last_block = blockchain.blockchain[-1]
    return blockchain.hash(last_block),200

@app.route('/transaction',methods=['Get'])
def TransactionInfo():#返回所有交易信息
    pass

@app.route('/nodes/register',methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if len(nodes) == 0:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'msg':"New nodes added!",
        'nodes':list(blockchain.nodes)
    }
    return jsonify(response)
#测试时使用的json文件为
#{"nodes":["","",""]}

@app.route("/LongChain",methods=['GET'])
def longchain():
    replaced = blockchain.longest_chain()
    if replaced:
        response={
            'msg':"This chain was replaced!",
            "new_chain":blockchain.blockchain
        }
    else:
        response={
            'msg': "This chain is the longest!",
            "new_chain": blockchain.blockchain
        }
    return jsonify(response),200

@app.route("/test",methods=['get'])
def test():
    response = requests.get("http://127.0.0.1:5000/chain")
    print(response.json())
    return "True";


if __name__ == "__main__":
    app.run()
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(debug=True, host='0.0.0.0', port=port)