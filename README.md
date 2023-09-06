# RustDesk API
## 手动注册
```
注册
http://127.0.0.1:21114/api/register?username=test&password=test
修改密码
http://127.0.0.1:21114/api/set_password?username=test&password=test&new_password=123456
```
## 配置文件
```
db_type: "SQLite" #数据库类型 目前支持 SQLite MySQL
database:
    name: "./config/data.db"  #数据名称 SQLite输入文件路径 MySQL输入数据库名称
    username: "root" #MySQL输入数据库账号
    password: "123456" #MySQL输入数据库密码
    ip: "127.0.0.1" #MySQL输入数据库IP
    port: 3306 #MySQL输入数据库端口

```