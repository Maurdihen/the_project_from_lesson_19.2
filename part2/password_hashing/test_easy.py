import sys
from pathlib import Path
import os
import unittest
import inspect
import main
import solution

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase             # noqa: E402


class PasswordTestCase(SkyproTestCase):
    def setUp(self):
        self.func_name = 'easy'

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")
    
    def test_easy_returns_not_none(self):
        func = getattr(main, self.func_name)
        author_func = getattr(solution, self.func_name)
        self.assertIsNotNone(
            func('HardPassword'),
            "%@Проверьте что функция не возвращает None"
        )

        self.assertTrue(
            func('HardPassword')==author_func('HardPassword'),
           "%@Проверьте что в функции используется алгоритм md5")

if __name__ == "__main__":
    unittest.main()