#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#------------freeswitch-----------
FS_HOST='0.0.0.0'
FS_PORT=8021
FS_auth='ClueCon'


#-----------redis-----------------
REDIS_DB = 'queue'
REDIS_PORT = 6379
REDIS_HOST = '0.0.0.0'

QUEUE_POOL = 2

#-------------flow config---------

host = 'http://123.59.82.44:8080/flow/close.do'
flowId='a599d36c4c7a71ddcc1bc7259a15ac3a'
appId='lcdhjqr97255315906'
key = 'The nature of the polymer is currently a trade secret'

#=============DB config ===================================

DATABASE_HOST = "10.9.111.12" #要链接的服务器的IP地址，local-IP
DATABASE_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
DATABASE_NAME = "postgres" #数据库名称
DATABASE_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
DATABASE_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的

#==================RabbtiMq ===============================
MQ_URL = '127.0.0.1'






