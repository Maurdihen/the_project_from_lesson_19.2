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
from ttools.skyprotests.tests import SkyproTestCase, StdoutCapturing  # noqa: E402

def func():
    print('работаю')

class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.func_name = 'off'

    def test_module_has_function_called(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")

    def test_called_works_correct(self):
        with StdoutCapturing() as func_output:
            main.off(func)()
        
        self.assertEqual(
            len(func_output), 1, 
            "%@ Проверьте что Ваша функция-декоратор код выводит что-либо в терминал"
        )

        self.assertEqual(
            func_output[0], 'функция отключена',
            "%@Проверьте что Ваша функция-декоратор выводит"
            " правильный ответ"
        )

        self.assertNotIn(
            "работаю", func_output,
            "%@Проверьте, что декоратор отключает функцию"
        )


if __name__ == "__main__":
    unittest.main()