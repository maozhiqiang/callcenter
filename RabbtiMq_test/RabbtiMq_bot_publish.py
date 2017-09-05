# -*- coding: utf-8 -*-

import pika
import json
import time

#消息发送端口
class RabbitMqPublishClient(object):

    def __init__(self,amqp_url):
        self._url = amqp_url


    def publish(self,db_msg):
        params = pika.URLParameters(self._url)
        conn = pika.BlockingConnection(parameters=params)
        chan_db = conn.channel()

        chan_db.exchange_declare(exchange='call.esl', exchange_type='direct', durable=True)

        # db_msg = {'op': 'add_reply', 'data': {'call_id': 10, 'path': '/path/to'}}

        # 发布db写消息
        chan_db.basic_publish(
            exchange='call.esl',
            routing_key='esl.db',
            body=json.dumps(db_msg),
            properties=pika.BasicProperties(content_type='application/json')
        )

pub =RabbitMqPublishClient('amqp://call_user:123456@127.0.0.1:5672/call?heartbeat_interval=30')
if __name__ == '__main__':
    db_msg = {'op': 'add_reply', 'data': {'call_id': 10, 'path': '/path/to'}}
    pub.publish(db_msg)


