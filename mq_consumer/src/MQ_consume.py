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
channel.exchange_declare(exchange=conf.MQ_exchange, exchange_type='direct')
channel.queue_declare(queue=conf.MQ_QUEUE,durable=True)
channel.queue_bind(exchange=conf.MQ_exchange, queue=conf.MQ_QUEUE)


print '==============================================================\n'
print '             rabbtiMQ server:  %s '%conf.MQ_URL
print '             rabbtiMQ exchange:  %s '%conf.MQ_exchange
print '             rabbtiMQ queue:  %s '%conf.MQ_QUEUE

def callback(ch, method, properties, body):
    logger.info(" [x] Received %r\n\n" % body)
    dict = json.loads(body)
    if dict['mark'] == 'insert':
        sql = 'INSERT INTO fs_call_replay(who, text, record_fpath, create_at, call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\',\'{5}\') RETURNING id'.format(
            dict['who'], dict['text'], dict['record_fpath'], dict['create_at'],dict['call_id'] , dict['jsonStr'])
        db.run_insert_sql(sql)
        logger.info('******** run_insert_sql..*********...%s' % sql)

    elif dict['mark'] == 'user_label':
        sql =  " update fs_call set cust_tag = '{0}' where channal_uuid ='{1}' ".format(dict['user_label'],dict['channal_uuid'])
        db.run_update_sql(sql)
        logger.info(' run_update_sql.........user_label...%s'%sql)
    elif dict['mark'] == 'statistical':
        sql = "select replay.text from fs_call " \
              "left join fs_call_replay as replay on fs_call.id = replay.call_id " \
              "where fs_call.id = {0} and replay.who = 'human' ORDER BY  replay.create_at".format(dict['call_id'])
        result  = db.get_all_sql(sql)
        sentences = []
        for item in result:
            sentences.append(item.text)
        print ' [ list_sentens ...%s ] '%sentences
        httpseverclient(dict['flow_id'],sentences,dict['number'],dict['task_id'],dict['user_id'])
    else:
        sql = "update fs_call set full_record_fpath ='{0}' where channal_uuid ='{1}'".format(dict['record_fpath'],dict['channal_uuid'] )
        db.run_update_sql(sql)
        logger.info('run_update_sql.....%s' % sql)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def httpseverclient(flow_id,sentences,number,task_id,user_id):
    httpClient = None
    labels = []
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
            logger.info('[ ==lables== %s ]'%dict)
            sql_select = "select * from fs_customer where number = '{0}' and user_id = {1}"
            sql_update = " update fs_customer set label = label || '{0}' where number = '{1}'  and user_id = {2} "
            sql_log = " insert into fs_customer_label_log(task_id,flow_id,user_input,user_word,key_word,label,similarity,create_at) values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\') RETURNING id"
            if dict['successful'] and  len(dict['data'])> 0:
                try:
                    list_data = db.get_one_sql(sql_select.format(number, user_id))
                    print '[******list_data*******]',sql_select.format(number, user_id)
                    if list_data :
                        for item in dict['data']:
                            db.run_insert_sql(sql_log.format(task_id, flow_id, item['sentence'], item['word'], item['key_word'],item['label'], item['similarity'], create_at))
                            print sql_log.format(task_id, flow_id, item['sentence'], item['word'], item['key_word'],params, item['similarity'], create_at)
                            if item['label'] in list_data.label:
                                print ' %s 在fs_consumer 的%s __ %s 中已经存在 '%(item['label'],number,user_id)
                                continue
                            else:
                                params = "{" + item['label'] + '}'
                                db.run_update_sql(sql_update.format(params, number, user_id))
                                print '-------fs_consumer----label  ------',sql_update.format(params, number, user_id)

                    else:
                        print 'fs_consumer  中不存在 %s 记录'%number
                except Exception as e :
                        logger.info('exception ****%s'%e)
        else:
            logger.info('.......httpClient error status : %s' % response.status)
    except Exception, e:
        logger.info('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()


channel.basic_consume(callback,queue=conf.MQ_QUEUE)
print '\n==============================================================\n'
print '               MQ_consume ....running.....                   '
print '\n==============================================================\n'
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
#
# if __name__ == '__main__':
#
#     sql = "select fs_call.task_id,replay.text from fs_call " \
#           "left join fs_call_replay as replay on fs_call.id = replay.call_id " \
#           "where fs_call.id = 28 and replay.who = 'human' ORDER BY  replay.create_at"
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
#     httpseverclient('23e566219595a9cb92bc3e5a175dbd63',list,'15900282168',10,8)




