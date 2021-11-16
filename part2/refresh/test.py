import sys
from pathlib import Path
import os
import unittest
import inspect
import main
import solution
import jwt

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase             # noqa: E402


class PasswordTestCase(SkyproTestCase):
    def setUp(self):
        self.func_name = 'generate_jwt'
        self.data = {
            'username': 'testUser',
            'role': 'test_role'
        }
        self.algo = 'HS256'
        self.secret = 's3cR$eT'

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")
    
    def test_tokens(self):
        func = getattr(main, self.func_name)
        author_func = getattr(solution, self.func_name)
        self.assertIsNotNone(
            func(self.data),
            "%@Проверьте что функция не возвращает None"
        )
        self.assertTrue(
            isinstance(func(self.data), dict),
            "%@Проверьте что функция возвращает словарь"
        )
        result = func(self.data)
        access_token = result.get('access_token')
        refresh_token = result.get('refresh_token')
        for token, implementation in zip([access_token, refresh_token], 
                         ['access_token', 'refresh_token']):
            self.assertIsNotNone(
                token,
                ("%@Проверьте, что функция возвращает словарь, который содержит"
                f" {implementation}")
            )
        
        try:
            access_token_object = jwt.decode(access_token, self.secret, self.algo)
            refresh_token_object = jwt.decode(refresh_token, self.secret, self.algo)
        except Exception:
            raise self.failureException(
                "При декодировании ваших токенов произошла ошибка",
                "Проверьте при создании токена вы используете условия, обозначенные в задании")
        
        for token, implementation in zip([access_token_object, refresh_token_object], 
                                         ['access_token', 'refresh_token']):
            for key in ['username', 'role', 'exp']:
                self.assertIsNotNone(
                    token.get(key),
                    f"%@ Проверьте что в {implementation} содержится переменная {key}")
        


if __name__ == "__main__":
    unittest.main()
