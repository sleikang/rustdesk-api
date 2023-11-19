from api.rustdesk_api import app

from api.database_api import DatabaseApi
from system.log import log

if __name__ == "__main__":
    client = DatabaseApi()
    p = client.init_config()
    if p:
        log().info("初始化配置完成")
        app.run(
            host="0.0.0.0",
            port=21114,
            debug=False,
            access_log=False,
            workers=1,
            single_process=True,
        )
        log().info("启动服务, 0.0.0.0:21114")
