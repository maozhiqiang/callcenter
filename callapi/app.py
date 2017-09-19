# -*- encoding: utf-8 -*-

from utils import *

from flask import Flask


app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/user/register', methods=['POST'])
@require('phone','password')
def customer_register():
    print  "wahaha"
    ss = "wahaha"
    return ss

if __name__ == '__main__':
    app.run()

