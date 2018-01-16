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

    str="MOBIKE94818577406qwijfewopiherphsz"
    str="mytest"
    str = '读十九大报告你有什么感悟？未来五年你给自己树立了哪些小目标？“十九大回声”专题我们采访了一系列人群一起来读读他们的十九大笔记看看他们未来五年的梦想是什么？吴书香“85后”村党支部第一书记吴书香在展示'
    result_md5_value = get_md5_value(str)
    print 'MD5: ', result_md5_value

    # str="测试开场白"
    # str="测试挽回流程"
    # result_md5_value = get_md5_value(str)
    # print 'MD5: ', result_md5_value

