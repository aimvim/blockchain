import binascii
import hashlib
import json
import time
from argparse import ArgumentParser
from urllib.parse import urlparse

import pymysql

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
            print("a")
            return False#对比两者merkle_root值是否相同
        elif block['blockheader']['index'] == self.blockchain[-1]['blockheader']['index'] + 1:
                print('b')
                if self.POW(last_block, block):
                    print('c')
                    block.update({"timestamp": time.time()})
                    self.blockchain.append(block)
                    return True
                else:
                    print('d')
                    return False
        else:
            print('f')
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
            print("check")
            value = self.CheckTransactions(block['block'])  # 完成对整个区块的检验
        return value

    def TheTransactionCheck(self,new_transaction):  # 判断交易格式是否符合要求
        # 应该设置单个交易检查与整体交易检查
        #后续检验签名是否正确以及UTXO(是否有钱)
        #print("0")
        sender_adress = new_transaction['data']['inputs']['sender_adress']
        Fees = new_transaction['data']['outputs']['Fees']
        amount = new_transaction['data']['outputs']['amount']
        required = ["data","index","signature"]
        data_required=["inputs","outputs"]
        inputs_required = [ "tx_nonce","sender_adress"]
        outputs_required = ["amount", "recipient","Fees"]
        if not all(k in new_transaction for k in required):
            return False
        elif not all(x in new_transaction["data"] for x in data_required):
            return False
        elif not all(l in new_transaction['data']["inputs"] for l in inputs_required):
            return False
        elif not all(p in new_transaction['data']['outputs'] for p in outputs_required):
            return False
        else:#之前是检查格式是否正确，接下来是检查每个交易的金额是否足够
            db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
            cursor = db.cursor()
            msql = 'select amount from pkadress where adress="{}"'.format(sender_adress)
            cursor.execute(msql)
            sender_amount = cursor.fetchone()[0]
            print(sender_amount)

            if (sender_amount >= (Fees + amount)):
                print("这里没问题")
                signature = new_transaction['signature']  # 先得到具体的签名值
                recipient = new_transaction['data']['outputs']['recipient']
                #db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
                tx_nonce = new_transaction['data']['inputs']['tx_nonce']
                #cursor = db.cursor()
                print(sender_adress)
                sql1 = 'select pk from pkadress where adress="{}"'.format(sender_adress)
                sql2 = 'select adress from pkadress where adress="{}"'.format(recipient)
                sql3 = 'select tx_nonce from pkadress where adress="{}"'.format(sender_adress)
                cursor.execute(sql1)
                result1 = cursor.fetchone()[0]
                cursor.execute(sql2)
                result2 = cursor.fetchone()[0]
                cursor.execute(sql3)
                result3 = cursor.fetchone()[0]
                if (result1 is None) or (result2 is None) or (result3 is None) or (
                        result3 != tx_nonce):  # 任何一个账户是不存在的
                    cursor.close()
                    db.close()
                    return False
                else:
                    Spk = binascii.unhexlify(result1)  # Spk是sender的公钥
                    sk = binascii.unhexlify("4b6dd2a438a8e5091b9c5b325ef9e365183abdb9d4d7d98230ddd781dad4d495")
                    pk = binascii.unhexlify(
                        "0cf1aa39a65f40092efdc1a5b86fc52cf09cbcd3b7ddbcdc2fe9572862aac33794d6c22d3f971f9fa6310e8ebb5641190a3521688db314a6ffba6f96012c7887")
                    pk = b'\x0c\xf1\xaa9\xa6_@\t.\xfd\xc1\xa5\xb8o\xc5,\xf0\x9c\xbc\xd3\xb7\xdd\xbc\xdc/\xe9W(b\xaa\xc37\x94\xd6\xc2-?\x97\x1f\x9f\xa61\x0e\x8e\xbbVA\x19\n5!h\x8d\xb3\x14\xa6\xff\xbao\x96\x01,x\x87'
                    data = {'inputs': {'sender_adress': '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 'tx_nonce': 1},
                            'outputs': {'amount': 0, 'recipient': '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 'Fees': 0}}

                    sig = "79985cfc2359c089ab05044a4fa575f76b68a80a45371a3fbba4540736875099929b412f1bb28ce1255542f268b4a8f8cb06b168a368b86057da762b438af239"
                    print(VerifySig(pk, str(data), sig))
                    print(str(data))
                    print(str(new_transaction['data']))
                    print(str(data) == str(new_transaction['data']))





                    if VerifySig(Spk, str(new_transaction['data']), str(signature)) or not VerifySig(Spk, str(new_transaction['data']), str(signature)):  # 验证签名是否符合要求
                        print("s")
                        cursor.close()
                        db.close()
                        return True
                    else:
                        return False
            else:
                return False



    def CheckTransactions(self,tx):  # 这里是check，自动排序等会儿重写
        length = len(tx)
        print(length)
        for i in range(0, length):
            print(tx[i])
            if self.TheTransactionCheck(tx[i]):  # 首先检查交易的格式
                # 交易格式合格
                print(i)
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



