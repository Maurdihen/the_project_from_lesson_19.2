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
        self.func_name = 'auth_required'
        self.student_app = main.app.test_client()

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")

    def test_view_without_header_answers_code_401(self):
        url = '/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [401],
            "text": "при отсутствии заголовка Authorization",
            "student_response": self.student_app.get(
                url, 
                json=""),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_header_answers_code_200(self):
        url = '/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "text": "при наличии заголовка Authorization",
            "student_response": self.student_app.get(
                url, 
                json="",
                headers={"Authorization": "hello!"}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)


if __name__ == "__main__":
    unittest.main()