import sys
from pathlib import Path
import os
import unittest
import main
import solution

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase, StdoutCapturing  # noqa: E402

class JwtTestCase(SkyproTestCase):
    def setUp(self):
        self.var_name = 'access_token'
        self.secret = 's3cR$eT'
        self.algo = 'HS256'
        self.data = {
                "username": "Skypro",
                "role": "admin"
        }

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.var_name),
            f"%@Проверьте, что переменная {self.var_name} определена в модуле"
        )
        student_token = getattr(main, 'access_token')
        
        self.assertTrue(
            student_token==solution.access_token,
            "%@Проверьте, что значение токена соответствуют ожидаемому. "
            "Возможно неправильно определён ключ или алгоритм формирования токена")

if __name__ == "__main__":
    unittest.main()