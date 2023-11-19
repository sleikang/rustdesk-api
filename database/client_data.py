from database.database import DataBase
from database.sqlite import SQLite
from database.mysql import MySQL
import threading


class ClientData(object):
    client: DataBase = None
    allotnum = None
    allotmaxnum = None
    lock = None

    def __init__(
        self,
        type: str = "SQLite",
        database: str = "",
        ip: str = "127.0.0.1",
        port: int = "3306",
        username: str = "admin",
        password: str = "password",
        allotmaxnum: int = 3,
    ):
        self.lock = threading.Lock()
        self.allotnum = 0
        self.allotmaxnum = allotmaxnum
        if type == "SQLite":
            self.client = SQLite(db=database)
        elif type == "MySQL":
            self.client = MySQL(
                database=database,
                ip=ip,
                port=port,
                username=username,
                password=password,
            )

    def query(self, sql: str, parameters=None):
        """
        查询数据库
        :param sql 语句
        :param parameters 参数
        :return True or False, data, err
        """
        self.lock.acquire()
        p = None
        data = None
        err = None
        try:
            p, data, err = self.client.query(sql=sql, parameters=parameters)
        except Exception as result:
            err = "异常错误：{}".format(result)
        self.lock.release()
        return p, data, err

    def execution(self, sql: str, parameters=None):
        """
        执行数据库
        :param sql 语句
        :param parameters 参数
        :return True or False
        """
        self.lock.acquire()
        p = None
        err = None
        try:
            p, err = self.client.execution(sql=sql, parameters=parameters)
        except Exception as result:
            err = "异常错误：{}".format(result)
        self.lock.release()
        return p, err
