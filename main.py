import hashlib

CryptPassword = hashlib.sha256("2423124917".encode("utf8")).hexdigest()
print(CryptPassword)

x= {"s":1,"ss":2}
x.update({"l":1})
print(x)