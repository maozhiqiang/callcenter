#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-29 上午10:53
# @Author  : Arvin
# @Site    : 
# @File    : MQ_consume.py
# @Software: PyCharm

import sys
import json
import sys
import sys
import pika
import httplib
from mq_consumer.src import Config as conf, DBHandler as db
from mq_consumer.src.LogUtils import Logger

reload(sys)
sys.setdefaultencoding('utf-8')
logger = Logger()

credentials = pika.PlainCredentials(conf.MQ_USERNAME,conf.MQ_PWD)
connection = pika.BlockingConnection(pika.ConnectionParameters(conf.MQ_URL,5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='callexchange', exchange_type='direct')
channel.queue_declare(queue='call_api',durable=True)
channel.queue_bind(exchange='callexchange', queue='call_api')

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

    else:
        sql = "update fs_call set full_record_fpath ='{0}' where channal_uuid ='{1}'".format(dict['record_fpath'],dict['channal_uuid'] )
        db.run_update_sql(sql)
        logger.info('run_update_sql.....%s' % sql)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def httpseverclient(flow_id,sentences):
    httpClient = None
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
            logger.info('Flow return ----------%s' % dict)
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
