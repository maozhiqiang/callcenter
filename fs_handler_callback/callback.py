#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-23 下午2:46
# @Author  : Arvin
# @Site    : 
# @File    : callback.py
# @Software: PyCharm

import time
import json
import urllib2
import datetime
from datetime import date
import Config as conf
import DBhandler as db
from LogUtils import Logger
logger = Logger()
#-----------------------fs_handler_callback---------------------------------------

fs_callback_sql =  " select * from fs_call where channal_uuid ='{0}' "
fs_callback_sqllist = " select who,text,record_fpath,create_at from fs_call_replay  where call_id = {0} ORDER BY create_at "

fs_callback_host = " select * from fs_user where id  =  {0} "

fs_update_call_callback = "update fs_call set is_callback = {0} , callback_ct = callback_ct + 1  ,callback_at = '{1}'  where channal_uuid = '{2}' "

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj,time):
            return obj.strftime("%H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

class call_api(object):
    def __init__(self,uuid,user_id,call_id):
        self.data_obj = {}
        self.success = True
        self.callback_url = None
        self.error = None
        self.call_info = None
        self.item_info = None
        self.channal_uuid = uuid
        self.user_id = user_id
        self.call_id = call_id
        self.get_callback_url()

    # 拿call 信息
    def get_call_data(self):
        try:
            ss_sql = fs_callback_sql.format(self.channal_uuid)
            call_info = db.get_one_sql(ss_sql)
            return call_info
        except Exception as e:
            self.success = False
            print 'callback_sql1 error .....%s' % e.message
            self.error = 'sql except %s ' % e.message

    # 拿replay 分段信息
    def get_replay_data(self):
        try:
            item_sql = fs_callback_sqllist.format(self.call_id)
            item_info = db.get_all_sql(item_sql)
            for item in item_info:
                if item['record_fpath'] !="":
                    # print '...回放声音的全路径： ',ss
                    item['record_fpath'] = conf.playbaclaudio + item['record_fpath']
            # logger.info(item_info)
            return  item_info
        except Exception as e:
            self.success = False
            print 'callback_sql2 error .....%s' % e.message
            self.error = 'sql except %s ' % e.message

    # 拿host callback_url信息
    def get_callback_url(self):
        try:
            host_sql = fs_callback_host.format(self.user_id)
            host_info = db.get_one_sql(host_sql)
            # print '[ ------3-`-------%s ]' % host_info
            self.callback_url = host_info['callback_url']
        except Exception as e:
            self.uccess = False
            print 'callback_sql3 error .....%s' % e.message
            self.error = 'sql except %s ' % e.message
    #处理回调
    def call_back_process(self):
        call_info = self.get_call_data()
        item_info = self.get_replay_data()
        params = {"call": call_info, "call_item": item_info}
        self.data_obj['success'] = self.success
        self.data_obj['data'] = params
        self.data_obj['error'] = self.error
        logger.info('body_data------->%s' % json.dumps(self.data_obj, cls=DateEncoder))
        time_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            req = urllib2.Request(self.callback_url, json.dumps(self.data_obj, cls=DateEncoder))  # 需要是json格式的参数
            req.add_header('Content-Type', 'application/json')  # 要非常注意这行代码的写法
            response = urllib2.urlopen(req)
            result = json.loads(response.read())
            print result
            print '[------result -----]', result['status']
            if result['status'] == 0:
                update_sql = fs_update_call_callback.format(True, time_at, self.channal_uuid)
                logger.info('[ ------- sql_update_callback ------- is %s]' % update_sql)
                db.update_sql(update_sql)
            else:
                update_sql = fs_update_call_callback.format(False, time_at, self.channal_uuid)
                logger.info('[ ------- sql_update_callback ------- is %s]' % update_sql)
                db.update_sql(update_sql)
        except Exception, e:
            print e

if __name__ == '__main__':

    callback = call_api('371c6fc6-fd12-4533-b2bf-e3eed81a16d6',3,1)
    callback.call_back_process()