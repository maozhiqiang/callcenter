# -*- coding: UTF-8 -*-

from DBPool import Postgresql_Pool as db_pool
from LogUtils import Logger
logger = Logger()

def run_sql(sql):
    logger.info('[sql]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        logger.info("  runsql ...except error %s" % e.message)

def update_sql(sql):
    logger.info('[sql]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        logger.info("  update_sql ...except error %s" % e.message)

def get_one_sql(sql):
    logger.info('[sql]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        result = cursor.fetchone()  # 获取一条数据
        db_pool.close(cursor, conn)
        return  result
    except Exception as e:
        logger.info("  get_one_sql ...except error %s" % e.message)

def get_all_sql(sql):
    logger.info('[get_all_sql]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        list = cursor.fetchall()  # 获取所有数据
        db_pool.close(cursor, conn)
        return list
    except Exception as e:
        logger.info("  get_all_sql ...except error %s" % e.message)

if __name__ == '__main__':
    sql = "select * from fs_host"
    result = get_all_sql(sql)
    print  result

