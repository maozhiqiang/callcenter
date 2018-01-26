#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#============== statistical  统计 ==========================
flow_host = '39.107.69.88'
flow_port = 80
flow_url = "/semanteme-label/map-more.do"

#=============DB config ===================================

DATABASE_HOST = "rm-2zeeq8wu95hbrl2gmho.pg.rds.aliyuncs.com" #要链接的服务器的IP地址，local-IP
DATABASE_PORT = 3432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
DATABASE_NAME = "call_crm" #数据库名称
DATABASE_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
DATABASE_PASSWORD = "Z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的

#==================RabbtiMq ===============================
MQ_URL = '127.0.0.17'
MQ_USERNAME = 'admin'
MQ_PWD = '123123'
MQ_QUEUE = 'durable'
# MQ_QUEUE = 'call_api'
MQ_exchange = 'callexchange'
#MQ_exchange = 'callapp'






