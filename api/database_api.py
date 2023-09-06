from system.singleton import singleton
from database.commsql import CommSql
import os
import uuid
import hashlib
import json
from system.yaml_config import YamlConfig
from system.log import log
import re


@singleton
class DatabaseApi(object):
    client = None
    type = None
    match_str = None

    def __init__(self) -> None:
        try:
            self.type = "SQLite"
            self.match_str = "?"
        except Exception as result:
            log().info("初始化错误, {}".format(result))

    def init_config(self):
        try:
            yaml_config = YamlConfig()
            yaml_config.load_config()
            config = yaml_config.get_config()
            self.type = config.get("db_type", "SQLite")
            if self.type == "SQLite":
                self.match_str = "?"
            else:
                self.match_str = "%s"
            self.client = CommSql(
                type=self.type,
                database=config.get("database").get("name"),
                ip=config.get("database").get("ip"),
                port=config.get("database").get("port"),
                username=config.get("database").get("username"),
                password=config.get("database").get("password"),
            )
            file_data = ""
            file_path = ""
            if self.type == "SQLite":
                file_path = os.path.join(os.getcwd(), "config", "sqlite.sql")
            elif self.type == "MySQL":
                file_path = os.path.join(os.getcwd(), "config", "mysql.sql")
            with open(file_path, mode="r", encoding="utf-8") as file:
                file_data = file.read()
            if not file_data:
                log().info("初始化错误, SQL文件[{}]加载失败".format(file_path))
                return False
            sql_list = re.findall(
                pattern="[CREATE|SET|PRAGMA][\s\S]+?;", string=file_data
            )
            if not sql_list:
                log().info("初始化错误, SQL文件[{}]语句解析失败".format(file_path))
                return False
            for sql in sql_list:
                p, err = self.client.execution(sql=sql)
                if not p:
                    log().info("初始化错误, SQL初始化失败, {}".format(err))
                    return False
            return True
        except Exception as result:
            log().info("初始化错误, {}".format(result))
        return False

    def login(self, username: str, password: str, client_id: str, client_uuid: str):
        info = None
        err = None
        try:
            password = hashlib.md5(str(password).encode("utf8")).hexdigest()
            p, data, err = self.client.query(
                sql="SELECT * FROM users where username = {0} and password = {0};".format(
                    self.match_str
                ),
                parameters=(username, password),
            )
            if not p or not len(data):
                err = "账号不存在"
                return False, info, err
            token = uuid.uuid4().hex
            p, err = self.client.execution(
                sql="DELETE FROM token WHERE username = {0} and client_id = {0} and uuid = {0};".format(
                    self.match_str
                ),
                parameters=(username, client_id, client_uuid),
            )
            if not p:
                err = "登录失败, 无法删除登录信息"
                return False, info, err
            info = data[0]
            info["token"] = token
            uid = info["id"]
            p, err = self.client.execution(
                sql="INSERT INTO token(username, uid, client_id, uuid, access_token) VALUES({0}, {0}, {0}, {0}, {0});".format(
                    self.match_str
                ),
                parameters=(username, uid, client_id, client_uuid, token),
            )
            if not p:
                err = "登录失败, 无法记录登录信息"
                return False, info, err
            return True, info, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, info, err

    def logout(self, client_id: str, client_uuid: str):
        err = None
        try:
            p, err = self.client.execution(
                sql="DELETE FROM token WHERE client_id = {0} and uuid = {0};".format(
                    self.match_str
                ),
                parameters=(client_id, client_uuid),
            )
            if not p:
                err = "退出登录失败, 无法删除登录信息"
                return False, err
            return True, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, err

    def get_user(self, client_id: str, client_uuid: str, token: str):
        info = None
        err = None
        try:
            p, data, err = self.client.query(
                sql="SELECT * FROM token where client_id = {0} and uuid = {0} and access_token = {0};".format(
                    self.match_str
                ),
                parameters=(client_id, client_uuid, token),
            )
            if not p or not len(data):
                err = "账号不存在"
                return False, info, err

            info = data[0]
            return True, info, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, info, err

    def get_addr_book(self, token: str):
        info = None
        err = None
        try:
            p, data, err = self.client.query(
                sql="SELECT * FROM token where access_token = {0};".format(
                    self.match_str
                ),
                parameters=(token,),
            )
            if not p or not len(data):
                err = "登录信息无效"
                return False, info, err
            p, tag_data, err = self.client.query(
                sql="SELECT * FROM tags where uid = {0};".format(self.match_str),
                parameters=(data[0]["uid"],),
            )
            info = {}
            info["tags"] = tag_data
            p, peers_data, err = self.client.query(
                sql="SELECT * FROM peers where uid = {0};".format(self.match_str),
                parameters=(data[0]["uid"],),
            )
            info["peers"] = peers_data
            return True, info, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, info, err

    def set_addr_book(self, add_data, token: str):
        err = None
        try:
            p, data, err = self.client.query(
                sql="SELECT * FROM token where access_token = {0};".format(
                    self.match_str
                ),
                parameters=(token,),
            )
            if not p or not len(data):
                err = "登录信息无效"
                return False, err
            p, err = self.client.execution(
                sql="DELETE FROM tags WHERE uid = {0};".format(self.match_str),
                parameters=(data[0]["uid"],),
            )
            if not p:
                err = "删除标签失败"
                return False, err
            tags = add_data["tags"]
            peers = add_data["peers"]
            for tag in tags:
                p, err = self.client.execution(
                    sql="INSERT INTO tags(uid, tag) VALUES({0}, {0});".format(
                        self.match_str
                    ),
                    parameters=(data[0]["uid"], tag),
                )
                if not p:
                    err = "更新标签失败"
                    return False, err
            p, err = self.client.execution(
                sql="DELETE FROM peers WHERE uid = {0};".format(self.match_str),
                parameters=(data[0]["uid"],),
            )
            if not p:
                err = "删除通讯录失败"
                return False, err
            for peer in peers:
                p, err = self.client.execution(
                    sql="INSERT INTO peers(uid, client_id, username, hostname, alias, platform, tags, forceAlwaysRelay, rdpPort, rdpUsername) VALUES({0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0});".format(
                        self.match_str
                    ),
                    parameters=(
                        data[0]["uid"],
                        peer["id"],
                        peer["username"],
                        peer["hostname"],
                        peer["alias"],
                        peer["platform"],
                        json.dumps(peer["tags"]),
                        peer.get("forceAlwaysRelay", ""),
                        peer.get("rdpPort", ""),
                        peer.get("rdpUsername", ""),
                    ),
                )
                if not p:
                    err = "更新通讯录失败"
                    return False, err
            return True, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, err

    def register(self, username: str, password: str):
        err = None
        try:
            p, data, err = self.client.query(
                sql="SELECT * FROM users where username = {0};".format(self.match_str),
                parameters=(username,),
            )
            if not p:
                err = "注册失败, 无法检索用户是否存在"
                return False, err
            elif len(data):
                err = "注册失败, 用户已存在"
                return False, err
            password = hashlib.md5(str(password).encode("utf8")).hexdigest()
            p, err = self.client.execution(
                sql="INSERT INTO users(username, password) VALUES({0}, {0});".format(
                    self.match_str
                ),
                parameters=(username, password),
            )
            if not p:
                err = "注册失败, 无法记录用户信息"
                return False, err
            return True, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, err

    def set_password(self, username: str, password: str, new_password: str):
        err = None
        try:
            p, data, err = self.client.query(
                sql="SELECT * FROM users where username = {0};".format(self.match_str),
                parameters=(username,),
            )
            if not p:
                err = "修改失败, 无法检索用户是否存在"
                return False, err
            elif not len(data):
                err = "修改失败, 用户不存在"
                return False, err
            password = hashlib.md5(str(password).encode("utf8")).hexdigest()
            new_password = hashlib.md5(str(new_password).encode("utf8")).hexdigest()
            p, err = self.client.execution(
                sql="UPDATE users SET password = {0} WHERE username = {0} and password = {0};".format(
                    self.match_str
                ),
                parameters=(new_password, username, password),
            )
            if not p:
                err = "修改密码失败"
                return False, err
            return True, err
        except Exception as result:
            err = "异常错误, {}".format(result)

        return False, err
