import binascii

hex_str = "48656c6c6f"  # 示例十六进制字符串，对应文本 "Hello"
bytes_str = binascii.unhexlify(hex_str)
print(type(bytes_str))
print(bytes_str)  # 输出: b'Hello'
