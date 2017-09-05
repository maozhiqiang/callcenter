#!/Users/mxb/workspace/pyenvs/call/bin/python
# -*-coding: utf-8 -*-

import atexit
import multiprocessing
import signal
import sys
import time
import ESL
from LogUtils import Logger
from psqlhelper import DBHelper

logger = Logger()

con = ESL.ESLconnection('0.0.0.0', 8021, 'Aicyber')
_begin_time = time.time()
_pid = multiprocessing.current_process().pid
print '[ %s  ESL connection is %s  ] '%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),con.connected())
@atexit.register
def bye():
    sec = time.time() - _begin_time
    print 'bye, program run %d second.' % sec

def event_processor(event_queue):
    """事件处理进程，消费者"""
    while 1:
        db = DBHelper()
        time_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = event_queue.get()
        event_name = event['event_name']
        uuid = event['channal_uuid']
        Hangup_Cause = event['Hangup-Cause']
        state = event['Channel-Call-State']
        if event_name in ['CHANNEL_CREATE']:
            sql = "update fs_call set call_at = '{0}' where channal_uuid ='{1}'".format(time_at,uuid)
            logger.info('==============CHANNEL_CREATE sql===============\n : %s'%sql)
            db.runsql(sql)

        if event_name in ['CHANNEL_ANSWER']:
            sql = "update fs_call set answer_at = '{0}' where channal_uuid ='{1}'".format(time_at,uuid)
            logger.info('==============CHANNEL_ANSWER sql :==============-\n %s' % sql)
            db.runsql(sql)

        if event_name in ['CHANNEL_HANGUP']:
            print 'name.....%s' % event_name

        if event_name in ['CHANNEL_HANGUP_COMPLETE']:
            updatesql = "update fs_call set    call_status='{0}' ,finish_at='{1}',channal_status='{2}' ,channal_detail = '{3}'  where channal_uuid='{4}'".format(
                'finish', time_at, state, Hangup_Cause, uuid)
            logger.info('==============CHANNEL_HANGUP_COMPLETE sql==============:\n %s' % updatesql)
            db.runsql(updatesql)

        logger.info('event_processor: consume event %s from event_queue' % event)
        time.sleep(.5)

def event_listener(call_list, event_queue):
    """事件监听进程，收到事件后将事件加入队列，生成者
    :param call_list:
    :return:
    """
    standard_event = "CHANNEL_CREATE CHANNEL_ANSWER  CHANNEL_HANGUP CHANNEL_HANGUP_COMPLETE "
    if con.connected:
        con.events('plain', 'all')
        while 1:
            e = con.recvEvent()
            if e:
                event_name = e.getHeader("Event-Name")
                if event_name in standard_event:
                    dict = {}
                    dict['event_name'] = e.getHeader("Event-Name")
                    dict['channal_uuid'] = e.getHeader("unique-id")
                    dict['call_number'] = e.getHeader("Caller-Destination-Number")
                    dict['Channel-Call-State'] = e.getHeader("Channel-Call-State")
                    dict['Hangup-Cause'] = e.getHeader("Hangup-Cause")
                    event_queue.put(dict)
                    uuid = e.getHeader("unique-id")
                    logger.info('.......event_listener.......uuid.....%s'%uuid)
            time.sleep(.5)
    else:
        logger.error('.......esl connect error.......')
        sys.exit(-1)

def call_sender(call_list, call_size):
    """呼叫发起进程，len(call_list)<call_size 时从call表里取号外呼
    :param call_list 本进程与 event_listener 进程共享的呼叫列表，存channal_uuid
    :param call_list
    """
    db = DBHelper()
    while True:
        try:
            if len(call_list) < call_size:
                call_free = call_size - len(call_list)
                uuid_list = db.get_call_channal_uuid(call_free)
            for i in range(min(call_free, len(uuid_list))):
                # 从call表中取call_free条run的记录，发起外呼，并将uuid存入call_list
                uuid = uuid_list.pop()
                #根据uuid　查找电话，并判断当前状态
                object  = db.get_number_callStatus(uuid[0])
                logger.info("Prepare call %s....%s"%(uuid[0],object))
                if object is not None:
                    number = object[0]
                    status = object[1]
                    if cmp(status,'run')==0:
                        call_list.append(uuid[0])
                        call_outbound(uuid[0],number)
                        logger.info('call_sender: append %s to call' % uuid[0])
        except Exception as e:
            logger.error(e.message)

        time.sleep(.5)

def call_outbound(uuid,number):
    db = DBHelper()
    # Run command
    if con.connected:
        try:
            command = "originate {ignore_early_media=true,absolute_codec_string=pcma,origination_uuid=%s}sofia/gateway/gw1/%s &python(callappv2.Bot)" % (
                uuid, number)
            logger.info('command:%s'%command) ,
            con.api(command)
            logger.info('run update  sql to status ')
            db.updateTocallstatus(uuid)
        except Exception as e:
            logger.error(e.message)
    else:
        sys.exit(-1)

def HttpClientPost(channal_uuid):
    import  urllib2,urllib
    try:
        url = 'http://192.168.0.183:8000/api/finance/bill/update/'
        req = urllib2.Request(url)
        data = {'channal_uuid': channal_uuid}
        data = urllib.urlencode(data)
        # enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        logger.info('...............Bill result..... %s '%response.read())
        return response.read()
    except Exception as err:
        logger.error(" HttpClientPost .....error ...%s"%err)
        return None

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

if __name__ == '__main__':

    manager = multiprocessing.Manager()
    # 呼叫列表大小
    call_size = 5
    # 呼叫列表，存channel_uuid，call_sender与event_listener共享
    call_list = manager.list()
    # 事件队列，event_listener与event_processor共享
    event_queue = manager.Queue()

    proc_call_sender = multiprocessing.Process(
        target=call_sender, name='call_sender', args=(call_list, call_size))
    proc_call_sender.start()

    proc_event_listener = multiprocessing.Process(
        target=event_listener, name='event_listener', args=(call_list, event_queue))
    proc_event_listener.start()

    proc_event_processor = multiprocessing.Process(
        target=event_processor, name='event_processor', args=(event_queue,))
    proc_event_processor.start()

    # proc_call_sender.join()
    # proc_event_listener.join()
    # proc_event_processor.join()
    count = 0
    flag = False
    while True:
        time.sleep(3)
