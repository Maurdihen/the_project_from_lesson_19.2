# Написать функцию `generate_jwt` которая 
# генерирует access_token и refresh_token.
# В качестве аргумента функция должна принимать словарь вида user_obj
# В access и в refresh токене должна содержаться информация об:
# 1. имени пользователя ('username')
# 2. роли ('role')
# 3. времени действия токена ('exp')
# Время действия access токена должно составлять 30 с момента получения
# Время действия refresh токена - 130 дней c момента получения


import datetime
import calendar
import jwt
    
algo = 'HS256'
secret = 's3cR$eT'

user_obj = {
    "username": 'test_user',
    "role": 'admin'
}

def generate_jwt(user_obj):
    data = {
        "username": user_obj.get('username'),
        "role": user_obj.get('role')
    }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algorithm=algo)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, secret, algorithm=algo)
    return {"access_token": access_token, "refresh_token": refresh_token}

if __name__=='__main__':
    generate_jwt(user_obj)