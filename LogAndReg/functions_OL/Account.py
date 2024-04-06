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

# 这里的函数是用于私钥生成，公钥生成，生成签名，与验证签名
def GenSk():  # 生成私钥
    PrivateKey = os.urandom(32)
    return PrivateKey


def GenPk(PrivateKey):  # 基于私钥生成公钥，然后生成地址？这里输入的私钥是二进制字节串
    Publick_Key = ecdsa.SigningKey.from_string(
        PrivateKey, curve=ecdsa.SECP256k1).verifying_key.to_string()
    return Publick_Key


# 公钥用于签名的验证，地址用来实现转账
def AdCre(private_key,id):  # 生成账户地址，并将公钥与地址存入数据库当中
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
    sql = 'insert into pkadress(pk,adress,id,amount) value("{}","{}","{}",100)'.format(binascii.hexlify(public_key).decode(), address.decode(),id)
    print(len(binascii.hexlify(public_key)))
    print(len(address.decode()))
    print(type(address.decode()))
    try:
        cursor.execute(sql)
        db.commit()
    except:
        cursor.close()
        db.close()
        raise Exception("账号重复")
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
    return binascii.hexlify(signature).decode()#这里生成的签名是字符串格式


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

sk = binascii.unhexlify("4b6dd2a438a8e5091b9c5b325ef9e365183abdb9d4d7d98230ddd781dad4d495")
pk = binascii.unhexlify("0cf1aa39a65f40092efdc1a5b86fc52cf09cbcd3b7ddbcdc2fe9572862aac33794d6c22d3f971f9fa6310e8ebb5641190a3521688db314a6ffba6f96012c7887")
print(pk)
pk = b'\x0c\xf1\xaa9\xa6_@\t.\xfd\xc1\xa5\xb8o\xc5,\xf0\x9c\xbc\xd3\xb7\xdd\xbc\xdc/\xe9W(b\xaa\xc37\x94\xd6\xc2-?\x97\x1f\x9f\xa61\x0e\x8e\xbbVA\x19\n5!h\x8d\xb3\x14\xa6\xff\xbao\x96\x01,x\x87'
data={'inputs':{'sender_adress':'1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn','tx_nonce': 1}, 'outputs': {'amount': 0, 'recipient': '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 'Fees': 0}}

sig="79985cfc2359c089ab05044a4fa575f76b68a80a45371a3fbba4540736875099929b412f1bb28ce1255542f268b4a8f8cb06b168a368b86057da762b438af239"
print(VerifySig(pk,str(data),sig))
print(type(pk))
print(type(sig))