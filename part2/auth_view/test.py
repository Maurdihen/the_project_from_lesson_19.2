import sys
from pathlib import Path
import os
import unittest
import main
from sqlalchemy import text
import jwt

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase             # noqa: E402
from ttools.skyprotests.tests_mixins import ResponseTestsMixin  # noqa: E402

CREATE_TABLE = ("CREATE TABLE user ("
                "id integer PRIMARY KEY, "
                "username varchar(300), "
                "password varchar(300),"
                "role varchar(300))")

INSERT_ROWS = ("INSERT INTO user"
               "('username', 'password', role) VALUES "
               "('test_user', '2747f4f326d86ec59d8cd1b527018032',"
               " 'user')")
               

class AuthTestCase(SkyproTestCase, ResponseTestsMixin):
    def setUp(self):
        self.func_name = 'auth_required'
        self.student_app = main.app.test_client()
        self.student_app_post = self.student_app.post
        self.user_data = {"username": "test_user", "password": "QWEPASSWORDQWE"}
        self.invalid_password = {"username": "test_user", "password": "bad_password"}
        self.invalid_user = {"username": "bad_user", "password": "bad_password"}
        self.url = '/auth/'
        self.method = 'POST'
        self.db = main.db
        self.secret = 's3cR$eT'
        self.algo = 'HS256'
        if self.db.session.is_active:
            self.db.session.close()
        self.db.drop_all()
        with self.db.session.begin():
            self.db.session.execute(text(CREATE_TABLE))
            self.db.session.execute(text(INSERT_ROWS))
    
    def test_client_post_get_token_with_valid_data(self):
        test_options = {
            "url": self.url,
            "method": self.method,
            "code": [201],
            "text": "при правильном пароле и имени пользователя ",
            "student_response": self.student_app_post(
                self.url,
                json=self.user_data),
            "expected": dict
        }
        response_data = self.check_status_code_jsonify_and_expected(**test_options).json
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')
        for token, implementation in zip([access_token, refresh_token], 
                         ['access_token', 'refresh_token']):
            self.assertIsNotNone(
                token,
                ("%@Проверьте, что функция возвращает словарь, который содержит"
                f" {implementation}")
            )
        self.refresh_token = refresh_token
        try:
            access_token_object = jwt.decode(access_token, self.secret, self.algo)
            refresh_token_object = jwt.decode(refresh_token, self.secret, self.algo)
        except Exception:
            raise self.failureException(
                "При декодировании ваших токенов произошла ошибка. ",
                "Проверьте, что токены генерируются корректно.")
        
        for token, implementation in zip([access_token_object, refresh_token_object], 
                                         ['access_token', 'refresh_token']):
            for key in ['username', 'role', 'exp']:
                self.assertIsNotNone(
                    token.get(key),
                    f"%@ Проверьте что в {implementation} содержится переменная {key}")
        
        # REFRESH TOKEN TESTS:
        # valid refresh_token
        test_options = {
            "url": self.url,
            "method": self.method,
            "code": [201],
            "text": "при правильном значении refresh_token",
            "student_response": self.student_app.put(
                self.url,
                json={"refresh_token": self.refresh_token}),
            "expected": dict,
        }
        self.check_status_code_jsonify_and_expected(**test_options).json
        
        # put with empty data
        test_options = {
            "url": self.url,
            "method": self.method,
            "code": [400],
            "text": "при правильном значении refresh_token",
            "student_response": self.student_app.put(
                self.url,
                json={}),
            "expected": dict,
        }
        self.check_status_code_jsonify_and_expected(**test_options).json

    def test_client_post_get_token_with_invalid_password(self):
        test_options = {
            "url": self.url,
            "method": self.method,
            "code": [401],
            "text": "при неправильном пароле и правильном имени пользователя ",
            "student_response": self.student_app_post(
                self.url,
                json=self.invalid_password),
            "expected": dict,
            "answer": {"error": "Неверные учётные данные"}
        }
        self.check_status_code_jsonify_and_expected(**test_options).json

    def test_client_post_get_token_with_invalid_password_and_username(self):
        test_options = {
            "url": self.url,
            "method": self.method,
            "code": [401],
            "text": "при неправильном пароле и правильном имени пользователя ",
            "student_response": self.student_app_post(
                self.url,
                json=self.invalid_user),
            "expected": dict,
            "answer": {"error": "Неверные учётные данные"}
        }
        self.check_status_code_jsonify_and_expected(**test_options).json



    def tearDown(self):
        self.db.session.close()
if __name__ == "__main__":
    unittest.main()