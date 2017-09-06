#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import psycopg2
import psycopg2.extras
import time
#DATABASE_HOST = "0.0.0.0" #要链接的服务器的IP地址，local-IP
DATABASE_HOST = "192.168.0.183" #要链接的服务器的IP地址，Server-IP
DATABASE_PORT = 5432 #postgresql端口号，安装postgresql时设置的，一般默认是5432
DATABASE_NAME = "postgres" #数据库名称
DATABASE_USERNAME = "postgres" #用户名，这里的用户名也是在安装postgresql时设置的，一般默认postgres
DATABASE_PASSWORD = "z8asuidn" #链接数据库服务器的密码，安装时设置，安装完毕后可以修改的

class DBHelper():
    def __init__(
            self,
            host = DATABASE_HOST,
            port = DATABASE_PORT,
            user = DATABASE_USERNAME,
            password = DATABASE_PASSWORD,
            database = DATABASE_NAME):
        self.conn = psycopg2.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = database)
        self.cursor = self.conn.cursor(
            cursor_factory = psycopg2.extras.DictCursor)
        self.result = None

    def getNextOne(self, ):
        self.result = self.cursor.fetchone()
        return self.result

    def getAll(self, ):
        self.result = self.cursor.fetchall()
        return self.result

    def getCurrentOne(self, ):
        return self.result

    def insertSql(self,sql):
        self.cursor.execute(sql)

    def updateSql(self,answer_at,uuid):
        sql = 'update fs_call set answer_at = %s where channal_uuid = %s'
        self.cursor.execute(sql,(answer_at,uuid))

    def getChannalUuid(self,queueSize=2):
        sql = "select channal_uuid from fs_call where call_status='run' limit {0}".format(queueSize)
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        return self.result

    def getCustnumber_and_callStatus(self,channal_uuid):
        sql = "select cust_number,call_status from fs_call where channal_uuid = '{0}'".format(channal_uuid)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def updateTocallstatus(self,uuid):
        sql = "update fs_call set call_status = 'calling' where channal_uuid = '{0}'".format(uuid)
        self.cursor.execute(sql)
        self.commit()

    def updateFull_record_fpath(self,path,channal_uuid):
        sql = "update fs_call set full_record_fpath ='{0}' where channal_uuid ='{1}'".format(path,channal_uuid)
        self.cursor.execute(sql)
        self.commit()

    def getcallid(self,number,uuid):
        sql = "select id from fs_call where cust_number = '{0}' and channal_uuid = '{1}'".format(number,uuid)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            self.result = result[0]
        else:
            self.result = result
        return self.result

    def getFlowIdAndAppId(self,number,uuid):
        sql = "select 	call.id,call.cust_name, call.cust_number, call.task_id, task.flow_id from fs_call as  call left join fs_task as task on  task.id =call.task_id where channal_uuid = '{0}' and cust_number = '{1}'"
        print 'sql : %s'%sql
        sql = sql.format(uuid,number)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def getFlowId(self,number,uuid):
        sql = "select task.flow_id from fs_call as  call left join fs_task as task on  task.id =call.task_id where channal_uuid = '{0}' and cust_number = '{1}'"
        sql = sql.format(uuid, number)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def record_chat_sql(self,who,text,record_fpath,create_at,call_id,jsonStr):
        sql = "INSERT INTO fs_call_replay(who, text, record_fpath, create_at, call_id,resp_param)VALUES ('{0}', '{1}', '{2}', '{3}', '{4}','{5}')".format(who,text,record_fpath,create_at,call_id,jsonStr)
        self.cursor.execute(sql)
        self.commit()
    def runsql(self, sql):
        result = self.cursor.execute(sql)
        self.commit()
        return result

    def close(self, ):
        self.cursor.close()
        self.conn.close()

    def rowcount(self, ):
        return self.cursor.rowcount

    def commit(self, ):
        return self.conn.commit()

if __name__ == '__main__':

    db = DBHelper()
    # db.runsql('select * from fs_call ')
    # rows = db.cursor.fetchall()
    # for col in rows:
    #     print col
    # list = db.getChannalUuid(2)
    # for col in list:
    #     print col

    # print db.updateTocallstatus('81befead-3b22-4454-a137-518161e80cc5')
    # db.record_chat_sql('bot', '我们楼盘是在南开区，比邻全国重点学府南开大学和天津大学，天拖公交站附近，这边您知道的吧？', '/tmp/15900282168_out_0.wav', '2017-06-24 15:03:23', '2')
    list = db.getFlowIdAndAppId('15900282168','a6ae62b9-b5cd-4e3e-9d1f-f77c8f47ad0c')
    if list is not None:
        print list
        print 'llllllllllllll',list[0]
    # for item in list :
    #     print item
