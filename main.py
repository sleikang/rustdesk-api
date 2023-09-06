from api import rustdesk_api
from http_server.web_server import WebServer
import sys
import asyncio
from api.database_api import DatabaseApi
from system.log import log

if __name__ == "__main__":
    client = DatabaseApi()
    p = client.init_config()
    if p:
        log().info("初始化配置完成")
        # 在 Windows 上使用 SelectorEventLoop
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        web = WebServer(host="0.0.0.0", port=21114)
        web.add_function(
            host_pattern=".*",
            host_handlers=[
                ("/api/login", rustdesk_api.Login),
                ("/api/logout", rustdesk_api.Logout),
                ("/api/heartbeat", rustdesk_api.Heartbeat),
                ("/api/sysinfo", rustdesk_api.Sysinfo),
                ("/api/login-options", rustdesk_api.LoginOptions),
                ("/api/currentUser", rustdesk_api.GetUser),
                ("/api/ab", rustdesk_api.GetAddrBook),
                ("/api/audit/.*", rustdesk_api.Audit),
                ("/api/register", rustdesk_api.Register),
                ("/api/set_password", rustdesk_api.SetPassWord),
            ],
        )
        log().info("启动服务, 0.0.0.0:21114")
        web.start()
