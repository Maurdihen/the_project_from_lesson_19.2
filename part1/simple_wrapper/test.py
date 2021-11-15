import sys
from pathlib import Path
import os
import unittest
import inspect
import main
import json

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402

def func():
    test_list = ['test1', 'test2']
    return test_list

class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.func_name = 'jsonwrap'

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")

    def test_wrapper(self):
        func_result = getattr(main, self.func_name)(func)()
        self.assertTrue(
            isinstance(func_result, str),
            "%@Проверьте что в результате применения"
            " декоратора декорируемая функция возвращает строку")

        self.assertTrue(is_json(func_result),
             "%@Проверьте что значение возвращаемой функции"
             " после применения декоратора соответствует формату json"
        )


def is_json(result):
    try:
        json.loads(result)
    except ValueError as e:
        return False
    return True


if __name__ == "__main__":
    unittest.main()