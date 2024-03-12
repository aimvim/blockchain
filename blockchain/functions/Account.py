import binascii
import hashlib
import os
import base58
import ecdsa
import pymysql
from Crypto.Hash import MD5
from Crypto.Signature import pkcs1_15
from ecdsa import SigningKey, SECP256k1, VerifyingKey
from Crypto.PublicKey import RSA


def GenSk():  # 生成私钥
    PrivateKey = os.urandom(32)
    return PrivateKey


def GenPk(PrivateKey):  # 基于私钥生成公钥，然后生成地址？
    Publick_Key = ecdsa.SigningKey.from_string(
        PrivateKey, curve=ecdsa.SECP256k1).verifying_key.to_string()
    return Publick_Key


# 公钥用于签名的验证，地址用来实现转账
def AdCre(private_key):  # 生成账户地址，并将公钥与地址存入数据库当中
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
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="blockchain")
    cursor = db.cursor()
    sql = 'insert into pkadress value("{}","{}")'.format(binascii.hexlify(public_key).decode(), address.decode())
    print(len(binascii.hexlify(public_key)))
    print(len(address.decode()))
    print(type(address.decode()))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
    cursor.close()
    db.close()
    return address.decode()


# 生成地址和签名之后，需要将其存入数据库中
# 正常流程上来说，生成私钥，签名，地址均直接一步生成

def GenSig(sk, msg):
    # 注意：这里的sk是字节串格式，在调用的时候需要记得转化——使用函数binascii.unhexlify
    # 将消息转换为字节串
    msg_bytes = msg.encode()
    # 创建签名密钥对象
    sk_obj = SigningKey.from_string(sk, curve=SECP256k1)
    # 生成签名
    signature = sk_obj.sign(msg_bytes)
    # 返回签名的十六进制表示
    return binascii.hexlify(signature).decode()


def VerifySig(pk, msg, signature):
    # 注意：这里的pk是二进制字节串格式，在调用的时候需要记得转化——使用函数binascii.unhexlify
    # 将消息和签名转换为字节串
    msg_bytes = msg.encode()
    signature_bytes = binascii.unhexlify(signature)
    # 创建验证密钥对象
    vk_obj = VerifyingKey.from_string(pk, curve=SECP256k1)
    try:
        # 尝试验证签名
        vk_obj.verify(signature_bytes, msg_bytes)
        return True  # 验证成功
    except ecdsa.BadSignatureError:
        return False  # 验证失败


# 采用UTXO格式
def RestCoin():  # 返回用户余额（实在不行一个一个去搜）
    pass


def TxHistory():  # 返回用户交易历史（实在不行一个一个去搜）
    pass

sk = binascii.unhexlify("942e520e28e2af56c7f9cf79fe9f082e807ee4a75a8cdb0bb9a08303011eaf35")
pk = binascii.unhexlify("9ec11f8949f458d0ac8c32bd542b76451be1014d0e3c1264737d20a109aae3bb23ec19575e619bae0a7918e10b967717fde63a8f67186b2eca056937e4e536d0")
signature = GenSig(sk, "123")
print(signature)
print(VerifySig(pk,"12", signature))