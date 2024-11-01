import configparser
from conf.setting import FILE_PATH

class OperationConfig:
    def __init__(self, file_path=None):
        if file_path is None:
            self.__file_path = FILE_PATH['conf']
        else:
            self.__file_path = file_path
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__file_path, encoding='utf-8')
        except configparser.Error as e:
            print(e)

    def get_section_from_data(self, section, option):
        """
        读取ini
        :param section: 头部
        :param option: key
        :return:
        """
        try:
            data = self.conf.get(section, option)
            return data
        except configparser.Error as e:
            print(e)

    def get_envi(self, option):
        return self.get_section_from_data("api_envi",option)

    def get_mysql_config(self, option):
        return self.get_section_from_data("MYSQL", option)
if __name__ == '__main__':
    oper = OperationConfig()
    # print(oper.get_section_from_data("api_envi", "host"))
    print(oper.get_envi("host"))