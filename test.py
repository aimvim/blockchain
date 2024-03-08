def TheBlokCheck(block):
  required = ["blockheader", "block"]
  blockheader_required = ["version", "prehash", "index", "nonce", "merkle_root", "target"]
  block_required = []  # block由多个交易组成数组 block=[transaction1,transaction2,...]
  value = True
  if not all(k in block for k in required):
    return False
  elif not all(l in block['blockheader'] for l in blockheader_required):
    return False  # 已经完成对区块头部的验证
  else:
    value = CheckTransactions(block['block'])  # 完成对整个区块的检验
  return value


def TheTransactionCheck(new_transaction):  # 判断交易格式是否符合要求
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


def CheckTransactions(tx):  # 这里是check，自动排序等会儿重写
  length = len(tx)
  for i in range(0, length):
    if TheTransactionCheck(tx[i]):  # 首先检查交易的格式
      # 交易格式合格
      if i + 1 != tx[i]['index']:
        # 下标不合格
        return False
    else:
      # 交易格式不合格
      return False
  return True

block = {
"blockheader":{
"version":1,
"prehash":"ea29697a2791965d3f3587360acdfffa4e215c87adb405cacb66712850dde935",
"index":1,
"nonce":1,
"merkle_root":1,
"target":"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
},
"block":[{
    "index":1,
  "inputs": {
    "sender_signature": 1,
    "transaction_reference": 1
  },
  "outputs": {
    "amount": 1,
    "recipient": 1
  },
  "Fees":0
},{
    "index":2,
  "inputs": {
    "sender_signature": 1,
    "transaction_reference": 1
  },
  "outputs": {
    "amount": 1,
    "recipient": 1
  },
  "Fees":0
}]
}

transaction=[{
    "index":1,
  "inputs": {
    "sender_signature": 1,
    "transaction_reference": 1
  },
  "outputs": {
    "amount": 1,
    "recipient": 1
  },
  "Fees":0
},{
    "index":2,
  "inputs": {
    "sender_signature": 1,
    "transaction_reference": 1
  },
  "outputs": {
    "amount": 1,
    "recipient": 1
  },
  "Fees":0
}]

print(len(transaction))