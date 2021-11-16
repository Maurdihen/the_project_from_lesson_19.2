# Просто: Напишите функцию, которая получает пароль 
# в открытом виде и хеш, берет хеш от пароля 
# в открытом виде и сравнивает хеши
#
# Сложно: Напишите функцию, которая получает пароль 
# в открытом виде, хеш, соль и алгоритм хеширования, 
# берет хеш от пароля в открытом виде и сравнивает хеши

import hashlib
import hmac

def easy(pwd_hash, other_password):
    new_password_hash = hashlib.md5(other_password.encode('utf-8')).hexdigest()
    return new_password_hash == pwd_hash

PWD_HASH_ITERATIONS = 1000
def hard(password_hash, other_password, salt, algo):
    return hmac.compare_digest(
        password_hash,
        hashlib.pbkdf2_hmac(algo, other_password.encode(), salt, PWD_HASH_ITERATIONS)
    )
