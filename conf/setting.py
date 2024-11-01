import os
import sys
import logging

DIR_PATH = os.path .dirname(os.path.dirname(__file__))
sys.path.append(DIR_PATH)

# log日志输出
LOG_LEVEL = logging.DEBUG #输出日志到文件
STREAM_LOG_LEVEL = logging.INFO #输出日志到控制台

# 文件路径
FILE_PATH = {
    'extract' : os.path.join(DIR_PATH, 'extract.yaml'),
    'conf' : os.path.join(DIR_PATH, 'conf', 'config.ini'),
    'LOG' : os.path.join(DIR_PATH, 'log'),
}

print(FILE_PATH['extract'] + '文件路径')
print(FILE_PATH['conf'])

