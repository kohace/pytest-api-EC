import os.path
import allure
import jsonpath
import operator
from numpy.random.mtrand import operator

from common.recordlog import logs


class Assertions:
    def contains_assert(self, value, response, status_code):
        flag = 0
        for assert_key, assert_value in value.items():
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f'预期结果:{assert_value}\n实际结果:{status_code}','响应代码断言结果：失败')
                    logs.error('contanins断言失败, 接口返回码【%S】 不等于 【%s】' % (status_code, assert_value))
            else:
                resp_list = jsonpath.jsonpath(response, '$..%s' % assert_key)
                print(resp_list)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    if assert_value in resp_list:
                        print('断言成功')
                        logs.info('断言成功, 预期：【%s】 ，实际： 【%s】' % (assert_value, resp_list))

                    else:
                        flag += 1
                        allure.attach(f'预期结果:{assert_value}\n实际结果:{status_code}', '响应为本断言结果：失败')
                        logs.error('断言失败, 预期：【%s】 ，实际： 【%s】' % (assert_value, resp_list))
            return flag

    def equals_assert(self,value, response):
        return self.all_equals_assert(value,response, True)

    def not_equals_assert(self,value, response):
        """相等断言"""
        return self.all_equals_assert(value,response, False)

    def all_equals_assert(self, value, response,is_eq):
        flag = 0
        """相等断言"""
        res_lst = []
        if isinstance(value,dict) and isinstance(response,dict):
            for res in response:
                if list(value.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del response[rl]
            if is_eq:
                eq_assert = operator.eq(response,value)
                if eq_assert:
                    logs.info(f'相等断言成功，接口实际返回值:{response}, 等于预期结果:{str(value)}')
                else:
                    flag += 1
                    logs.error(f'相等断言失败，接口实际返回值:{response}, 不等于预期结果:{str(value)}')
            else:
                eq_assert = operator.ne(response,value)
                if eq_assert:
                    logs.info(f'不相等断言成功，接口实际返回值:{response}, 等于预期结果:{str(value)}')
                    flag += 1
                else:
                    logs.error(f'不相等断言失败，接口实际返回值:{response}, 不等于预期结果:{str(value)}')

        else:
            raise TypeError('error，必须为字典类型！')
        return flag

    def assert_result(self, expected, response, status_code):
        """"""
        try:
            all_flag = 0
            for yq in expected:
                for k, v in yq.items():
                    if k == 'contains':
                        flag = self.contains_assert(v, response, status_code)
                        all_flag += flag
                    elif k == 'eq':
                        self.equals_assert(value, response)
                        all_flag += flag
            assert all_flag == 0
            logs.info('测试成功')
        except Exception as e:
            logs.error('测试失败！')
            logs.error(f'异常信息{e}')
            assert all_flag == 0

if __name__ == '__main__':
    from common.readyaml import get_testcase_yaml
    data = get_testcase_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), r'testcase\Login', 'login.yaml'))[0]
    print(data)
    value = data['testCase'][0]['validation']
    # response = data['testCase'][0]['response']
    response = {
        'error_code':None,
        'msg':'登录成功',
        'msg_code':200,
        'token':'666666666666'
    }

    ass = Assertions()
    for i in value:
        for k,v in i.items():
            ass.not_equals_assert(v,response)