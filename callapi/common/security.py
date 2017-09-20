# -*-coding: utf-8 -*-
import  hashlib
#md5加盐加密
def _hashed_with_salt(info, salt):
    m = hashlib.md5()
    m.update(info.encode('utf-8'))
    m.update(salt)
    return m.hexdigest()

#对登录密码进行加密
def hashed_login_pwd(pwd):
    return _hashed_with_salt(pwd, const.login_pwd_salt)
