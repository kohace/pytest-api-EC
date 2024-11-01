import logging
import os
import time
from logging.handlers import RotatingFileHandler

from conf import setting

logpath = setting.FILE_PATH['LOG']
if not os.path.exists(logpath):
    os.mkdir(logpath)

logfile_name = logpath + r'\test.{}.log'.format(time.strftime("%Y%m%d-%H%M%S"))

class RecordLog:
    """封装日志"""

    def output_logging(self):
        """"""
        logger = logging.getLogger(__name__)

        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s'
            )

            fh = RotatingFileHandler(filename=logfile_name,mode='a', maxBytes=10 * 1024 * 1024, backupCount=7,encoding='utf-8')
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)

            logger.addHandler(fh)

            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)
        return logger

apilog = RecordLog()
logs = apilog.output_logging()