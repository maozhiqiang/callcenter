#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-12 下午4:09
# @Author  : Arvin
# @Site    : 
# @File    : MQClient.py
# @Software: PyCharm
#rabbtimq_exchange = 'callexchange'
import json
import pika

class MQConstant():
    MQ_NAME = 'admin'
    MQ_PWD = '123123'
    MQ_EXCHANGE = 'callexchange'
    MQ_QUEUE = 'durable'
    MQ_HOST = '127.0.0.1'
    MQ_PORT = 5672

class MQHandler(object):
    def __init__(self,username,password,host,port,exchange,rout_key):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.exchange = exchange
        self.rout_key = rout_key
        self.content_type = 'application/json'

    def get_conn(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        print '----%s------%s---'%(self.host,self.port)

        conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port, '/', credentials))
        print conn
        return conn

    def get_channel(self):
        channel = self.get_conn().channel()
        channel.exchange_declare(exchange=self.exchange,type='direct')
        channel.queue_declare(queue=self.rout_key,durable=True)
        channel.queue_bind(exchange=self.exchange, queue=self.rout_key)
        return channel

    def close_conn(self):
        self.get_conn().close()

    def publish(self, ms_data):
        self.get_channel().basic_publish(
            exchange=self.exchange,
            routing_key=self.rout_key,
            body=json.dumps(ms_data),
            properties=pika.BasicProperties(content_type=self.content_type)
        )
        self.close_conn()
mq = MQHandler(MQConstant.MQ_NAME,MQConstant.MQ_PWD,MQConstant.MQ_HOST,MQConstant.MQ_PORT,MQConstant.MQ_EXCHANGE,MQConstant.MQ_QUEUE)
if __name__ == '__main__':
    # mq = MQHandler(MQConstant.MQ_NAME,MQConstant.MQ_PWD,MQConstant.MQ_HOST,MQConstant.MQ_PORT,MQConstant.MQ_EXCHANGE,MQConstant.MQ_QUEUE)
    data = {}
    data['mark'] = 'sql_insert'
    data['sql_str'] = 'select * from fs_call'
    mq.publish(data)

