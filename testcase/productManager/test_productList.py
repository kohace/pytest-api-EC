import allure
import pytest

from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from base.apiutils import BaseRequests

@allure.feature('商品列表')
class TestProductList:

    @allure.story('获取商品列表接口')
    @pytest.mark.parametrize("params", get_testcase_yaml("./testcase/productManager/getProductList.yaml"))
    def test_get_product_list(self, params):
        BaseRequests().specification_yaml(params)