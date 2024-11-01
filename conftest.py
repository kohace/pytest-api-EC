import warnings
from common.recordlog import logs
from common.readyaml import ReadYamlData

import pytest

read = ReadYamlData()

@pytest.fixture(scope='session',autouse=True)
def clear_extract_data():
    read.clear_yaml_data()


@pytest.fixture(scope='session',autouse=True)
def fixture_test(request):
    logs.info("——————接口测试开始——————")
    yield
    logs.info("——————接口测试结束——————")

# @pytest.fixture(scope='session',autouse=True)
# def clear_extract(request):
#     # 禁用HTTPS ResourceWarning
#     warnings.simplefilter(action='ignore', category=FutureWarning)
#     yfd.clear_yaml_data()
#     remove_file()
#     print("——————接口测试开始——————")
#     yield
#     print("——————接口测试结束——————")