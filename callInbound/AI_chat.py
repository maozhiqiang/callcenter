# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
reload(sys)
import httplib
import  urllib
import  json
import AI_config
'''
一、被动接口
1.http://api.aicyber.com/passive_chat
post请求
2.参数
名称                类型 说明
client_user_id      (str,客户端用户id)
app_id              (str,appid)
user_input          (str,用户问题)
secret  (先将app_id,key严格按照顺序串联，再进行md5加密 key:qwijfewopiherphsz)
3. 返回值


success (str,成功true,失败false)
msg (str,失败时错误信息)
data (Json,需要的数据)
'''

def passive_chat(user_input='你好'):
    params = {'client_user_id': AI_config.AI_userId, 'app_id': AI_config.AI_appid,'user_input':user_input,'secret':AI_config.AI_secret}

    httpClient = None
    result = ""
    try:
        params = json.dumps(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        httpClient = httplib.HTTPConnection("106.75.47.69", 80, timeout=30)
        httpClient.request("POST", "/passive_chat", params, headers)
        response = httpClient.getresponse()
        if response.status == 200:
            jsonStr = response.read()
            dict = json.loads(jsonStr)
            if (dict['successful']=='true'):
                obj = dict['data']
                result = obj['output']
        else:
            result = ""
            print '.......error.........'
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    print '..........AI Reslut......: %s '%(result)
    return  result

if __name__ == '__main__':
    passive_chat('')
