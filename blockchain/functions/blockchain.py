import hashlib
import json
import time
from argparse import ArgumentParser
from urllib.parse import urlparse
from flask import Flask, request, jsonify

class BlockChain:
    def __init__(self):
        self.blockchain = []  # blockchain中存在多个区块
        self.nodes = []
        self.transaction = []  # 出块奖励的交易信息都将存放在这里，更多交易信息自由决定
        self.TheBlockAward = 50

    def add_block(self,block):
        last_block = self.blockchain[-1]
        if block['blockheader']['index'] == self.blockchain[-1]['blockheader']['index'] + 1:
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

    def hash(self,block):
        block_hash = hashlib.sha256(str(block['blockheader']).encode("utf8"))  # 字符串进行UTF-8编码之后才能进行哈希
        return block_hash.hexdigest()

        # 注册节点

    def register_node(self,address):
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

    def longest_chain(self):
        neighbours = self.nodes
        new_chain = None
        pass  # 需要先知道访问哪个位置

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
        required = ["inputs", "outputs", "Fees", "index"]
        inputs_required = ["sender_signature", "transaction_reference"]
        outputs_required = ["amount", "recipient"]
        if not all(k in new_transaction for k in required):
            return False
        elif not all(l in new_transaction["inputs"] for l in inputs_required):
            return False
        elif not all(p in new_transaction['outputs'] for p in outputs_required):
            return False
        else:
            return True

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

    def MerkleRoot(self,tx):
        # 该函数的最终返回值为根哈希值
        pass

