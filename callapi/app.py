# -*- encoding: utf-8 -*-
import base64
import config
from flask import Flask,jsonify,request
from callapi.handler import WebAPI as xunfei_asr
from callapi.handler import  FlowHandler as flow
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbname:MrVg+X1ZwS4RiCh9@120.25.102.84:3306/db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World'

# @app.route('/user/register', methods=['POST'])
# @require('phone','password')
# def customer_register():
#     if request.method['GET']:
#         print 'error'
#
#     print  "wahaha"
#     ss = "wahaha"
#     return ss

#上传分段录音，返回分段录音语音识别结果 and  分段录音存储的路径
@app.route('/call/api/upload/asr/', methods=['POST','GET'])
def upload_asr():
    if request.method == 'POST':
        if not request.json :
            return jsonify({'success':False, 'message':u'请求的数据格式不正确'})
        if 'filename' not in request.json or 'wavedata' not in request.json:
            return jsonify({'success':False, 'message':u'请求的数据参数不正确'})
        filename = request.json['filename']
        wavedata = request.json['wavedata']
        data = base64.b64decode(wavedata)
        file = config.SUB_VOICE % filename
        with open(file, 'wb') as f:
            f.write(data)
        print 'filename is %s  ' % filename
        try:
            url_v = config.URL_V+file
            resultInfo = xunfei_asr.vc.getText(file)
            resultInfo['url_v'] = url_v
            return_dict = {'success': True, 'msg': u'操作成功', 'data': resultInfo}
        except Exception as e:
            return_dict = {'success': False, 'msg': u'asr error', 'data': None}
            print e.message
        return jsonify(return_dict)
    else:
        return jsonify({'success': False, 'message': '请使用POST请求'})

#上传全程录音文件，返回录音文件所在目录
@app.route('/call/api/upload/full/',methods=['POST','GET'])
def upload_full_voice():
    if request.method == 'POST':
        if not request.json:
            return jsonify({'success': False, 'message': u'请求的数据格式不正确'})
        if 'filename' not in request.json or 'wavedata' not in request.json:
            return jsonify({'success': False, 'message': u'请求的数据参数不正确'})
        filename = request.json['filename']
        wavedata = request.json['wavedata']
        data = base64.b64decode(wavedata)
        file = config.FULL_VOICE % filename
        with open(file, 'wb') as f:
            f.write(data)
        print 'filename is %s  ' % filename
        url_v = config.FULL_VOICE + file
        return_dict = {'success': True, 'msg': u'操作成功', 'data': {'url_v':url_v}}
        return jsonify(return_dict)
    else:
        return jsonify({'success': False, 'message': u'请使用POST请求'})
#流程接口
@app.route('/call/api/flow/start/',methods={'POST','GET'})
def flow_api():
    if request.method == 'POST':
        if not request.json:
            return jsonify({'success': False, 'message': u'请求的数据格式不正确'})
        if 'user_Input' not in request.json or 'userId' not in request.json or 'flowId' not in request.json:
            return jsonify({'success': False, 'message': u'请求的数据参数不正确'})
        user_Input = request.json['user_Input']
        userId = request.json['userId']
        flowId = request.json['flowId']
        try:
            resultInfo = flow.flowHandler(user_Input, userId, flowId)
        except Exception as e:
            resultInfo = None
            print 'flow error :%s' % e.message
        return_dict = {'success': True, 'msg': u'操作成功', 'data': resultInfo}
        return  jsonify(return_dict)
    else:
        return jsonify({'success': False, 'message': u'请使用POST请求'})

@app.route('/call/api/flow/closed',methods=['POST','GET'])
def closedFlow():
    if request.method == 'POST':
        if not request.json:
            return jsonify({'success': False, 'message': u'请求的数据格式不正确'})
        if 'userId' not in request.json or 'flowId' not in request.json:
            return jsonify({'success': False, 'message': u'请求的数据参数不正确'})
        userId = request.json['userId']
        flowId = request.json['flowId']
        try:
            resultInfo = flow.closeFlow( userId, flowId)
        except Exception as e:
            resultInfo = None
            print 'flow error :%s' % e.message
        return_dict = {'success': True, 'msg': u'操作成功', 'data': resultInfo}
        return  jsonify(return_dict)
    else:
        return jsonify({'success': False, 'message': '请使用POST请求'})

if __name__ == '__main__':
    app.run()


