#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth : pangguoping
# 消费者
import pika

credentials = pika.PlainCredentials('admin', '123123')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672,'/',credentials))
channel = connection.channel()
# 定义exchange和类型
channel.exchange_declare(exchange='direct_test',
                         type='direct')

# 生成随机队列
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
severities = ['error', 'info']
# 将随机队列与routing_key关键字以及exchange进行绑定
for severity in severities:
    channel.queue_bind(exchange='direct_test',
                       queue=queue_name,
                       routing_key=severity)
print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


# 接收消息
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()