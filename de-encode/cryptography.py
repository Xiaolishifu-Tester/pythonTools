from cryptography.fernet import Fernet
# from cryptography.fernet import Feet

# 生成一个密钥
key = Fernet.generate_key()
print(key)  # 输出: b'p5nU4CZ2Dm64Zx-DB_gFYR7S6Yw2g1-HgDmw2grJ03E='

# 创建一个Fernet对象
f = Fernet(key)

# 加密
data = b"Hello, World!"
encrypted_data = f.encrypt(data)
print(
    encrypted_data)  # 输出: b'gAAAAABb4JpKZMZXvRDjZQ1qkBQWVvwzdfNnZUFZLZJO-9z4ZNy_jrUYnRNYBQW-QXJbX_kXRkp1mz4j2YEIHWQ=='

# 解密
decrypted_data = f.decrypt(encrypted_data)
print(decrypted_data)  # 输出: b'Hello, World!'