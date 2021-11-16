# У Вас имеется шаблон Flask приложения с настроенной БД
# и неймспейсом "auth"
# Вам необходимо добавить в неймспейс auth
# Class Based View, которая решает следующие задачи:
# 1. При POST-запросе на адрес /auth/ возвращается словарь с access_token и refresh token.
# Запрос должен содержать следующие сведения:
# {
#    "username": "test_user",
#    "password": "password"
# }
#     1.1 Если такой пользователь отсутствует в базе данные 
#         или пароль неверный возвращайте ответ:
#         {"error": "Неверные учётные данные"}    с кодом 401
#    
#     1.2 Если в теле запроса пост отсутствую поля
#          username или password возвращайте ответ с кодом 400
#
# 2. При PUT запросе на адрес /auth/ возвращается словарь с access_token и refresh token.
# запрос должен содержать refresh token
# {
#    "refresh_token": "refresh_token"
# }
#    2.1 Если refresh_token отсутствует в запросе возвращать код 400
#
# 3. Проверьте, что ваши access и refresh  токены содержат username и role
#    пользователя, а также время действия токена 'exp'
#
# Для самопроверки мы добавили в базу данных запись о пользователе у которого
# пароль хранится в виде хэша, закодированного по алгоритму md5
#
# +----+----------+----------------------------------+-------+
# | id | username |             password             |  role |
# +----+----------+----------------------------------+-------+
# | 1  | SkyUser  | e5a9a38d52002ca74792b474d152bede | admin |
# +----+----------+----------------------------------+-------+
# *пароль в обычном виде: eGGPtRKS5
#
#
from flask import Flask
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
api = Api(app)
auth_ns = api.namespace('auth')

secret = 's3cR$eT'
algo = 'HS256'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

db.create_all()

u1 = User(id=1, username='SkyUser', password='e5a9a38d52002ca74792b474d152bede', role='admin')

with db.session.begin():
    db.session.add(u1)

@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        # TODO напишите Ваш код здесь
        pass

    def put(self):
        # TODO напишите Ваш код здесь
        pass

if __name__ == '__main__':
    app.run(debug=False)
