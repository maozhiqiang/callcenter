# -*- coding: UTF-8 -*-
import time
import psycopg2
import psycopg2.extras
from DBPool import Postgresql_Pool as db_pool
from LogUtils import Logger
logger = Logger()

def run_sql(sql):
    logger.info('[sql__run]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        print("  runsql ...except error %s" % e.message)

def update_sql(sql):
    logger.info('[sql__update]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        print  ("  update_sql ...except error %s" % e.message)

def get_one_sql(sql):
    logger.info('[sql__get_one]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        count = cursor.execute(sql, )
        conn.commit()
        result = cursor.fetchone()  # 获取一条数据
        db_pool.close(cursor, conn)
        return  result
    except Exception as e:
        print   ("  get_one_sql ...except error %s" % e.message)

def get_all_sql(sql):
    #logger.info('[get_all_sql]....%s' % sql)
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        count = cursor.execute(sql, )
        conn.commit()
        list = cursor.fetchall()  # 获取所有数据
        db_pool.close(cursor, conn)
        return list
    except Exception as e:
        print ("  get_all_sql ...except error %s" % e.message)

def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False
if __name__ == '__main__':
    # # sql = "select * from fs_call where channal_uuid = 'b86e58df-3af7-40d4-be71-3c934a95e9fe'"
    # sql = "select  fs_call.answer_at,fs_call.finish_at,fs_call.task_id,task.user_id " \
    #       "from fs_call left join fs_task as task on fs_call.task_id = task.id " \
    #       "where channal_uuid = 'b86e58df-3af7-40d4-be71-3c934a95e9fe'"
    # sql =  " update fs_user set call_minute = call_minute - {0} where id = {1} "
    # sql = sql.format(1,12)
    # info = update_sql(sql)
    # print info
    #
    list_item = []
    sql = 'select who,text,record_fpath,create_at from fs_call_replay  where call_id = 1 ORDER BY create_at'
    result = get_all_sql(sql)
    print  type(result)
    import Config as conf
    for item in result:
        print item['record_fpath']
        print 50*'--'
        ss = conf.playbaclaudio+item['record_fpath']
        print ss
        item['record_fpath'] = ss
        print 50 * '***'
        print "***%s**\n\n"%item['record_fpath']
    print result
        # for key in item.items():
        #     print key[0]+':'+str(key[1])





    # print  '\n'
    # print '接通时间',result[0]
    # print '挂机时间',result[1]
    # print '任务Id',result[2]
    # end_time =result[1]
    # start_time = result[0]
    # if is_valid_date(start_time) and is_valid_date(end_time):
    #     print '*************'
    #     diff_seconds = (end_time - start_time).seconds
    #     if diff_seconds % 60 == 0:
    #         print '通话分钟数', diff_seconds / 60
    #     else:
    #         print '通话分钟数', diff_seconds / 60 + 1
    # else:
    #     print '-------------'


