#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-29 上午10:41
# @Author  : Arvin
# @Site    : 
# @File    : DBHandler.py
# @Software: PyCharm
import sys

import psycopg2
import psycopg2.extras

from DBPool import Postgresql_Pool as db_pool
from LogUtils import Logger

reload(sys)
sys.setdefaultencoding('utf-8')
logger = Logger()

def run_insert_sql(sql):
    logger.debug('------run_insert_sql: %s'%sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        id = cursor.fetchone()[0]
        print "ID of last record is ",id  # 最后插入行的主键ID
        conn.commit()
        logger.debug('------run_insert_sql finish: %s' % sql)
        db_pool.close(cursor, conn)
        return id
    except Exception as e:
        logger.error('runsql exception error %s '%e)

def run_update_sql(sql):
    logger.debug('\n\n------run_update_sql: %s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        logger.debug('------run_update_sql finish: %s' % sql)
        db_pool.close(cursor, conn)
    except Exception as e:
        logger.error('runsql exception error %s '%e)

def get_one_sql(sql):
    logger.info('[sql__get_one]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        count = cursor.execute(sql, )
        conn.commit()
        result = cursor.fetchone()  # 获取一条数据
        db_pool.close(cursor, conn)
        return  result
    except Exception as e:
        print   ("  get_one_sql ...except error %s" % e.message)

def get_all_sql(sql):
    logger.info('[get_all_sql]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        list = cursor.fetchall()  # 获取所有数据
        db_pool.close(cursor, conn)
        return list
    except Exception as e:
        print ("  get_all_sql ...except error %s" % e.message)
