import os
import shutil
import pytest

if __name__ == '__main__':
    pytest.main()
    shutil.copy('./environment.xml', './report/temp')
    os.system(f'allure serve ./report/temp')
    # pytest.main(['-vs', './testcase', '-m', 'maoyan'])
