import base64

# 加密
encoded_data = base64.b64encode(b"798448501@qq.com")
print(encoded_data)  # 输出: b'SGVsbG8sIFdvcmxkIQ=='

# 解密
decoded_data = base64.b64decode(b'xxxxxYmFRNDExNTP3Li4=')
print(decoded_data)  # 输出: b'Hello, World!'