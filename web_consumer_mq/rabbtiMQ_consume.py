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

credentials = pika.PlainCredentials('admin','123123')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    conf.MQ_URL,5672,'/',credentials))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='durable',durable=True)


def callback(ch, method, properties, body):
    logger.info(" [x] Received %r\n\n" % body)
    dict = json.loads(body)
    print '**********',dict
    if dict['mark'] == 'insert':
        print  '-------------', dict['who'], dict['text'], dict['record_fpath'], dict['create_at'], dict['call_id'], \
        dict['jsonStr']
        sql = 'INSERT INTO fs_call_replay(who, text, record_fpath, create_at, call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\',\'{5}\')'.format(
            dict['who'], dict['text'], dict['record_fpath'], dict['create_at'],dict['call_id'] , dict['jsonStr'])

    else:
        print '................',dict['record_fpath'],dict['channal_uuid']
        sql = "update fs_call set full_record_fpath ='{0}' where channal_uuid ='{1}'".format(dict['record_fpath'],dict['channal_uuid'] )
    logger.info('runsql.....%s'%sql)
    runsql(sql)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def runsql(sql):
    try:
        conn = db_pool.getConn()
        cursor = conn.cursor()
        count = cursor.execute(sql, )
        logger.info("ID of last record is %d"%int(cursor.lastrowid))  # 最后插入行的主键ID
        conn.commit()
        db_pool.close(cursor, conn)
    except Exception as e:
        logger.error('runsql exception error %s '%e)

channel.basic_consume(callback,
                      queue='durable',
                      #no_ack=True
                      )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()