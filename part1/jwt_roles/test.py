import sys
from pathlib import Path
import os
import unittest
import inspect
import main

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase             # noqa: E402
from ttools.skyprotests.tests_mixins import ResponseTestsMixin  # noqa: E402


class DecorTestCase(SkyproTestCase, ResponseTestsMixin):
    def setUp(self):
        self.func_name = 'admin_required'
        self.student_app = main.app.test_client()
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.fMPkh9GNQMlLRxO0PmvCjUPPwX0t4CM5Wk4ATt35mNY"
        self.invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.IMKkztrqfADs5-uIvC8h29FWHMjccmlWqTOBf-oIYpY"
        self.user_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJ1c2VyIn0.4bcM79bPHZN4trdBB4qNt_BX8239ynV97TV-3k-GGfk"

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")

    def test_get_without_header_answers_code_200(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "text": "при отсутствии заголовка Authorization",
            "student_response": self.student_app.get(
                url, 
                json=""),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_get_with_header_answers_code_200(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "text": "при наличии заголовка Authorization",
            "student_response": self.student_app.get(
                url, 
                json="",
                headers={"Authorization": ""}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_get_with_token_answers_code_200(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "text": "при наличии заголовка Authorization с правильным токеном",
            "student_response": self.student_app.get(
                url, 
                json="",
                headers={"Authorization": f"Bearer {self.token}"}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_post_without_header_answers_code_401(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [401],
            "text": "при отсутствии заголовка Authorization",
            "student_response": self.student_app.post(
                url, 
                json=""),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_post_with_header_answers_code_401(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [401],
            "text": "при наличии заголовка Authorization без токена",
            "student_response": self.student_app.post(
                url, 
                json="",
                headers={"Authorization": ""}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_post_with_admin_token_answers_code_201(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [201],
            "text": "при наличии заголовка Authorization с правильным токеном и ролью admin",
            "student_response": self.student_app.post(
                url, 
                json="",
                headers={"Authorization": f"Bearer {self.token}"}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_post_with_admin_token_answers_code_201(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [201],
            "text": "при наличии заголовка Authorization с правильным токеном и ролью admin",
            "student_response": self.student_app.post(
                url, 
                json="",
                headers={"Authorization": f"Bearer {self.token}"}),
        }
        x = self.check_status_code_jsonify_and_expected(**test_options)


    def test_post_with_user_token_answers_code_201(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [403],
            "text": "при наличии заголовка Authorization с правильным токеном и ролью user",
            "student_response": self.student_app.post(
                url, 
                json="",
                headers={"Authorization": f"Bearer {self.user_token}"}),
        }
        x = self.check_status_code_jsonify_and_expected(**test_options)
        pass

    def test_post_with_invalid_token_answers_code_401(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [401],
            "text": "при наличии заголовка Authorization с неправильным токеном",
            "student_response": self.student_app.post(
                url, 
                json="",
                headers={"Authorization": f"Bearer {self.invalid_token}"}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)


if __name__ == "__main__":
    unittest.main()