# -*- coding: UTF-8 -*-

import hashlib

def get_md5_value(src):
    if type(src) == unicode:
        src = src.encode('utf-8')
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def get_sha1_value(src):
    if type(src) == unicode:
        src = src.encode('utf-8')
    mySha1 = hashlib.sha1()
    mySha1.update(src)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest

if __name__ == '__main__':
    # str="1Lenovoqwijfewopiherphsz"

    str="QOROSqwijfewopiherphsz"
    # str="mytest"
    result_md5_value = get_md5_value(str)
    print 'MD5: ', result_md5_value

    str="测试开场白"
    str="测试挽回流程"
    str = '租金流程'
    result_md5_value = get_md5_value(str)
    print 'MD5: ', result_md5_value

