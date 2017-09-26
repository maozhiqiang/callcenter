# -*- encoding: utf-8 -*-

from flask import Flask
from flask import request
from callapi.common.utils import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbname:MrVg+X1ZwS4RiCh9@120.25.102.84:3306/db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/user/register', methods=['POST'])
@require('phone','password')
def customer_register():
    if request.method['GET']:
        print 'error'

    print  "wahaha"
    ss = "wahaha"
    return ss

if __name__ == '__main__':
    app.run()

