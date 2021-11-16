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
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402

class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.func_name = 'check_token'

    def test_module_has_function(self):
        self.assertTrue(
            hasattr(main, self.func_name),
            f"%@Проверьте, что функция {self.func_name} определена в модуле"
        )

        self.assertTrue(
            inspect.isfunction(getattr(main, self.func_name)),
            f"%@Проверьте что объект {self.func_name} является функцией")

    def test_decode_token(self):
        token = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                 'eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.'
                 'fMPkh9GNQMlLRxO0PmvCjUPPwX0t4CM5Wk4ATt35mNY')
        invalid_token = 'InvalidQWETOKEN'
        secret = 's3cR$eT'
        algo = 'HS256'
        self.assertTrue(
            isinstance(token, str),
            "%@Проверьте что в результате применения"
            " декоратора декорируемая функция возвращает строку")
        data = main.check_token(token, secret, algo)
        author_data = solution.check_token(token, secret, algo)
        invalid_data = main.check_token(invalid_token, secret, algo)

        self.assertTrue(
            data==author_data,
            "%@Проверьте что Ваша функция возвращает декодированную информацию "
            "при получении правильного токена"
        )

        self.assertFalse(
            invalid_data,
            "%@Проверьте что при получении неправильного токена возвращается False "
        )

if __name__ == "__main__":
    unittest.main()