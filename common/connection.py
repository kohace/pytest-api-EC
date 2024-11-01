import pymysql

from common.recordlog import logs
from conf.operationConfig import OperationConfig

conf = OperationConfig()

class ConnectMysql:
    def __init__(self):
        mysql_conf = {
            'host' : conf.get_mysql_config('host'),
            'port' : int(conf.get_mysql_config('port')),
            'user' : conf.get_mysql_config('username'),
            'password' : conf.get_mysql_config('password'),
            'database' : conf.get_mysql_config('database'),
        }

        self.conn = pymysql.connect(**mysql_conf,charset='utf8')
        print(self.conn)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        print(self.cursor)
        logs.info("""成功连接到数据库
        host: {host},
        port: {port},
        database: {database},
        """.format(**mysql_conf))

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def close(self):
        if self.conn and self.cursor:
            self.conn.close()
            self.cursor.close()

    def insert(self, sql):
        """新增"""

    def update(self, sql):
        """新增"""

    def insert(self, sql):
        """新增"""


if __name__ == '__main__':
    mq = ConnectMysql()
    sql = 'select * from students limit 5'
    print(mq.query(sql))
