# Redis监控

## 说明
基于```Python Flask + G2```实现，监控常用Redis性能指标，如```userd_memory、 total_command_processed、connection_clients```等等。

## 环境要求
	Python：2.7.*
	Flask：0.12.* ， 提供web服务
	Redis：要监控的redis
	MongoDB或Mysql：用于存储监控数据


## 安装
在Debian或Ubuntu上：
1. 安装python：           ```sudo apt-get install python```
2. 安装Flask：             ```sudo pip install Flask```
3. 安装mongodb(推荐)或mysql：    ```sudo apt-get install mongodb```
4. 安装python redis包      ```sudo pip install redis```
5. 安装python pymongo：   ```sudo pip install pymongo```
6. 安装python MySQLdb包    （可选，默认是用mongodb）

## 配置
(如用mysql存储数据，则先需导入数据表结构，脚本文件在```sql/mysql.sql```)
编辑```config.py```文件：
* REDIS_SERVERS:：要监控的Redis，可配置多个
* DATA_STORE_TYPE：存储到何处，值为```mongodb```或```mysql```，默认mongodb
* STORE_MONGODB：mongodb参数配置
* STORE_MYSQL：mysql参数配置（选mongodb时可不配置此项）

## 使用
1. 启动redis监控脚本：```./redis_monitor.py --duration=100 --interval=3```(```duration```：持续时间：```interval```：隔多少秒监控一次，如用后台执行，在命令后面加```&```)
2. 启动flask应用：```./app.py```
3. 打开浏览器输入：```http://localhost:5000/```

## 结果
![image](https://github.com/Kevinsss/redis_monitor/blob/master/result/result.png)