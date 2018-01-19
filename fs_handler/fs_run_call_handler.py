# -*-coding: utf-8 -*-

import os
import ESL
import sys
import time
import signal
import DBhandler as db
from LogUtils import Logger

logger = Logger()
get_host_sql = " select * from fs_host  where state in [1,2] "
get_call_sql = " select * from view_call_running "
get_free_line_sql = " select (line_num-line_use) as rec from fs_host where id ={0} "
chc_host_sql = " update fs_host set line_use = line_use + 1 where id = {0}"
update_call_sql = " update fs_call set call_status = 'trying' , queue_at = '{0}'  where channal_uuid = '{1}' "
ahq_host_sql = " select * from fs_host where id = {0}  and  state in (1,2) "

# 呼叫管理
class CallManager(object):
    #初始化，加载host
    def __init__(self):
        self.list_num = 0
        self.flg = True
    #执行轮询进程，获取要拨打的电话号码
    def process(self):
        if self.flg:
            list_call_number = db.get_all_sql(get_call_sql)
            time_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.list_num = len(list_call_number)
            if len(list_call_number) > 0:
                self.flg = False
                logger.debug('[ %s   list_call_number count is ....%s.....flg....%s]'%(time_at,self.list_num,self.flg))
            for item in list_call_number:
                self.list_num = self.list_num-1
                print ('[ for in -- self.list_num is ].....%s'%self.list_num)
                host_id = item.host_id
                self.prepare_call(item,host_id)
            self.flg = True

    def prepare_call(self, item, host_id):
        #这里修改成 每次根据host_id 查询host数据,判断线路是否可用
        host = db.get_one_sql(ahq_host_sql.format(host_id))
        if host:
            conn = ESL.ESLconnection(host.gateway_ip, 8021, 'Aicyber')
            if conn.connected():
                num = db.get_one_sql(get_free_line_sql.format(host_id))
                if num <=0:#没有可用线路数
                    logger.info('没有可用线路了excute [sql]: %s __ rresult: %s]\n\n'%(get_free_line_sql.format(host_id),num))
                    return False
                else:#有富余线路数,执行拨打电话
                    self.calling(item,host,conn)
            else:
                conn_status = 'success' if conn.connected() else 'fail'
                print('Connect fs host: %s:%d  status = %s' % (host.gateway_ip, 8021, conn_status))

    def calling(self, item,host,conn):
        if not host.gateway_name:
            gateway = 'sofia/gateway/gw1'
        else:
            gateway = 'sofia/gateway/{0}'.format(host.gateway_name)
        if conn.connected:
            channel_vars = 'ignore_early_media=true,absolute_codec_string=g729,' \
                           'origination_uuid=%s,task_id=%s,flow_id=%s,call_back=false,call_id=%s,host_id=%s,is_test=%s,user_id=%s' % \
                           (str(item.channal_uuid),item.task_id, str(item.flow_id),item.id,host.id, '1',item.user_id)
            logger.info('[-------is_interrupt: %s----]' % item.is_interrupt)
            if item.is_interrupt:
                command = "originate {%s}%s/%s &python(callappv3.Bot)" % (channel_vars, gateway, str(item.cust_number))
            else:
                command = "originate {%s}%s/%s &python(callappv2.Bot)" % (channel_vars, gateway, str(item.cust_number))
            logger.error('\n\n Invoke fs api:\n%s  \n\n' % command)
            ss = conn.bgapi(command)
            logger.info('***bgapi return ** %s\n\n'% ss.serialize('json'))
            try:
               time_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
               db.update_sql(update_call_sql.format(time_at,str(item.channal_uuid)))
            except Exception as e:
               print 'eror',e.message
            return True
        else:
            return False

def handler(signal_num, frame):
    print("\nCall service exit, wait a moment...")
    time.sleep(2)
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    manager = CallManager()
    print '             [ start fs_run_call........]'
    while True:
        try:
            manager.process()
            time.sleep(2)
        except Exception as e:
            print('polling warnning!!! error:%s' %(e,))
