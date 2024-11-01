import json
from urllib import request

import yaml
import os


# from senderqeuest import SendRequest
from conf.setting import FILE_PATH


def get_testcase_yaml(file):
    try:
        with open(file, 'r', encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(e)

class ReadYamlData:
    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_data = get_testcase_yaml(yaml_file)
        else:
            self.yaml_data = 'getProductList.yaml'

    def write_yaml_data(self, value):
        """
        写入数据到yaml文件中
        :param value:
        :return:
        """
        file_path = FILE_PATH['extract']
        if os.path.exists(file_path):
            os.system(file_path)
        try:
            file = open(file_path, 'a', encoding="utf-8")
            if isinstance(value, dict):
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
        except Exception as e:
            print(e)
        finally:
            file.close()

    def read_extract_yaml(self, node_name, sec_node_name=None):
        file_path = FILE_PATH['extract']
        if os.path.exists(file_path):
            pass
        else:
            print(file_path+" 文件不存在")

            # file = open(file_path, 'w', encoding="utf-8")
            # file.close()
            # print("创建成功")

        try:
            with open(file_path, 'r', encoding="utf-8") as rf:
                extract_data = yaml.safe_load(rf)
                if sec_node_name is None:
                    return extract_data[node_name]
                else:
                    return extract_data[node_name][sec_node_name]
        except Exception as e:
            print(e)

    def clear_yaml_data(self):
        with open(FILE_PATH['extract'], 'w', encoding="utf-8") as rf:
            rf.truncate()



if __name__ == '__main__':
    res = get_testcase_yaml('../testcase/Login/login.yaml')[0]
    url = "http://127.0.0.1:8787" + res['baseInfo']['url']
    data = res['testCase'][0]['data']
    method = res['baseInfo']['method']
    print(url)

    send = SendRequest()
    resquest = send.run_main(method=method, url=url, data=data, header=None)
    print(resquest)

    token = resquest.get('token')
    write_data = {}
    write_data['Token'] = token

    ryd = ReadYamlData()
    # ryd.write_yaml_data(write_data)
    #
    # json_str = json.dumps(res)

    # print(json_str)

    ex = ryd.read_extract_yaml('token')
    print(ex)