from sanic import Sanic
from sanic.response import json
from api.database_api import DatabaseApi
import time
from system.log import log
import json as data_json

app = Sanic(name="rustdesk_api")


@app.route("/api/register", name="get_register", methods=["GET"])
async def register(request):
    root_object = {}
    status = 200
    try:
        client = DatabaseApi()
        p, err = client.register(
            username=request.args.get("username"),
            password=request.args.get("password"),
        )
        if p:
            root_object["msg"] = "注册成功"
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/register", name="post_register", methods=["POST"])
async def register(request):
    root_object = {}
    status = 200
    try:
        data = request.json
        client = DatabaseApi()
        p, err = client.register(username=data["username"], password=data["password"])
        if p:
            root_object["msg"] = "注册成功"
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/set_password", name="get_set_password", methods=["GET"])
async def set_password(request):
    root_object = {}
    status = 200
    try:
        client = DatabaseApi()
        p, err = client.set_password(
            username=request.args.get("username"),
            password=request.args.get("password"),
            new_password=request.args.get("new_password"),
        )
        if p:
            root_object["msg"] = "修改成功"
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/set_password", name="post_set_password", methods=["POST"])
async def set_password(request):
    root_object = {}
    status = 200
    try:
        data = request.json
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
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/login", methods=["POST"])
async def login(request):
    root_object = {}
    status = 200
    try:
        data = request.json
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
                    "email": "",
                    "note": "",
                    "status": 1,
                    "grp": info.get("group", ""),
                    "is_admin": False,
                },
            }
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/currentUser", methods=["POST"])
async def get_user(request):
    root_object = {}
    status = 200
    try:
        data = request.json
        client = DatabaseApi()
        token = request.token
        p, info, err = client.get_user(
            client_id=data["id"], client_uuid=data["uuid"], token=token
        )
        if p:
            root_object = {
                "name": info["username"],
                "email": "",
                "note": "",
                "status": 1,
                "grp": info.get("group", ""),
                "is_admin": True,
            }
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/ab", name="get_ab", methods=["GET"])
async def get_addr_book(request):
    root_object = {}
    status = 200
    try:
        client = DatabaseApi()
        token = request.token
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
                        "tags": data_json.loads(row["tags"]),
                        "forceAlwaysRelay": row["forceAlwaysRelay"],
                        "rdpPort": row["rdpPort"],
                        "rdpUsername": row["rdpUsername"],
                    }
                )
            root_object = {"data": data_json.dumps({"tags": tags, "peers": peers})}
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/ab", name="post_ab", methods=["POST"])
async def get_addr_book(request):
    root_object = {}
    status = 200
    try:
        root_object = {}
        client = DatabaseApi()
        token = request.token
        data = request.json
        add_data = data_json.loads(data["data"])
        p, err = client.set_addr_book(add_data=add_data, token=token)

        if p:
            root_object["msg"] = "修改成功"
        else:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/login-options", methods=["GET"])
async def get_login_options(request):
    root_object = {}
    status = 200
    try:
        root_object = {}
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/logout", methods=["POST"])
async def logout(request):
    root_object = {}
    status = 200
    try:
        data = request.json
        client = DatabaseApi()
        p, err = client.logout(
            client_id=data["id"],
            client_uuid=data["uuid"],
        )
        if not p:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    log().info("退出登录, 响应{}".format(root_object))
    return json(body=root_object, status=status)


@app.route("/api/heartbeat", methods=["POST"])
async def heartbeat(request):
    root_object = {}
    status = 200
    try:
        _ = request.json
        root_object = {"modified_at": int(time.time())}
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/sysinfo", methods=["POST"])
async def sysinfo(request):
    root_object = {}
    status = 200
    try:
        data = request.json
        client = DatabaseApi()
        p, err = client.write_system_info(system_info=data)
        if not p:
            root_object["error"] = err
            status = 201
    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201

    return json(body=root_object, status=status)


@app.route("/api/audit/<name>", methods=["GET", "POST"])
async def audit(request, name):
    root_object = {}
    status = 200
    try:
        root_object = {}

    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/users", methods=["GET", "POST"])
async def users(request):
    root_object = {}
    status = 200
    try:
        root_object = {"total": 0, "data": []}

    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)


@app.route("/api/peers", methods=["GET", "POST"])
async def peers(request):
    root_object = {}
    status = 200
    try:
        root_object = {"total": 0, "data": []}

    except Exception as result:
        root_object["error"] = "异常错误, {}".format(result)
        status = 201
    return json(body=root_object, status=status)
