# !/usr/bin/env python
# -*-coding: utf-8 -*-
import Config as conf
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import pika
from LogUtils import Logger
logger = Logger()

def rabbitmqClint(content):
    credentials = pika.PlainCredentials(conf.rabbitmq_user, conf.rabbit_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(conf.rabbitmq_server, 5672, '/', credentials))
    logger.info('-----rabbitmq ----send conent %s'%content)
    channel = connection.channel()
    channel.exchange_declare(exchange=conf.rabbtimq_exchange, exchange_type='direct')
    # 声明queue
    channel.queue_declare(queue=conf.rabbtimq_queue,durable=True)
    channel.queue_bind(exchange=conf.rabbtimq_exchange, queue=conf.rabbtimq_queue)
    print '[--------queue-------]',conf.rabbtimq_queue
    # n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    channel.basic_publish(exchange=conf.rabbtimq_exchange,
                          routing_key=conf.rabbtimq_queue,
                          body=content,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          )
                          )
    # print(" [x] Sent '%s' "%content)
    connection.close()
# if __name__ == '__main__':
#     sql = 'INSERT INTO fs_call_replay(who, text, record_fpath,  call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'.format(
#             45, 454, 454, 454, 4545, 4545)
#     rabbitmqClint(sql)
#     pass