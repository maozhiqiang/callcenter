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

    def get_call_channal_uuid(self,queueSize=2):
        sql = "select channal_uuid from fs_call where call_status='run' limit {0}".format(queueSize)
        result =  self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_number_callStatus(self,channal_uuid):
        sql = "select cust_number,call_status from fs_call where channal_uuid = '{0}'".format(channal_uuid)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def updateTocallstatus(self,uuid):
        sql = "update fs_call set call_status = 'calling' where channal_uuid = '{0}'".format(uuid)
        self.cursor.execute(sql)
        self.commit()

    def getcallid(self,number,uuid):
        sql = "select id from fs_call where cust_number = '{0}' and channal_uuid = '{1}'".format(number,uuid)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is  not None:
            self.result = result[0]
        else:
            self.result = result
        return  self.result

    def getFlowIdAndAppId(self,number,uuid):
        sql = "select 	call.id,call.cust_name, call.cust_number, call.task_id, task.flow_id from fs_call as  call left join fs_task as task on  task.id =call.task_id where channal_uuid = '{0}' and cust_number = '{1}'"
        # print 'sql %s'%sql
        sql = sql.format(uuid,number)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def runsql(self, sql):
        result = self.cursor.execute(sql)
        self.commit()
        # print  result
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
    result = db.get_call_channal_uuid()
    print result[0][0]