import binascii
import hashlib
import os
import base58
import ecdsa
import pymysql


def GenSk():#生成私钥
    PrivateKey = os.urandom(32)
    return PrivateKey #十六进制转二进制之后再调整
def GenPk(PrivateKey):#基于私钥生成公钥，然后生成地址？
    Publick_Key= ecdsa.SigningKey.from_string(
        PrivateKey, curve=ecdsa.SECP256k1).verifying_key.to_string()
    return Publick_Key

#公钥用于签名的验证，地址用来实现转账
def AdCre(private_key):#生成账户地址，并将公钥与地址存入数据库当中
    public_key = GenPk(private_key)
    prefix_and_pubkey = b"\x04" + public_key
    intermediate = hashlib.sha256(prefix_and_pubkey).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(intermediate)
    hash160 = ripemd160.digest()
    prefix_and_hash160 = b"\x00" + hash160
    # 确认嵌套了hashlib.shai9
    double_hash = hashlib.sha256(hashlib.sha256(prefix_and_hash160).digest()).digest()
    checksum = double_hash[:4]
    pre_address = prefix_and_hash160 + checksum
    address = base58.b58encode(pre_address)
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="blockchain")
    cursor = db.cursor()
    sql = 'insert into pkadress value("{}","{}")'.format(str(binascii.hexlify(public_key)),str(address.decode()))
    try:
        cursor.execute(sql)
        db.commit()
        print("123")
    except Exception as e:
        print(e)
    cursor.close()
    db.close()
    return address.decode()
#生成地址和签名之后，需要将其存入数据库中
#正常流程上来说，生成私钥，签名，地址均直接一步生成

def GenSig(sk,msg):#根据消息与私钥生成签名
    pass
def VerifySig():#检验签名的正确性.
    pass

#采用UTXO格式
def RestCoin():#返回用户余额（实在不行一个一个去搜）
    pass

def TxHistory():#返回用户交易历史（实在不行一个一个去搜）
    pass