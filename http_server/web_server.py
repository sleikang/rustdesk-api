# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web


class WebServer:
    app = None
    host = None
    port = None
    err = None

    def __init__(self, host="0.0.0.0", port=8000) -> None:
        try:
            self.app = tornado.web.Application()
            self.host = host
            self.port = port
        except Exception as result:
            self.err = "异常错误, {}".format(result)

    def start(self):
        try:
            # 启动web程序，开始监听端口的连接
            self.app.listen(port=self.port, address=self.host)
            tornado.ioloop.IOLoop.current().start()
        except Exception as result:
            self.err = "异常错误, {}".format(result)

    def add_function(self, host_pattern, host_handlers):
        """
        添加函数接口
        :param host_pattern [in] 接口域名
        :param host_handlers [in] 接口句柄
        """
        try:
            self.app.add_handlers(
                host_pattern=host_pattern, host_handlers=host_handlers
            )
        except Exception as result:
            self.err = "异常错误, {}".format(result)
