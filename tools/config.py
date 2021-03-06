# -*- coding: UTF-8 -*-

#======================================================================================================
#======================================================================================================
#======================================================================================================
#=============================================Ning Bo==================================================
#=======================freeswitch  外网ip 121.42.31.97  内网ip:10.163.250.207                 =========
#=======================web         外网ip:121.42.36.138 内网ip:10.165.51.223                  =========
#=======================flow        ip 123.59.82.44                                           =========
#======================================================================================================
#======================================================================================================

#------流程配置信息
# flow_host = '123.59.82.44'
# flow_port = 8080
# flow_url = "/flow/execute.do"
# key = 'The nature of the polymer is currently a trade secret'
# flow_close_url = "/flow/close.do"
# #-----百度语音配置信息
# AI_userId = 'callcenter'
# AI_appid = 'dhcs94484422366'
# AI_secret = '4e96fc3e31546c19d7aac41018136649'
# AI_key = 'QOROS'
# #-----redis  配置文件
# REDIS_DB = 'cache'
# REDIS_PORT = 6379
# REDIS_HOST = '10.165.51.223'# 宁波redis  连接web服务器的redis
# #----- postgresql  配置文件
# POSTGRESQL_HOST = "10.165.51.223" #要链接的服务器的IP地址，Server-IP 138 web
# POSTGRESQL_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
# POSTGRESQL_NAME = "postgres" #数据库名称
# POSTGRESQL_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
# POSTGRESQL_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的
# #----- rabbtimq  配置文件
# rabbitmq_server = '10.165.51.223'
# rabbtimq_port = 5672
# rabbitmq_user = 'admin'
# rabbit_password = '123123'
# #------讯飞配置文件
# #XUNFEI_URL = '117.121.21.146'
# XUNFEI_URL = 'openapi.openspeech.cn'

#======================================================================================================
#======================================================================================================
#======================================================================================================
#=============================================Aicyber==================================================
#=======================freeswitch  外网ip 118.190.166.134  内网ip:10.31.91.222                 ========
#=======================web         外网ip:118.190.166.165  内网ip:10.31.92.12                  ========
#=======================flow        ip 117.50.8.27                                            =========
#======================================================================================================
#======================================================================================================
#------流程配置信息
#flow_host = '123.59.82.44'
flow_host = '117.50.8.27'
flow_port = 8080
flow_url = "/flow/execute.do"
key = 'The nature of the polymer is currently a trade secret'
flow_close_url = "/flow/close.do"
#-----百度语音配置信息
AI_userId = 'callcenter'
AI_appid = 'dhcs94484422366'
AI_secret = '4e96fc3e31546c19d7aac41018136649'
AI_key = 'QOROS'
#-----redis  配置文件
REDIS_DB = 'cache'
REDIS_PORT = 6379
REDIS_HOST = '10.31.92.12'#redis 134
#----- postgresql  配置文件
POSTGRESQL_HOST = "10.31.92.12" #要链接的服务器的IP地址，Server-IP 138 web
POSTGRESQL_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
POSTGRESQL_NAME = "postgres" #数据库名称
POSTGRESQL_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
POSTGRESQL_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的
#----- rabbtimq  配置文件
rabbitmq_server = '10.31.92.12'#134
rabbtimq_port = 5672
rabbitmq_user = 'admin'
rabbit_password = '123123'
#------讯飞配置文件
#XUNFEI_URL = '117.121.21.146'
XUNFEI_URL = 'openapi.openspeech.cn'
#=============SoniVoice=============

#======================================================================================================
#======================================================================================================
# update fs_call set full_record_fpath = '/audio/88448e11861e7995d723fe2eda17a6b3/all_audio/13901268648_full_20171128164437_.wav' where id = 1349301
#======================================================================================================
#=============================================Ucloud ==================================================
#=======================freeswitch  外网ip 106.75.47.65     内网ip:10.9.179.149                 ========
#=======================web         外网ip:106.75.96.155    内网ip:10.9.169.85                  ========
#=======================flow        外网ip:106.75.61.164    内网ip:10.9.179.149                =========
#======================================================================================================
#======================================================================================================

#------流程配置信息
# flow_host = '106.75.61.164'
# flow_port = 8080
# flow_url = "/flow/execute.do"
# key = 'The nature of the polymer is currently a trade secret'
# flow_close_url = "/flow/close.do"
# #-----百度语音配置信息
# AI_userId = 'callcenter'
# AI_appid = 'dhcs94484422366'
# AI_secret = '4e96fc3e31546c19d7aac41018136649'
# AI_key = 'QOROS'
# #-----redis  配置文件
# REDIS_DB = 'cache'
# REDIS_PORT = 6379
# REDIS_HOST = '10.9.169.85'
# #----- postgresql  配置文件
# POSTGRESQL_HOST = "10.9.90.133" #要链接的服务器的IP地址，Server-IP 138 web
# POSTGRESQL_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
# POSTGRESQL_NAME = "call" #数据库名称
# POSTGRESQL_USERNAME = "root" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
# POSTGRESQL_PASSWORD = "z8asuidnaicyber" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的
# #----- rabbtimq  配置文件
# rabbitmq_server = '10.9.169.85'
# rabbtimq_port = 5672
# rabbitmq_user = 'admin'
# rabbit_password = '123123'
# #------讯飞配置文件
# #XUNFEI_URL = '117.121.21.146'
# XUNFEI_URL = 'openapi.openspeech.cn'
