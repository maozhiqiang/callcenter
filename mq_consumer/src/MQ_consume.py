#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-29 上午10:53
# @Author  : Arvin
# @Site    : 
# @File    : MQ_consume.py
# @Software: PyCharm
import time
import json
import sys
import pika
import httplib
import Config as conf, DBHandler as db
from LogUtils import Logger


reload(sys)
sys.setdefaultencoding('utf-8')
logger = Logger()

credentials = pika.PlainCredentials(conf.MQ_USERNAME,conf.MQ_PWD)
connection = pika.BlockingConnection(pika.ConnectionParameters(conf.MQ_URL,5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='callexchange', exchange_type='direct')
channel.queue_declare(queue=conf.MQ_QUEUE,durable=True)
channel.queue_bind(exchange='callexchange', queue='durable')

def callback(ch, method, properties, body):
    logger.info(" [x] Received %r\n\n" % body)
    dict = json.loads(body)
    if dict['mark'] == 'insert':
        sql = 'INSERT INTO fs_call_replay(who, text, record_fpath, create_at, call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\',\'{5}\')'.format(
            dict['who'], dict['text'], dict['record_fpath'], dict['create_at'],dict['call_id'] , dict['jsonStr'])
        db.run_insert_sql(sql)
        logger.info('run_insert_sql.....%s' % sql)

    elif dict['mark'] == 'user_label':
        sql =  " update fs_call set cust_tag = '{0}' where channal_uuid ='{1}' ".format(dict['user_label'],dict['channal_uuid'])
        db.run_update_sql(sql)
        print ' run_update_sql.........user_label'
    elif dict['mark'] == 'statistical':
        sql = "select replay.text from fs_call " \
              "left join fs_call_replay as replay on fs_call.id = replay.call_id " \
              "where fs_call.id = {0} and replay.who = 'human' ORDER BY  replay.create_at".format(dict['call_id'])
        result  = db.get_all_sql(sql)
        sentences = []
        for item in result:
            sentences.append(item.text)
        print ' [ list_sentens ...%s ] '%sentences
        httpseverclient(dict['flow_id'],sentences,dict['user_id'],dict['number'],dict['task_id'])
    else:
        sql = "update fs_call set full_record_fpath ='{0}' where channal_uuid ='{1}'".format(dict['record_fpath'],dict['channal_uuid'] )
        db.run_update_sql(sql)
        logger.info('run_update_sql.....%s' % sql)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def httpseverclient(flow_id,sentences,user_id,number,task_id):
    httpClient = None
    create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        values = {'flow_id': flow_id, 'sentences': sentences}
        params = json.dumps(values)
        headers = {"Content-type": "application/json"}
        httpClient = httplib.HTTPConnection(conf.flow_host, conf.flow_port, timeout=30)
        httpClient.request("POST", conf.flow_url, params, headers)
        response = httpClient.getresponse()
        if response.status == 200:
            jsonStr = response.read()
            dict = json.loads(jsonStr)
            result = dict
            print dict
            sql = "insert into fs_customer_label (number, label, create_at, user_id)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\') RETURNING id"
            sql_log_1 = "insert into fs_customer_label_log(user_input,similarity,create_at,cust_label_id,key_word,label,user_word,flow_id,task_id) values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\') RETURNING id"
            sql_log_2 = "insert into fs_customer_label_log(user_input,similarity,create_at,key_word,label,user_word,flow_id,task_id) values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\') RETURNING id"
            if dict['successful'] and  len(dict['data'])> 0:
                for item in dict['data']:
                    print item['key_word']
                    label = item['label']
                    last_id = db.run_insert_sql(sql.format(number,label,create_at,user_id))
                    print '[ last_id ]----',last_id
                    if last_id == None:
                        db.run_insert_sql(sql_log_2.format(item['sentence'],item['similarity'],create_at,item['key_word'],item['label'],item['word'],flow_id,task_id))
                    else:
                        db.run_insert_sql(
                            sql_log_1.format(item['sentence'], item['similarity'], create_at, last_id, item['key_word'],
                                             item['label'], item['word'], flow_id, task_id))
        else:
            result = {'successful': False, 'message': 'httpclient error'}
            logger.info('.......httpClient error status : %s' % response.status)
    except Exception, e:
        result = {'successful': False, 'message': 'httpclient exception'}
        logger.info('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()
    return result

channel.basic_consume(callback,queue=conf.MQ_QUEUE)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
#
# if __name__ == '__main__':
#     sql = "select fs_call.task_id,replay.text from fs_call " \
#           "left join fs_call_replay as replay on fs_call.id = replay.call_id " \
#           "where fs_call.id = 7 and replay.who = 'human' ORDER BY  replay.create_at"
#     print  sql
#     list_sentens = db.get_all_sql(sql)
#     list = []
#     for item in list_sentens:
#         print item.text
#         print item.task_id
#         list .append(item.text)
#     ll = []
#     ll.append('附近有医院吗')
#     ll.append('附近有学校吗')
#     httpseverclient('23e566219595a9cb92bc3e5a175dbd63',ll,1,'15900282168',5566)
#     # create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     # sql = "insert into fs_customer_label (number, label, create_at, user_id)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\') RETURNING id"
    #
    # id = db.run_insert_sql(sql.format('15900282168','qqq',create_at,1))
    # print id




