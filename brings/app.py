# coding=utf-8
import os
from flask import g
import  DBhandler as db
from flask import request
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, jsonify,url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__ ,template_folder='template')
CORS(app)

FULL_AUDIO = None
path = '/home/callcenter/recordvoice/{0}/bot_audio'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['mp3', 'wav','png','jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<flowId>', methods=['POST'])
def upload(flowId):
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        upfails = []
        if len(flowId) == 0:
            return jsonify({'success': False, 'message': u'流程ID不能为空','data':None})
        wave_path =path.format(flowId)
        verify_path(wave_path)
        #http://121.42.31.97/recordvoice/899f04f0fef39dab0fbf975d171856d6/bot_audio/ed0e45ed55b552a978d655efc0fa2d31.wav
        template_ = 'http://121.42.36.138/recordvoice/{0}/bot_audio/{1}'
        print ' .... wave_path .... %s'%wave_path
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            if file and allowed_file(file.filename):
                #判断文件是否已存在
                if os.path.exists(os.path.join(wave_path, filename)):
                   print '..............remove............'
                   os.remove(os.path.join(wave_path, filename))
                file.save(os.path.join(wave_path, filename))
                realypath = template_.format(flowId,filename)
                print '.... realypath .... %s'%realypath
                filenames.append(realypath)
            else:
                upfails.append(filename)
        return_dict = {'success': True, 'msg': u'操作成功', 'data': {'filenames': filenames,'upfails':upfails}}
        return jsonify(return_dict)
    else:
        return jsonify({'success': False, 'message': u'请使用POST请求','data':None})

def verify_path( path):
    if not os.path.exists(path):
        os.makedirs(path)

@app.route('/aicyber/resource/')
def index2():
    return render_template('form.html')

@app.route('/aicyber/resource/api',methods=['POST'])
def run_sql_string():
    data = None
    if not request.json:
        return jsonify({'successful':False, 'message':'请求的数据格式不正确'})
    if request.method == 'POST':
        json_sqlString = request.json['sql_string']
        json_flg = request.json['flg']
        if json_flg == 'select_one':
            data = db.get_one_sql(json_sqlString)
        elif json_flg == 'select_all':
            data = db.get_all_sql(json_sqlString)
            # print 'data====',data
        elif json_flg == 'update':
            db.update_sql(json_sqlString)
        return jsonify({'success': True, 'message': u'成功响应', 'data': data})
    else:
        return jsonify({'success': False, 'message': u'请使用POST请求', 'data': None})



@app.route('/uploads/<flowId>/<filename>')
def uploaded_file(flowId,filename):
    template_ = 'http://121.42.31.97/recordvoice/{0}/bot_audio/'
    realypath = template_.format(flowId)
    print ' .... realypath ....%s'%realypath
    return send_from_directory(realypath, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("8081"),debug=True)