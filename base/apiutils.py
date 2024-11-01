import json
import re
import jsonpath
import allure

from common.debugtalk import DebugTalk
from common.readyaml import ReadYamlData, get_testcase_yaml
from common.recordlog import logs
from conf.operationConfig import OperationConfig
from common.senderqeuest import SendRequest
from common.assertions import  Assertions

assert_res = Assertions()

class BaseRequests:
    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequest()

    def replace_load(self, data):
        """yaml数据替换解析"""
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)
            # print('从yaml文件获取的原始数据：', str_data)
        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                # ref_all_params = str_data[start_index:end_index + 1]
                # # 取出yaml文件的函数名
                # func_name = ref_all_params[2:ref_all_params.index("(")]
                # # 取出函数里面的参数
                # func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]
                # # 传入替换的参数获取对应的值,类的反射----getattr,setattr,del....
                # extract_data = getattr(DebugTalk(), func_name)(*func_params.split(',') if func_params else "")
                #
                # if extract_data and isinstance(extract_data, list):
                #     extract_data = ','.join(e for e in extract_data)
                # str_data = str_data.replace(ref_all_params, str(extract_data))
                # print('通过解析后替换的数据：', str_data)

        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self, case_info):
        # case_info = case_info[0]
        cookie = None
        print("case_info-----------", case_info)
        params_type = ['params', 'data', json]
        base_url = self.conf.get_envi('host')
        url = base_url + case_info['baseInfo']['url']
        allure.attach(url, f'接口地址:{url}')
        api_name = case_info['baseInfo']['api_name']
        method = case_info['baseInfo']['method']
        header = case_info['baseInfo']['header']
        try:
            cookie = self.replace_load(case_info['baseInfo']['cookies'])
        except Exception as e:
            pass

        for tc in case_info['testCase']:
            case_name = tc.pop('case_name')

            # data = tc.pop('data')
            validation = tc.pop('validation')
            extract = tc.pop('extract',None)
            # print(case_name)
            extract_list = tc.pop('extract_list', None)
            for k, v in tc.items():
                if k in params_type:
                    tc[k] = self.replace_load(v)
            print(tc)
            res = self.send.run_main(name=api_name,url=url,case_name=case_name, header=header,method=method, cookies=cookie, **tc)
            allure.attach(res.text, f'接口的响应信息为:{res.text}', allure.attachment_type.TEXT)
            res_json = json.loads(res.text)  # 把json格式转换成字典字典
            if extract is not None:
                self.extract_data(extract, res.text)
            if extract_list is not None:
                self.extract_data_list(extract_list, res.text)

            # 处理接口断言
            assert_res.assert_result(validation, res_json, res.status_code)

    def extract_data(self, testcase_extarct, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extarct: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extarct.items():

                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_yaml_data(extract_data)
                # 处理json提取参数
                if '$' in value:
                    print(value)
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    print(ext_json)

                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extarct_data)
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml_data(extarct_data)
        except Exception as e:
            logs.error(e)


    def extract_data_list(self, testcase_extarct, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extarct: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extarct.items():

                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_yaml_data(extract_data)
                # 处理json提取参数
                if '$' in value:
                    print(value)
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    print(ext_json)

                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extarct_data)
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml_data(extarct_data)
        except Exception as e:
            logs.error(e)


if __name__ == '__main__':
    data = get_testcase_yaml('../testcase/productManager/getProductList.yaml')
    # print(data)
    base = BaseRequests()
    print(base.specification_yaml(data[0]))
    # base.replace_load(data)