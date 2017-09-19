# -*-coding: utf-8 -*-

import functools
import flask
from functools import wraps
from functools import wraps
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

def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in required_args:
                if arg not in request.json:
                    return flask.jsonify(code=400, msg='参数不正确')
            return func(*args, **kw)
        return wrapper
    return decorator


if __name__ == '__main__':
    rv = cache.get('my-item')
    print rv
