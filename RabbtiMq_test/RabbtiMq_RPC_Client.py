# -*- coding: utf-8 -*-
import pika
import uuid
import time

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response,  # 只要一收到消息就调用on_response
                                   no_ack=True,
                                   queue=self.callback_queue)  # 收这个queue的消息

    def on_response(self, ch, method, props, body):  # 必须四个参数
        # 如果收到的ID和本机生成的相同，则返回的结果就是我想要的指令返回的结果
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None  # 初始self.response为None
        self.corr_id = str(uuid.uuid4())  # 随机唯一字符串
        self.channel.basic_publish(
                exchange='',
                routing_key='rpc_queue',  # 发消息到rpc_queue
                properties=pika.BasicProperties(  # 消息持久化
                    reply_to = self.callback_queue,  # 让服务端命令结果返回到callback_queue
                    correlation_id = self.corr_id,  # 把随机uuid同时发给服务器
                ),
                body=str(n)
        )
        while self.response is None:  # 当没有数据，就一直循环
            # 启动后，on_response函数接到消息，self.response 值就不为空了
            self.connection.process_data_events()  # 非阻塞版的start_consuming()
            # print("no msg……")
            # time.sleep(0.5)
        # 收到消息就调用on_response
        return int(self.response)

if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    print(" [x] Requesting fib(7)")
    response = fibonacci_rpc.call(7)
    print(" [.] Got %r" % response)