# -*-coding: utf-8 -*-
"""Freeswitch主机事件监听处理进程

1.对每台fs主机外呼调用，由run_call(只在web服务机器中运行)外呼进程依据host表中的fs主机配置，任务配额，发起外呼调用
2.此进程运行在各fs主机上，监听通道事件并处理，跟远程队列服务通信，及数据库访问
"""
import ESL
import atexit
import signal
import sys
import time
import Config as conf
import multiprocessing
from multiprocessing import managers
from DBPool import Postgresql_Pool as db_pool
from LogUtils import Logger

logger = Logger()

con = ESL.ESLconnection(conf.ESL_HOST, conf.ESL_PORT, conf.ESL_PWD)
_begin_time = time.time()
_pid = multiprocessing.current_process().pid
#atexit.register
def bye():
    sec = time.time() - _begin_time
    print 'bye, program run %d second.' % sec


cc_sql = "update fs_call set call_at = '{0}' where channal_uuid ='{1}'"

ca_sql = "update fs_call set answer_at = '{0}' where channal_uuid ='{1}'"

chc_sql = "update fs_call set call_status='{0}'," \
          " finish_at='{1}', channal_status='{2}'," \
          " channal_detail='{3}' " \
          "where channal_uuid='{4}'"

chc_host_sql = "update fs_host set line_use = line_use - 1 where id = {0}"


def event_processor(event_queue, task_queue):
    """事件处理进程，消费者"""
    while 1:
        # 读队列会阻塞进程
        event = event_queue.get()
        time_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info('.......event_processor.......''name: %s, uuid: %s' %
                    (event['event_name'], event['channal_uuid']))

        if event['event_name'] == 'CHANNEL_CREATE':
            sql = cc_sql.format(time_at, event['channal_uuid'])
            print '[sql]:........CHANNEL_CREATE........ %s'%sql
            runsql(sql)

        elif event['event_name'] == 'CHANNEL_ANSWER':
            sql = ca_sql.format(time_at, event['channal_uuid'])
            print '[sql]:.........CHANNEL_ANSWER...... %s' % sql
            runsql(sql)

        elif event['event_name'] == 'CHANNEL_HANGUP_COMPLETE':
            sql = chc_sql.format('finish', time_at, event['Channel-Call-State'],
                                 event['Hangup-Cause'], event['channal_uuid'])
            print '[sql]:..........CHANNEL_HANGUP_COMPLETE....... %s' % sql
            runsql(sql)
            task_id = event['task_id']
            host_id = event['host_id']
            print 'task_id....',task_id
            if task_id != None:
                try:
                    task_queue.remove(int(task_id), event['channal_uuid'])
                except Exception as e:
                    print e.message
                logger.info('-------is_test------%s  '%event['is_test'])
                if event['is_test'] and event['is_test'] != '0':
                    sql = chc_host_sql.format(int(host_id))
                    runsql(sql)
                HttpClientPost(event['channal_uuid'])

def runsql(sql):
   logger.info('[sql]....%s'%sql)
   try:
       conn = db_pool.getConn()
       cursor = conn.cursor()
       count = cursor.execute(sql, )
       conn.commit()
       db_pool.close(cursor, conn)
   except Exception as e:
       logger.info("  runsql ...except error %s"%e.message)

def HttpClientPost(channal_uuid):
    try:
        import urllib
        import urllib2
        url = conf.server_url
        req = urllib2.Request(url)
        data = {'channal_uuid': channal_uuid}
        data = urllib.urlencode(data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        logger.info('...............Bill result..... %s '%response.read())
        return response.read()
    except Exception as err:
        logger.error(" api/finance/bill/update/ .....error ...%s"%err)
        return None


def event_listener(event_queue):
    """事件监听进程，收到事件后将事件加入队列，生成者
    :param call_list:
    :return:
    """
    # standard_event = "CHANNEL_CREATE CHANNEL_ANSWER CHANNEL_HANGUP CHANNEL_HANGUP_COMPLETE"
    if con.connected:
        # print con.connected()
        # 只订阅通道事件
        con.events('plain', 'CHANNEL_CREATE CHANNEL_ANSWER CHANNEL_HANGUP_COMPLETE')
        while con.connected:
            # 等待接收事件会阻塞进程，不用time.sleep
            e = con.recvEvent()
            # logger.info("----------event---------%s" % e.serialize('json'))
            if e:
                # dict是python保留字，不要做变量名
                dct = dict()
                dct['event_name'] = e.getHeader("Event-Name")
                dct['channal_uuid'] = e.getHeader("unique-id")
                dct['call_number'] = e.getHeader("Caller-Destination-Number")
                dct['Channel-Call-State'] = e.getHeader("Channel-Call-State")

                if dct['event_name'] in ['CHANNEL_ANSWER', 'CHANNEL_HANGUP_COMPLETE']:
                    dct['call_id'] = e.getHeader("variable_call_id")
                    dct['is_test'] = e.getHeader("variable_is_test")
                    if dct['event_name'] == 'CHANNEL_HANGUP_COMPLETE':
                        dct['Hangup-Cause'] = e.getHeader("Hangup-Cause")
                        dct['task_id'] = e.getHeader("variable_task_id")
                        dct['host_id'] = e.getHeader("variable_host_id")
                if dct['channal_uuid'] == None:
                    continue
                event_queue.put(dct)
                logger.info('.......event_listener.......name: %s, uuid: %s, number: %s,task_id:' %
                            (dct['event_name'], dct['channal_uuid'], dct['call_number']))

    logger.error('.......esl connect error.......')
    sys.exit(-1)

def handler(signum, frame):
    pid = multiprocessing.current_process().pid
    if _pid == pid:
        print "\nsubprocess will exit, please wait..."

    # if pid == proc_call_sender.pid:
    #     # 子进程退出时，释放传参时代入的额外资源，如db connection pool
    #     pass
    #
    # if pid == proc_event_listener.pid:
    #     pass
    #
    # if pid == proc_event_processor.pid:
    #     pass

    time.sleep(2)
    sys.exit(-1)

signal.signal(signal.SIGINT, handler)

class QueueManager(managers.BaseManager):
    pass

if __name__ == '__main__':

    QueueManager.register('get_queue')
    # address, authkey 要与run_queue服务的一致
    m = QueueManager(address=('121.42.36.138', conf.queue_port), authkey=conf.queue_authkey)
    #本地
    # m = QueueManager(address=('0.0.0.0', 50000), authkey='aicyberqueue'.encode('utf-8'))
    # print m
    # 连接任务队列服务，远端先运行run_queue启动队列服务
    try:
        print('[%s  start connect to server queue %s...]' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),conf.queue_ip))
        m.connect()
        print '[%s  already connect queue... ]'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    except Exception as e:
        print e

        print 'Connect task queue service fail, exec run_queue first.'
        sys.exit(0)
    """
    run_call进程发起调用时，设置通道变量 task_id, call_id, host_id
      挂机时将uuid出队列，调用task_queue(task_id, uuid)，释放任务队列空间，当小于任务机器人配额时可被选中
      挂机时将fs_host表中，id=host_id 的记录 line_use-1，减少fs主机已用线数，当line_use<line_max时可被选中
    """
    task_queue = m.get_queue()

    # 事件队列，event_listener与event_processor共享
    manager = multiprocessing.Manager()
    event_queue = manager.Queue()

    proc_event_listener = multiprocessing.Process(
        target=event_listener, name='event_listener', args=(event_queue,))
    proc_event_listener.start()

    proc_event_processor = multiprocessing.Process(
        target=event_processor, name='event_processor', args=(event_queue, task_queue))
    proc_event_processor.start()

    # proc_call_sender.join()
    # proc_event_listener.join()
    # proc_event_processor.join()
    # flag = False
    # count = 0
    while True:
        time.sleep(3)
