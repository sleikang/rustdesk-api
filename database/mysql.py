import pymysql
from database.database import DataBase
import threading


class MySQL(DataBase):
    sqlconnect = None
    lock = None
    err = None

    def __init__(
        self,
        database: str = "",
        ip: str = "127.0.0.1",
        port: int = "3306",
        username: str = "admin",
        password: str = "password",
    ) -> None:
        try:
            self.lock = threading.Lock()
            self.sqlconnect = pymysql.connect(
                host=ip, port=port, user=username, password=password, database=database
            )
        except Exception as reuslt:
            self.err = "数据库异常错误, {}".format(reuslt)

    def query(self, sql: str, parameters=None):
        """
        查询数据库
        :param sql 语句
        :param parameters 参数
        :return True or False, data, err
        """
        self.lock.acquire()
        done = False
        data = None
        try:
            cursor = self.sqlconnect.cursor()
            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)
            data = cursor.fetchall()
            done = True
            if len(data):
                column_names = [description[0] for description in cursor.description]
                result_data = [dict(zip(column_names, row)) for row in data]
                data = result_data
        except Exception as reuslt:
            self.err = "数据库异常错误, {}".format(reuslt)
        self.lock.release()
        return done, data, self.err

    def execution(self, sql: str, parameters=None):
        """
        执行数据库
        :param sql 语句
        :param parameters 参数
        :return True or False, err
        """
        self.lock.acquire()
        done = False
        try:
            cursor = self.sqlconnect.cursor()
            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)
            self.sqlconnect.commit()
            done = True
        except Exception as reuslt:
            self.err = "数据库异常错误, {}".format(reuslt)
        self.lock.release()
        return done, self.err
