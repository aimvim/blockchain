import hashlib
import json
import time
from argparse import ArgumentParser
from urllib.parse import urlparse
from blockchain.functions.Account import *
import requests
from flask import Flask, request, jsonify

class BlockChain:
    def __init__(self):
        self.blockchain = []  # blockchain中存在多个区块
        self.nodes = []
        self.transaction = []  # 出块奖励的交易信息都将存放在这里，更多交易信息自由决定
        self.TheBlockAward = 50

    def add_block(self,block):#添加区块，并对其正确性进行验证
        #merkle_root prehash index的检验在其中操作
        last_block = self.blockchain[-1]
        if block['blockheader']['merkle_root'] != self.MerkleRoot(block['block']):
            return False#对比两者merkle_root值是否相同
        elif block['blockheader']['index'] == self.blockchain[-1]['blockheader']['index'] + 1:
                if self.POW(last_block, block):
                    self.blockchain.append(block)
                    return True
                else:
                    return False
        else:
                return False

    # 生成创世区块
    def genesis_block(self):
        genesis = {
            "blockheader": {  # timestamp->不同时间下值还不同
                "version": 1.0,
                "prehash": "00000000000000000000000000000000000000000000000000000000000000000",
                "index": 0,
                "nonce": "0",
                "merkle_root": "0",
                "target": "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            },
            "block": [],
            "timestamp": time.time()  # 时间戳应该不参与hash#写的时候不写出timestamp，但是实际操作时需要加入
        }
        self.blockchain.append(genesis)

    def POW(self,last_block, block):  # 直接工作量证明#目前想法——返回True/False
        if block['blockheader']['prehash'] == self.hash(last_block):  # 直接return True/False
            if (self.hash(block) < block['blockheader']['target']):  # 根据出块时间实时更新target的值
                return True
            else:
                return False
        else:
            return False

    def hash(self,block):#哈希函数
        block_hash = hashlib.sha256(str(block['blockheader']).encode("utf8"))  # 字符串进行UTF-8编码之后才能进行哈希
        return block_hash.hexdigest()

        # 注册节点

    def register_node(self,address):#注册节点
        parsed_url = urlparse(address)
        # 如果网络地址不为空，那么就添加没有http://之类修饰的纯的地址，如：www.baidu.com
        if parsed_url.netloc:
            self.nodes.append(parsed_url.netloc)
        # 如果网络地址为空，那么就添加相对Url的路径
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.append(parsed_url.path)
        else:
            raise ValueError('Invalid URL')  # 说明这是一个非标准的Url

    def longest_chain(self):#处理不同节点中区块链长度不同的问题
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.blockchain)
        for node in neighbours:
            response = requests.get(f"http://{node}/chain")#到每个节点的chain页面
            if response.status_code == 200:
                length = response.json()[-1]['blockheader']['index'] + 1
                chain = response.json()#直接得到该节点上的链
                if length > max_length:
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.blockchain = new_chain
            return True
        else:
            return False

    def TheBlokCheck(self,block):  # 这是针对单个区块的检查，还需要对整个链上的区块进行检查
        required = ["blockheader", "block"]
        blockheader_required = ["version", "prehash", "index", "nonce", "merkle_root", "target"]
        block_required = []  # block由多个交易组成数组 block=[transaction1,transaction2,...]
        value = True
        if not all(k in block for k in required):
            return False
        elif not all(l in block['blockheader'] for l in blockheader_required):
            return False  # 已经完成对区块头部的验证
        else:
            value = self.CheckTransactions(block['block'])  # 完成对整个区块的检验
        return value

    def TheTransactionCheck(self,new_transaction):  # 判断交易格式是否符合要求
        # 应该设置单个交易检查与整体交易检查
        #后续检验签名是否正确以及UTXO(是否有钱)
        required = ["data","index","signature"]
        data_required=["inputs","outputs","Fees"]
        inputs_required = [ "tx_nonce","sender_adress"]
        outputs_required = ["amount", "recipient"]
        if not all(k in new_transaction for k in required):
            return False
        elif not all(x in new_transaction["data"] for x in data_required):
            return False
        elif not all(l in new_transaction['data']["inputs"] for l in inputs_required):
            return False
        elif not all(p in new_transaction['data']['outputs'] for p in outputs_required):
            return False
        else:#之前是检查格式是否正确，接下来是检查每个交易是否正确签名了
            signature = new_transaction['signature']#先得到具体的签名值
            sender_adress = new_transaction['data']['inputs']['sender_adress']
            recipient = new_transaction['data']['outputs']['recipient']
            db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
            tx_nonce = new_transaction['data']['inputs']['tx_nonce']
            cursor = db.cursor()
            sql1 = 'select pk from pkadress where adress="{}"'.format(sender_adress)
            sql2 = 'select adress from pkadress where adress="{}"'.format(recipient)
            sql3 = 'select tx_noce from pkadress where adress={}'.format(sender_adress)
            cursor.execute(sql1)
            result1 = cursor.fetchone()
            cursor.execute(sql2)
            result2 = cursor.fetchone()
            cursor.execute(sql3)
            result3 = cursor.fetchone()
            if (result1 or result2 or result3 == tx_nonce+1) == None:#任何一个账户是不存在的
                cursor.close()
                db.close()
            else:
                Spk =binascii.unhexlify(result1['pk'])#Spk是sender的公钥
                if VerifySig(Spk,str(new_transaction['data'],signature)):#验证签名是否符合要求
                    sql4 = 'update table pkadress set tx_nonce={} where adress="{}"'.format(result3, sender_adress)
                    cursor.execute(sql4)
                    db.commit()
                    cursor.close()
                    db.close()
                else:
                    return False


    def CheckTransactions(self,tx):  # 这里是check，自动排序等会儿重写
        length = len(tx)
        for i in range(0, length):
            if self.TheTransactionCheck(tx[i]):  # 首先检查交易的格式
                # 交易格式合格
                if i + 1 != tx[i]['index']:
                    # 下标不合格
                    return False
            else:
                # 交易格式不合格
                return False
        return True

    def AddTheTransaction(self,transaction):  # 根据用户提交的交易内容，返回整个交易的信息
        if self.TheTransactionCheck(transaction):
            # 格式正确
            # 之后需要继续检测签名是否合法
            transaction.append(transaction)  # 将交易信息全部放入
            return True
        else:
            return False

        # 左右两个节点生成方法是通过直接拼接得到的
    def data_hash(self, data):  # 要求输入的data是字符串类型
        data_hash = hashlib.sha256(data.encode("utf8")).hexdigest()
        return data_hash

    def MerkleRoot(self,block):  # block中存放的全部都是交易内容
        HashList = []
        if len(block) == 0:
            return 0
        else:
            for tx in block:
                HashList.append(self.data_hash(str(tx)))  # 将所有交易加密之后放上
        while len(HashList) != 1:  # 重复下述操作
            if len(HashList) % 2 == 0:  # HashList长度为偶数
                v = []
                for i in range(0, len(HashList), 2):
                    v.append(self.data_hash(str(HashList[i]) + str(HashList[i + 1])))
                HashList = v
            else:
                v = []
                for i in range(0, len(HashList) - 1, 2):
                    v.append(self.data_hash(str(HashList[i]) + str(HashList[i + 1])))
                v.append(self.data_hash(str(HashList[-1])))
                HashList = v
        return HashList[0]



