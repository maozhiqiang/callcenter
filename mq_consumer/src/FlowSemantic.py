#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-24 下午5:25
# @Author  : Arvin
# @Site    : 
# @File    : FlowSemantic.py
# @Software: PyCharm
import time
import json
import sys
import httplib
import Config as conf, DBHandler as db
from LogUtils import Logger


reload(sys)
sys.setdefaultencoding('utf-8')
logger = Logger()

def httpseverclient(flow_id,sentences,number,task_id,user_id):
    httpClient = None
    create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        values = {'flow_id': flow_id, 'sentences': sentences}
        print values
        params = json.dumps(values)
        headers = {"Content-type": "application/json"}
        httpClient = httplib.HTTPConnection(conf.flow_host, conf.flow_port, timeout=30)
        httpClient.request("POST", conf.flow_url, params, headers)
        response = httpClient.getresponse()
        if response.status == 200:
            jsonStr = response.read()
            dict = json.loads(jsonStr)
            logger.info('[ ==lables== %s ]'%dict)
            sql_select = "select * from fs_customer where number = '{0}' and user_id = {1}"
            sql_update = " update fs_customer set label = label || '{0}' where number = '{1}'  and user_id = {2} "
            sql_log = " insert into fs_customer_label_log(task_id,flow_id,user_input,user_word,key_word,label,similarity,create_at) values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\') RETURNING id"
            if dict['successful'] and  len(dict['data'])> 0:
                pass
                try:
                    for item in dict['data']:
                        list_data = db.get_one_sql(sql_select.format(number, user_id))
                        db.run_insert_sql(sql_log.format(task_id, flow_id, item['sentence'], item['word'], item['key_word'],item['label'], item['similarity'], create_at))
                        if list_data:
                            if item['label'] in list_data.label:
                                logger.info(' %s 在fs_consumer 的%s __ %s 中已经存在 '%(item['label'],number,user_id))
                                continue
                            else:
                                params = "{" + item['label'] + '}'
                                db.run_update_sql(sql_update.format(params, number, user_id))
                                logger.info('-------fs_consumer----label  ------%s'% sql_update.format(params, number, user_id))
                        else:
                            logger.info('fs_consumer  中不存在 %s 记录'%number)
                except Exception as e :
                        logger.info('exception ****%s'%e)
        else:
            logger.info('.......httpClient error status : %s' % response.status)
    except Exception, e:
        logger.info('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()
#'{"user_id": "66", "task_id": "101", "number": "18757421295", "call_id": "48053", "flow_id": "8edda3928db3fe07f5903a91811a6340", "mark": "statistical"}'
if __name__ == '__main__':

    sql = "select replay.text from fs_call " \
          "left join fs_call_replay as replay on fs_call.id = replay.call_id " \
          "where fs_call.id = {0} and replay.who = 'human' ORDER BY  replay.create_at".format('49285')
    result = db.get_all_sql(sql)
    sentences = []
    for item in result:
        print item.text
        sentences.append(item.text)
    # print  "sentences",sentences
    flow_id  = 'edfe111cb422699fd4cf5aba6e6ba671'
    task_id = '104'
    user_id = '86'
    number = '13012825520'
    httpseverclient(flow_id, sentences, number, task_id, user_id)
    # ss = db.get_one_sql("select * from fs_customer where number = '18757421295'")
    # print ss