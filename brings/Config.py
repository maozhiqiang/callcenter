# coding=utf-8
__author__ = 'Arvin.Wu'

#====================POSGRESQL===================
#
# DATABASE_HOST = "10.9.90.133" #要链接的服务器的IP地址，local-IP
# #DATABASE_HOST = "192.168.0.183" #要链接的服务器的IP地址，Server-IP
# DATABASE_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
# DATABASE_NAME = "call" #数据库名称
# DATABASE_USERNAME = "root" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
# DATABASE_PASSWORD = "z8asuidnaicyber" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的
#==========
#postgresql     username:call
#               user :root
#               pass118.190.166.165" #要链接的服务器的IP地址，local-IP
DATABASE_HOST = "118.190.166.165" #要链接的服务器的IP地址，Server-IP
DATABASE_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
DATABASE_NAME = "postgres" #数据库名称
DATABASE_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
DATABASE_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的
#postgresql+psycopg2://user:password@ip:port/db_name

MYSQL_SERVER='127.0.0.1'
MYSQL_SERVER_PORT=3306
MYSQL_SERVER_DATABASE='mytest'
MYSQL_SERVER_USERNAME='root'
MYSQL_SERVER_PASSWORD='mysql'
MYSQL_SERVER_CHARSET = "utf8"
MYSQL_SERVER_URI='mysql+pymysql://root:mysql@127.0.0.1:3306/mytest'