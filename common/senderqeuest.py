import json

import allure
import pytest
import requests

from common.recordlog import logs
from requests import utils
from common.readyaml import ReadYamlData

class SendRequest(object):
    """
    封装接口
    """

    def __init__(self):
        self.read = ReadYamlData()

    # def get(self, url, data, header = None):
    #     res = requests.get(url,data, headers=header, verify=False)
    #     return res.json()
    #
    # def post(self, url, data, header = None):
    #     res = requests.post(url, data, headers=header, verify=False)
    #     return res.json()
    #
    # def put(self, url, data, header = None):
    #     res = requests.put(url,data, headers=header, verify=False)
    #     return res.json()
    #
    # def delete(self, url, data, header = None):
    #     res = requests.delete(url,data, headers=header, verify=False)
    #     return res.json()

    def send_request(self, **kwargs):
        logs.info(kwargs)
        cookie = {}
        session = requests.Session()
        try:
            result = session.request(**kwargs)
            set_cookies = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookies:
                cookie['Cookie'] = set_cookies
                self.read.write_yaml_data(set_cookies)
                logs.info(f'cookie:{cookie}')
            logs.info(f'接口的实际返回信息:{str(result.text)}')
        except Exception as e:
            logs.error(e)
            pytest.fail('接口请求异常')
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, files=None, **kwargs):
        """
        :param url:
        :param data:
        :param header:
        :param method:
        :return:
        """
        try:
            logs.info(f'接口名称:{name}')
            logs.info(f'接口请求地址:{url}')
            logs.info(f'接口请求方式:{method}')
            logs.info(f'测试用例名称:{case_name}')
            logs.info(f'请求头:{header}')
            logs.info(f'Cookies:{cookies}')
            req_params = json.dumps(kwargs, ensure_ascii=False)
            logs.info(f'111---:{req_params}')
            if "data" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "json" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "params" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)
        response = self.send_request(method=method, url=url, headers=header, cookies=cookies, files=files, verify=False, **kwargs)

        # res = {}
        # if method.upper() == 'GET':
        #     res = self.get(url, data, header)
        # elif method.upper() == 'POST':
        #     res = self.post(url, data, header)
        # elif method.upper() == 'PUT':
        #     res = self.put(url, data, header)
        # elif method.upper() == 'DELETE':
        #     res = self.delete(url, data, header)
        # else:
        #     print("参数错误")
        return response


if __name__ == '__main__':
    url = 'http://127.0.0.1:8787/dar/user/login'
    data = {
        "user_name": "test01",
        "passwd": "admin123",
    }
    header = None

    send = SendRequest()
    res = send.run_main(url, data, header=header, method="post")
    # res = send.post(url, data, header)
    print(res)
