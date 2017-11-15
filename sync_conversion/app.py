# -*- encoding: utf-8 -*-

import commands
from flask import Flask
app = Flask(__name__)
# app.config.from_object('config')
#app.config.from_object('yourapplication.default_settings')


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
'''
执行cmd命令 ，把16000wav 转MP3
sudo apt-get install lame
sudo apt-get install libsox-fmt-mp3
sudo apt-get install sox

'''
@app.route('/synconver/<filename>')
def sync_convertowav(filename):
    print  filename
    # arr = filename.split('.')
    # wavfilename = arr[0] + '.wav'
    # cmd = 'sox %s -r 8000 -c 1 %s'%(filename,wavfilename)
    # result =commands.getoutput("date")
    # print '.....result ......',result
    return 'User1212 %s' % filename
if __name__ == '__main__':
    app.run()