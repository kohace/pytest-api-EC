import allure
import pytest

from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from base.apiutils import BaseRequests

@allure.feature('登录接口')
class TestLogin:

    @allure.story('用户名和密码正常登录校验')
    @pytest.mark.parametrize("params", get_testcase_yaml("./testcase/Login/login.yaml"))
    def test_case01(self, params):
        BaseRequests().specification_yaml(params)

    @allure.story('用户名和密码错误登录校验')
    @pytest.mark.parametrize("params", get_testcase_yaml("./testcase/Login/login.yaml"))
    def test_case01(self, params):
        BaseRequests().specification_yaml(params)

# if __name__ == '__main__':
#     pytest.main(['-vs'])