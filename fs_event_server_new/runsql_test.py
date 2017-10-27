# -*-coding: utf-8 -*-
"""Freeswitch主机事件监听处理进程

1.对每台fs主机外呼调用，由run_call(只在web服务机器中运行)外呼进程依据host表中的fs主机配置，任务配额，发起外呼调用
2.此进程运行在各fs主机上，监听通道事件并处理，跟远程队列服务通信，及数据库访问
"""
import ESL
import atexit
import signal
import sys
import time
import Config as conf
import multiprocessing
from multiprocessing import managers
from DBPool import Postgresql_Pool as db_pool
from LogUtils import Logger


logger = Logger()

def runsql(sql):
   logger.info('[sql]....%s'%sql)
   try:
       conn = db_pool.getConn()
       cursor = conn.cursor()
       count = cursor.execute(sql, )
       print 'count',count
       conn.commit()
       db_pool.close(cursor, conn)
   except Exception as e:
       logger.info("  runsql ...except error %s"%e.message)

if __name__ == '__main__':
    # sql = 'update fs_host set line_use = line_use - 1 where id = 5'
    # runsql(sql)
    pass
