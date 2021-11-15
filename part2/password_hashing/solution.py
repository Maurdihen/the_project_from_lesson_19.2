# Просто: Напишите функцию `easy` которая 
# получает пароль в открытом виде и 
# возвращает хеш с использованием алгоритма md5
#
# Сложно: Напишите функцию `hard` которая 
# получает пароль в открытом виде и соль 
# и возвращает хеш с использованием алгоритма sha256
import hashlib

def easy(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def hard(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        1000
    )
