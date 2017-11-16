# coding=utf-8
import os
import DBhandler as dbs
import models.UserModel as User
import Config as config
#跨域
from flask_cors import CORS
from flask_login import  LoginManager, current_user, login_user, login_required
from flask import Flask, render_template, request, jsonify, send_from_directory,redirect, url_for
from werkzeug.utils import secure_filename

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/aicyber/resource/login'


app = Flask(__name__ ,template_folder='template',static_folder='', static_url_path='')
app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
CORS(app)


login_manager.init_app(app)
#====================================创建引擎===================================
engine = create_engine(config.MYSQL_SERVER_URI, encoding='utf8', max_overflow=5)
#====================================创建表单===================================
User.Base.metadata.create_all(engine)


FULL_AUDIO = None
path = '/home/callcenter/recordvoice/{0}/bot_audio'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['mp3', 'wav','png','jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
#====================================== 上传服务=================================
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

@app.route('/uploads/<flowId>/<filename>')
def uploaded_file(flowId,filename):
    template_ = 'http://121.42.31.97/recordvoice/{0}/bot_audio/'
    realypath = template_.format(flowId)
    print ' .... realypath ....%s'%realypath
    return send_from_directory(realypath, filename)

#=================================================ORM 服务===========================================================

@login_manager.user_loader    #使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def user_loader(id):          #这个id参数的值是在 login_user(user)中传入的 user 的 id 属性
    user = User.query.filter_by(id=id).first()
    return user
@app.route('/aicyber/resource/index',methods=['GET'])
def loginIndex():
    return render_template('login.html')

@app.route('/aicyber/resource')
def index2():
    return render_template('form.html')

def dictToObj(data_dict, obj):
    for key in data_dict.keys():
        if hasattr(obj, key):
            setattr(obj, key, data_dict[key])

@app.route('/aicyber/resource/login',methods=['POST'])
def appLogin():
    name = request.form.get('username')
    pwd = request.form.get('password')
    Session = sessionmaker(bind=engine)
    session = Session()
    if pwd == '123':
        user = User()
        return redirect(url_for('index2'))
    return redirect(url_for('loginIndex'))

@app.route('/aicyber/resource/api',methods=['POST'])
def run_sql_string():
    data = None
    if not request.json:
        return jsonify({'successful':False, 'message':'请求的数据格式不正确'})
    if request.method == 'POST':
        json_sqlString = request.json['sql_string']
        json_flg = request.json['flg']
        if json_flg == 'select_one':
            data = dbs.get_one_sql(json_sqlString)
        elif json_flg == 'select_all':
            data = dbs.get_all_sql(json_sqlString)
            # print 'data====',data
        elif json_flg == 'update':
            dbs.update_sql(json_sqlString)
        return jsonify({'success': True, 'message': u'成功响应', 'data': data})
    else:
        return jsonify({'success': False, 'message': u'请使用POST请求', 'data': None})





if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("8081"),debug=True)