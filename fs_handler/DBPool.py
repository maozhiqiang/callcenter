# -*- encoding: utf-8 -*-
import psycopg2
import psycopg2.extras

import Config as conf

DATABASE_HOST = conf.DATABASE_HOST
DATABASE_PORT = conf.DATABASE_PORT
DATABASE_NAME = conf.DATABASE_NAME
DATABASE_USERNAME = conf.DATABASE_USERNAME
DATABASE_PASSWORD = conf.DATABASE_PASSWORD
from DBUtils.PooledDB import PooledDB
from LogUtils import Logger
logger = Logger()
print '[--------db-host-----]',conf.DATABASE_HOST
class Postgresql_Pool(object):
    """
       postgresql数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = postgresql.getConn()
               释放连接对象;conn.close()或del conn
       """
    # 连接池对象
    __pool = None

    @staticmethod
    def getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        #logger.info('postgresql connect host .....   %s' % DATABASE_HOST)
        if Postgresql_Pool.__pool is None:
            Postgresql_Pool.__pool = PooledDB(creator=psycopg2, mincached=2, maxcached=10,
                                        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USERNAME,
                                              password=DATABASE_PASSWORD,
                                              database=DATABASE_NAME)
        return Postgresql_Pool.__pool.connection()

    @staticmethod
    def close(cursor, conn):
        """
        @summary: 释放连接池资源
        """
        #logger.info('postgresql connect.....closed!!!')
        cursor.close()
        conn.close()




