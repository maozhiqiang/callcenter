# -*- coding: utf-8 -*-
import sys
import  datetime
import hashlib
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf8')

#=================服务器 info=====================================
#server="121.42.31.97"
#server_url = "http://121.42.31.97/recordvoice"
server="127.0.0.1"
server_url = "http://127.0.0.1/recordvoice"

#=====================Flow Config start==========================
#start flow
flow_host = '192.168.0.185'
flow_port = 9090
flow_url = "/flow/execute.do"
#closeflow
key = 'The nature of the polymer is currently a trade secret'
flow_close_url = "/flow/close.do"

#=====================Baidu Asr start  ==========================
AI_userId = 'callcenter'
AI_appid = 'dhcs94484422366'
AI_secret = '4e96fc3e31546c19d7aac41018136649'
AI_key = 'QOROS'

#========================redis ==================================
REDIS_DB = 'cache'
REDIS_PORT = 6379
#REDIS_HOST = '121.42.36.138'
REDIS_HOST = '127.0.0.1'
#======================postgresql================================
#POSTGRESQL_HOST = "192.168.0.183" #要链接的服务器的IP地址，local-IP
#POSTGRESQL_HOST = "121.42.36.138" #要链接的服务器的IP地址，Server-IP
POSTGRESQL_HOST = "192.168.0.185" #要链接的服务器的IP地址，Server-IP
POSTGRESQL_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
POSTGRESQL_NAME = "postgres" #数据库名称
POSTGRESQL_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
POSTGRESQL_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的

#====================rebbitmq=====================================
#rabbitmq_server = '121.42.36.138'
rabbtimq_port = 5672
rabbitmq_user = 'admin'
rabbit_password = '123123'
