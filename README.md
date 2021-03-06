# Redis监控

## 说明
基于```Python Flask + G2```实现，监控常用Redis性能指标，如```userd_memory、 total_command_processed、connection_clients```等等。

![image](https://github.com/Kevinsss/redis_monitor/blob/master/result/result.png)


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
6. 安装python MySQLdb包(默认是用mongodb)     ```sudo pip install mysql-python```

## 配置
(**如用mysql存储数据，则先需导入数据表结构，脚本文件在```sql/mysql.sql```**)

编辑```config.py```文件：
* REDIS_SERVERS:：要监控的Redis，可配置多个
* DATA_STORE_TYPE：存储到何处，值为```mongodb```或```mysql```，默认mongodb
* STORE_MONGODB：mongodb参数配置
* STORE_MYSQL：mysql参数配置（选mongodb时可不配置此项）

## 启动
1. 启动redis监控脚本：```./redis_monitor.py --duration=100 --interval=3```(```duration```：持续时间：```interval```：隔多少秒监控一次，如用后台执行，在命令后面加```&```)
2. 启动flask应用：```./app.py```
3. 打开浏览器输入：```http://ip:5000/```

## Redis常用指标说明
* ```Uptime```: 持续工作时间，单位秒
* ```Max Memory```：限制分配的最大内存，在低版本redis上，```info```命令不显示此信息
* ```Used Memory```：redis数据已用内存
* ```Used Memory Rss```：包含UsedMemory，同时也包括自身的开销
* ```Used Memory Peak```：Used Memory中的最大值
* ```Mem Fragmentation Ratio```：UsedMemoryPeak/UsedMemory的值，1.5左右为比较好的利用率，太大则说明利用率太低或者内存碎片太多，此时可能会影响Redis的性能
* ```Total Commands Processed```：命令处理总数(从Redis启动以来)，如果Redis反应迟钝或者性能地下，可观察此数据的变化情况，如果某一时刻变化很多，说明redis接收了大量的命令请求，因为Redis是单线程的，只能排队执行，导致后面命令响应速度变慢
* ```Total Connection Received```：总的连接数，Redis连接不关闭，会导致Redis拒绝连接，当出现时，检查此项是否达到配置的```MaxClients```
* ```Expired Keys```：过期的key数量
* ```CommadnCount图表```：```Total Commands Processed```的变化情况
* ```Memroy图表```：```Used Memory```和```Used Memory Peak```的变化情况

## 常见问题
1. 安装mysql-python包时报错```mysql_config not found```，缺少libmysqld-dev库(apt-get install libmysqld-dev)安装即可
2. 只用mongodb和mysql其中一种：安装相应的python包(两种包都存在时，可忽略后续步骤)，然后修改```config.py```中的```DATA_STORE_TYPE```的值，最后注释掉```datastore/storefactory```中相应的```import```
3. 各种连接错误：确保你的```Redis、Mongodb、Mysql```参数配置正确，且服务处于开启状态，并且能通过远程连接(如果服务在另外一台机器上)