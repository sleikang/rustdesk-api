from database.client_data import ClientData
import threading


class CommSql:
    maxnumconnect = None
    maxnumcache = None
    clientlist = None
    lock = None

    def __init__(
        self,
        type: str = "SQLite",
        database: str = "",
        ip: str = "127.0.0.1",
        port: int = "3306",
        username: str = "admin",
        password: str = "password",
        maxnumconnect: int = 1,
        maxnumcache: int = 5,
    ) -> None:
        """
        构造函数
        :param maxnumconnect 最大连接数
        :param maxnumcache 最大缓存数
        """
        self.lock = threading.Lock()
        self.maxnumcache = maxnumcache
        self.maxnumconnect = maxnumconnect
        self.clientlist = []
        if self.maxnumcache < 0:
            self.maxnumcache = 1
        if self.maxnumconnect < 0:
            self.maxnumconnect = 1
        for i in range(self.maxnumconnect):
            self.clientlist.append(
                ClientData(
                    type=type,
                    database=database,
                    ip=ip,
                    port=port,
                    username=username,
                    password=password,
                    allotmaxnum=self.maxnumcache,
                )
            )

    def query(self, sql: str, parameters=None):
        """
        查询数据库
        :param sql 语句
        :param parameters 参数
        :return True or False, data, err
        """
        p = None
        data = None
        ret, num, err = self.__getclient__()
        if ret:
            p, data, err = self.clientlist[num].query(sql=sql, parameters=parameters)
            self.__releasecache__(num=num)
        return p, data, err

    def execution(self, sql: str, parameters=None):
        """
        执行数据库
        :param sql 语句
        :param parameters 参数
        :return True or False
        """
        p = None
        ret, num, err = self.__getclient__()
        if ret:
            p, err = self.clientlist[num].execution(sql=sql, parameters=parameters)
            self.__releasecache__(num=num)
        return p, err

    def __getclient__(self):
        """
        获取客户端
        :return True, num, err 成功返回True, 编号, None 失败返回False, None, 错误
        """
        # 优先空闲连接
        with self.lock:
            for i in range(len(self.clientlist)):
                if (
                    self.clientlist[i].allotnum < self.clientlist[i].allotmaxnum
                    and self.clientlist[i].allotnum == 0
                ):
                    self.clientlist[i].allotnum += 1
                    return True, i, None

            # 优先缓存数少的
            minallotnum = -1
            num = -1

            for i in range(len(self.clientlist)):
                if self.clientlist[i].allotnum < self.clientlist[i].allotmaxnum:
                    if minallotnum == -1:
                        minallotnum = self.clientlist[i].allotnum
                        num = i
                    elif minallotnum > self.clientlist[i].allotnum:
                        minallotnum = self.clientlist[i].allotnum
                        num = i

            if num > -1:
                self.clientlist[num].allotnum += 1
                return True, num, None

            return False, None, "连接缓存已满"

    def __releasecache__(self, num: int):
        """
        释放连接
        :param num 连接编号
        """
        self.lock.acquire()
        self.clientlist[num].allotnum -= 1
        self.lock.release()
