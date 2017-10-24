# -*-coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import signal
import time
import django

from multiprocessing import managers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "call.settings")
django.setup()

import ESL
from django.db import transaction
from src.task.models import Call, ViewCallRun
from src.sysinfo.models import Host
from src.finance.utils import get_account_minute_by_task

import logging
import logging.handlers


LOG_FILE = 'tst.log'


class ESLDummy(object):
    connected = True


class Proxy(object):
    """ESL客户端代理
    根据配置生成esl客户端，负载对fs服务器外呼调用
    呼叫时由主机配置的网关呼出，每台fs主机启动fs_event事件监听及处理进程
    """

    def __init__(self, host):
        self.host_id = host.id
        self.ip = str(host.ip)
        self.port = host.port
        self.area = host.city
        # print ('-*-*-*-*-*-'+self.area)
        self.passowrd = str(host.relay_password)
        self.gateway = "sofia/gateway/gw1"
        self.line_max = host.line_num
        # self.conn = ESLDummy()  # dummy
        self.conn = ESL.ESLconnection(self.ip, self.port, self.passowrd)
        # todo host.line_use = 0 重启后主机已用线数设置为 0
        conn_status = 'success' if self.conn.connected else 'fail'
        # print(self.host_id, self.ip, self.port, self.passowrd, self.gateway, self.line_max)
        print('Connect fs host: %s at %s:%d，%s' % (self.passowrd, self.ip, self.port, conn_status))

    def call(self, item, task_queue):
        print ('to call............')
        task_id = item.task_id
        call_id = item.id
        uuid = str(item.channal_uuid)
        number = str(item.cust_number)

        is_success = self.fs_api(uuid=uuid, number=number, task_id=task_id, call_id=call_id,
                                 host_id=self.host_id, gateway=self.gateway)

        print ('call is_success=', is_success)
        if is_success:
            # 更新call状态
            item.call_status = 'running'
            item.save()
            # 调用任务队列服务接口，添加uuid到task_id的队列
            task_queue.add(task_id, uuid)
            # 修改主机已用线数，有并发访问加行锁
            host = Host.objects.select_for_update().get(pk=self.host_id)
            host.line_use += 1
            host.save()

    def fs_api(self, uuid, number, task_id, call_id, host_id, gateway):
        if not gateway:
            gateway = 'sofia/gateway/gw1'
        if self.conn.connected:
            # 设置通道变量task_id,call_id 处理挂断事件时，从task_id对应的队列中去掉uuid
            channel_vars = 'ignore_early_media=true,' \
                           'origination_uuid=%s,task_id=%s,call_id=%s,host_id=%s,is_test=%s' % \
                           (uuid, task_id, call_id, host_id, '1')
            command = "originate {%s}%s/%s &python(callappv2.Bot)" % (channel_vars, gateway, number)
            # logger.info('command:%s' % command),
            print('Invoke fs api:\n%s' % command)
            self.conn.bgapi(command)
            return True
        else:
            return False

    def can_use(self):
        if not self.conn.connected:
            return 'disconnect'
        host = Host.objects.select_for_update().get(id=self.host_id)
        if host.line_use >= self.line_max:
            return 'full'
        return 'free'


class ProxyFactory(object):
    def __init__(self):
        self.proxy_list = []
        self.load_proxy()

    def load_proxy(self):
        for host in Host.objects.all():
            proxy = Proxy(host)
            self.proxy_list.append(proxy)

    def get_proxy(self, area):
        ps = []
        for proxy in self.proxy_list:
            if area == proxy.area:
                status = proxy.can_use()
                ps.append(status)
                if status == 'free':
                    return 'free', proxy
        res = all([bool(s == 'disconnect') for s in ps])
        if res:
            return 'fail', 'all_disconnect'
        else:
            return 'fail', 'all_full'


class CallManager(object):
    """呼叫管理
    根据任务队列，分布式调用各fs服务器进行外呼"""

    def __init__(self, queue):
        self.proxy_factory = ProxyFactory()
        self.task_queue = queue

    def process(self):
        """查询任务中的待呼号码，任务队列未满时进队，选fs机器集群中的一台外呼"""
        for cr in ViewCallRun.objects.all():
            # 任务已用呼叫数
            print ('........task_id=',cr.task_id)
            call_use = self.task_queue.size(cr.task_id)
            # 加入任务呼叫数
            call_add = min(cr.task_bot_count - call_use, cr.call_run_count)
            call_minute = get_account_minute_by_task(task_id=cr.task_id)
            if call_add > call_minute:
                print ('call_minute < call_at........')
                return
            if call_add <= 0:
                print('CallManager: queue of task_id = %d is full.' % (cr.task_id,))
                continue
            print('CallManager: add %d call to queue of task_id = %d.' % (call_add, cr.task_id))

            with transaction.atomic():
                # 把fs_call，fs_host的更新做事务处理
                items = Call.objects.select_for_update().filter(task_id=cr.task_id, call_status='run')[:call_add]
                for item in items:
                    self.prepare_call(item, cr.task_area)

    def prepare_call(self, item, area):
        """选择一个可用的fs主机，发起外呼"""
        res, pof = self.proxy_factory.get_proxy(area)
        if res == 'free':
            pof.call(item, self.task_queue)
            return
        # res == 'fail' fs都断开了，或都线路满
        if pof == 'all_disconnect':
            # fs主机连接都断开了
            print('CallManager: ERROR! all fs host disconnect, start fs server or check host table.')
            time.sleep(2)
            sys.exit(0)
        elif pof == 'all_full':
            print('CallManager: WARN! all fs host line full, retry later...')


class QueueManager(managers.BaseManager):
    pass


def handler(signal_num, frame):
    print("\nCall service exit, wait a moment...")
    time.sleep(2)
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':

    QueueManager.register('get_queue')
    # m = QueueManager(address=('127.0.0.1', 50000), authkey='aicyberqueue')
    m = QueueManager(address=('10.165.51.223', 50000), authkey='aicyberqueue')

    # 连接任务队列服务，先运行run_queue.py
    try:
        m.connect()
        print ('connect....')
    except Exception:
        print('Connect task queue service fail, exec run_queue first.')
        sys.exit(0)

    queue = m.get_queue()
    print('Connect task queue service success, will connect fs host.')

    manager = CallManager(queue)
    while True:
        try:
            manager.process()
            time.sleep(2)
        except Exception as e:
            print('polling warnning!!! error:%s' %(e,))
