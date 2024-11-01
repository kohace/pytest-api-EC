import random

from common.readyaml import ReadYamlData

class DebugTalk:
    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_list(self, node_name, randoms=None):
        data = self.get_extract_data(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: 1,
                0: random.choice(data),
                -1 : ','.join(data)
            }
            data = data_value[randoms]
        return data



    def get_extract_order_data(self, data, randoms):
        if randoms not in[0,-1,-2]:
            return data[randoms-1]

    def get_extract_data(self, node_name, randoms=None):
        """
        获取数据中的key
        :param node_name:
        :param random: 随机
        :return:
        """
        data = self.read.read_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),
                -1 : ','.join(data),
                -2 : ','.join(data).split(',')
            }
            data = data_value[randoms]
        return data

    def md5_params(self, params):
        """

        :param params:
        :return:
        """

if __name__ == '__main__':
    debugtalk = DebugTalk()
    print(debugtalk.get_extract_data('product_id', '0'))