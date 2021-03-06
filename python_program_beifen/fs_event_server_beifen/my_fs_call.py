# -*-coding: utf-8 -*-

#from __future__ import print_function
import os
import ESL
import sys
import time
import signal
#from PsqlUtils import DBHelper
#from DBPool import Postgresql_Pool as db_pool
import DBhandler as db
from LogUtils import Logger

logger = Logger()
# db = DBHelper()
get_host_sql = "select * from fs_host"
get_call_sql = "select * from view_call_running"
get_free_line_sql = "select (line_num-line_use) as rec from fs_host where id ={0}"
chc_host_sql = "update fs_host set line_use = line_use + 1 where id = {0}"

#freeswitch 呼叫代理
class Proxy(object):
    def __init__(self, host):
        self.host_id = host[0]
        self.ip = str(host[2])
        self.port = host[3]
        self.area = host[1]
        self.passowrd = str(host[5])
        self.gateway = "sofia/gateway/gw1"
        self.line_max = host[6]
        self.conn = ESL.ESLconnection(self.ip, self.port, self.passowrd)
        conn_status = 'success' if self.conn.connected else 'fail'
        print('Connect fs host: %s at %s:%d，%s' % (self.passowrd, self.ip, self.port, conn_status))

    def call(self, item):
        task_id = item[3]
        call_id = item[0]
        uuid = str(item[2])
        number = str(item[1])
        is_success = self.fs_api(uuid=uuid, number=number, task_id=task_id, call_id=call_id,
                                 host_id=self.host_id, gateway=self.gateway)
        logger.info('[  call is_success = %s ]'%is_success)
        if is_success:
            db.update_sql(chc_host_sql.format(self.host_id))
        else:
            logger.info('self.bgapi.....retrun %s'%is_success)

    def fs_api(self, uuid, number, task_id, call_id, host_id, gateway):
        if not gateway:
            gateway = 'sofia/gateway/gw1'
        if self.conn.connected:
            # 设置通道变量task_id,call_id 处理挂断事件时，从task_id对应的队列中去掉uuid
            channel_vars = 'ignore_early_media=true,absolute_codec_string=g729,' \
                           'origination_uuid=%s,task_id=%s,call_id=%s,host_id=%s,is_test=%s' % \
                           (uuid, task_id, call_id, host_id, '1')
            command = "originate {%s}%s/%s &python(callappv2.Bot)" % (channel_vars, gateway, number)
            logger.info('Invoke fs api:\n%s' % command)
            self.conn.bgapi(command)
            return True
        else:
            return False

    #查询当前host可用线路数
    def can_use(self):
        if not self.conn.connected:
            return 'disconnect'
        num = db.get_one_sql(get_free_line_sql.format(self.host_id))
        if num <= 0:
            return 'full'
        return 'free'

# 呼叫管理
class CallManager(object):
    #初始化，加载host
    def __init__(self):
        self.proxy_factory = ProxyFactory()
    #执行轮询进程，获取要拨打的电话号码
    def process(self):
        list_call_number = db.get_all_sql(get_call_sql)
        for item in list_call_number:
            host_id = item[8]
            self.prepare_call(item,host_id)

    def prepare_call(self, item, host_id):
        res, pof = self.proxy_factory.get_proxy(host_id)
        if res == 'free':
            pof.call(item)
            return
        # res == 'fail' fs都断开了，或都线路满
        if pof == 'all_disconnect':
            # fs主机连接都断开了
            print('CallManager: ERROR! all fs host disconnect, start fs server or check host table.')
            time.sleep(2)
            sys.exit(0)
        elif pof == 'all_full':
            print('CallManager: WARN! all fs host line full, retry later...')

#代理工厂
class ProxyFactory(object):
    def __init__(self):
        self.proxy_list = []
        self.load_proxy()

    def load_proxy(self):
        list_host =db.get_all_sql(get_host_sql)
        for host in list_host:#循环 host列表
            proxy = Proxy(host)
            self.proxy_list.append(proxy)

    def get_proxy(self, host_id):
        ps = []
        for proxy in self.proxy_list:
            if host_id == proxy.host_id:
                status = proxy.can_use()
                ps.append(status)
                if status == 'free':
                    return 'free', proxy
        res = all([bool(s == 'disconnect') for s in ps])
        if res:
            return 'fail', 'all_disconnect'
        else:
            return 'fail', 'all_full'

def handler(signal_num, frame):
    print("\nCall service exit, wait a moment...")
    time.sleep(2)
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    manager = CallManager()
    while True:
        try:
            manager.process()
            time.sleep(2)
        except Exception as e:
            print('polling warnning!!! error:%s' %(e,))
