# -*-coding: utf-8 -*-

import functools
import flask
from functools import wraps
from functools import wraps
from flask import make_response
from flask import g, request, redirect, url_for

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

#缓存服务器
def cached(timeout=5 * 60, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator
"""
This is a python style.
 
@参数验证
eg:
@require('phone','password')
"""
def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in required_args:
                print  request.json
                if not request.json :
                    return flask.jsonify(code=401, msg='请用json格式')
                if arg not in request.json:
                    return flask.jsonify(code=400, msg='参数不正确')
            return func(*args, **kw)
        return wrapper
    return decorator
#允许跨域
'''
eg:
    @app.route('/hosts/')
    @allow_cross_domain
    def domains():
        pass
'''
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
'''
object to  json 

'''

def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    json = {}
    # json['fields'] = {}
    # json['pk'] = getattr(model, 'id')
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        # json['fields'][col.name] = getattr(model, col.name)
        json[col.name] = getattr(model, col.name)
    # return dumps([json])
    return json

if __name__ == '__main__':
    rv = cache.get('my-item')
    print rv
