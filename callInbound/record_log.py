# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import csv
import AI_config
import uuid
sys.path.append('..')
reload(sys)

starttime = datetime.datetime.now()

class RecordLogCLient:
    '''
    path: /tem/recordlog/appkey/file.log
    '''
    def __init__(self, appkey):
        self.__file = ''
        self.__appkey = appkey
        self.__path = '/home/callcenter/recordlog/'
        self.__filename = appkey+'.csv'
        self.isFileExists()

    def isFileExists(self):
        self.__file = os.path.join(self.__path, self.__appkey)
        print  '............self.__file : ',self.__file
        if not os.path.exists(self.__file):
            os.makedirs(self.__file)
            # f = open(self.__file+'/'+self.__filename, 'w')  # r只读，w可写，a追加
            with open(self.__file + '/' + self.__filename, 'w') as csvfile:
                writer = csv.writer(csvfile)
                # 先写入columns_name
                writer.writerow(["uid", "createTime", "ai_name", "call_id", "mark", "content"])
                # 写入多行用writerows
                # writer.writerows([[0, 1, 3], [1, 2, 3], [2, 3, 4]])
        else:
            print '..................self.path is exit..............',starttime

    def writeToCsv(self,data):
        with open(self.__file+'/'+self.__filename, "a") as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            # writer.writerow(["uid", "createTime","ai_name","call_id","mark","content"])
            # 写入多行用writerows
            writer.writerows([data])

# if __name__ == '__main__':
#     rc = RecordLogCLient('youer')
#
#     data = ['123123','asdads','212313','sdasda','1231231231321','asdasdad']
#     rc.writeToCsv(data)
#     name = "test_name"
#     namespace = "test_namespace"
#
#     print uuid.uuid1()  # 带参的方法参见Python Doc
#     print uuid.uuid3(uuid.NAMESPACE_DNS, name)
#     # print uuid.uuid4()
#     # print uuid.uuid5(namespace, name)