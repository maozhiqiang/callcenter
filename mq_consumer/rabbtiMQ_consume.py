# -*- encoding: utf-8 -*-
__author__ = 'Arvin wu'
import pika
import json
import Config as conf
from DBPool import Postgresql_Pool as db_pool
from LogUtils import Logger
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
logger = Logger()

credentials = pika.PlainCredentials(conf.MQ_USERNAME,conf.MQ_PWD)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    conf.MQ_URL,5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='callexchange', exchange_type='direct')
channel.queue_declare(queue='call_api',durable=True)
channel.queue_bind(exchange='callexchange', queue='call_api')
print '[********queue*****]',conf.MQ_QUEUE
def callback(ch, method, properties, body):
    logger.info(" [x] Received %r\n\n" % body)
    dict = json.loads(body)
    print '**********',dict
    if dict['mark'] == 'insert':
        sql = 'INSERT INTO fs_call_replay(who, text, record_fpath, create_at, call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\',\'{5}\')'.format(
            dict['who'], dict['text'], dict['record_fpath'], dict['create_at'],dict['call_id'] , dict['jsonStr'])
        run_insert_sql(sql)
        logger.info('run_insert_sql.....%s' % sql)
    else:
        # print '................',dict['record_fpath'],dict['channal_uuid']
        sql = "update fs_call set full_record_fpath ='{0}' where channal_uuid ='{1}'".format(dict['record_fpath'],dict['channal_uuid'] )
        run_update_sql(sql)
        logger.info('run_update_sql.....%s' % sql)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def run_insert_sql(sql):
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        logger.error('runsql exception error %s '%e)

def run_update_sql(sql):
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        logger.error('runsql exception error %s '%e)

channel.basic_consume(callback,queue=conf.MQ_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()