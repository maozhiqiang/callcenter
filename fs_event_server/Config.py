# coding=utf-8
__author__ = 'Arvin.Wu'

#====================POSGRESQL===================

DATABASE_HOST = "121.42.36.138" #要链接的服务器的IP地址，local-IP
#DATABASE_HOST = "192.168.0.183" #要链接的服务器的IP地址，Server-IP
DATABASE_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
DATABASE_NAME = "postgres" #数据库名称
DATABASE_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
DATABASE_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的

#====================QueueManager===============
queue_ip = '192.168.0.183'
queue_port = 50000
queue_authkey = 'aicyberqueue'

#====================ESL  Config==================

ESL_HOST = '121.42.31.97'
ESL_PORT = 8021
ESL_PWD = 'Aicyber'

#====================扣费 云上==================
#server_url = 'http://121.42.36.138:8000/api/finance/minute/update/'
#====================扣费 local==================
server_url = 'http://192.168.0.183:8000/api/finance/minute/update/'







