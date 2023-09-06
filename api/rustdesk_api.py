import tornado.ioloop
import tornado.web
import json
from api.database_api import DatabaseApi
import time
from system.log import log


# 定义一个基类handler，可以跨域访问
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self) -> None:
        # 表示对所有用户的请求都允许，允许其跨域操作
        if self.request.headers.get("Origin"):
            self.set_header(
                "Access-Control-Allow-Origin", self.request.headers.get("Origin")
            )
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header("Access-Control-Allow-Headers", "Content-Type")

    def options(self):
        self.set_status(200)  # 这里的状态码一定要设置200，建议
        self.finish()


class Register(BaseHandler):
    def get(self):
        root_object = {}
        try:
            client = DatabaseApi()
            p, err = client.register(
                username=self.get_argument("username"),
                password=self.get_argument("password"),
            )
            if p:
                root_object["msg"] = "注册成功"
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("注册, 响应{}".format(root_object))
        self.write(root_object)

    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            client = DatabaseApi()
            p, err = client.register(
                username=data["username"], password=data["password"]
            )
            if p:
                root_object["msg"] = "注册成功"
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("注册, 响应{}".format(root_object))
        self.write(root_object)


class SetPassWord(BaseHandler):
    def get(self):
        root_object = {}
        try:
            client = DatabaseApi()
            p, err = client.set_password(
                username=self.get_argument("username"),
                password=self.get_argument("password"),
                new_password=self.get_argument("new_password"),
            )
            if p:
                root_object["msg"] = "修改成功"
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("修改密码, 响应{}".format(root_object))
        self.write(root_object)

    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            client = DatabaseApi()
            p, err = client.set_password(
                username=data["username"],
                password=data["password"],
                new_password=data["new_password"],
            )
            if p:
                root_object["msg"] = "修改成功"
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("修改密码, 响应{}".format(root_object))
        self.write(root_object)


class Login(BaseHandler):
    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            client = DatabaseApi()
            p, info, err = client.login(
                username=data["username"],
                password=data["password"],
                client_id=data["id"],
                client_uuid=data["uuid"],
            )
            if p:
                root_object = {
                    "type": "access_token",
                    "access_token": info["token"],
                    "user": {
                        "name": data["username"],
                        "email": info.get("email", ""),
                        "note": info.get("note", ""),
                        "status": info["status"],
                        "grp": info["group"],
                        "is_admin": True if info["is_admin"] == 1 else False,
                    },
                }
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("登录, 响应{}".format(root_object))
        self.write(root_object)


class GetUser(BaseHandler):
    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            client = DatabaseApi()
            token = self.request.headers.get("Authorization").replace("Bearer ", "")
            p, info, err = client.get_user(
                client_id=data["id"], client_uuid=data["uuid"], token=token
            )
            if p:
                root_object = {
                    "name": info["username"],
                    "email": info["email"],
                    "note": info["note"],
                    "status": info["status"],
                    "grp": info["group"],
                    "is_admin": True if info["is_admin"] == 1 else False,
                }
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("获取用户信息, 响应{}".format(root_object))
        self.write(root_object)


class GetAddrBook(BaseHandler):
    def get(self):
        root_object = {}
        try:
            root_object = {}
            client = DatabaseApi()
            token = self.request.headers.get("Authorization").replace("Bearer ", "")
            p, info, err = client.get_addr_book(token=token)
            tags = []
            peers = []
            if p:
                for row in info["tags"]:
                    tags.append(row["tag"])
                for row in info["peers"]:
                    peers.append(
                        {
                            "id": row["client_id"],
                            "username": row["username"],
                            "hostname": row["hostname"],
                            "alias": row["alias"],
                            "platform": row["platform"],
                            "tags": json.loads(row["tags"]),
                            "forceAlwaysRelay": row["forceAlwaysRelay"],
                            "rdpPort": row["rdpPort"],
                            "rdpUsername": row["rdpUsername"],
                        }
                    )
                root_object = {"data": json.dumps({"tags": tags, "peers": peers})}
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("获取通讯录, 响应{}".format(root_object))
        self.write(root_object)

    def post(self):
        root_object = {}
        try:
            root_object = {}
            client = DatabaseApi()
            token = self.request.headers.get("Authorization").replace("Bearer ", "")
            data = json.loads(self.request.body)  # 解析 JSON 数据
            add_data = json.loads(data["data"])
            p, err = client.set_addr_book(add_data=add_data, token=token)

            if p:
                root_object = {}
            else:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("更新通讯录, 响应{}".format(root_object))
        self.write(root_object)


class LoginOptions(BaseHandler):
    def get(self):
        root_object = {}
        try:
            root_object = {}
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        self.write(root_object)


class Logout(BaseHandler):
    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            client = DatabaseApi()
            p, err = client.logout(
                client_id=data["id"],
                client_uuid=data["uuid"],
            )
            if not p:
                root_object["error"] = err
                self.set_status(201)
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("退出登录, 响应{}".format(root_object))
        self.write(root_object)


class Heartbeat(BaseHandler):
    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            root_object = {"modified_at": int(time.time())}
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("心跳, 响应{}".format(root_object))
        self.write(root_object)


class Sysinfo(BaseHandler):
    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据

        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("系统信息, 响应{}".format(root_object))
        self.write(root_object)


class Audit(BaseHandler):
    def get(self):
        root_object = {}
        try:
            root_object = {}

        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        self.write(root_object)

    def post(self):
        root_object = {}
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
        except Exception as result:
            root_object["error"] = "异常错误, {}".format(result)
            self.set_status(201)
        log().info("操作, 响应{}".format(root_object))
        self.write(root_object)
