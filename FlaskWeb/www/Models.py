# coding=utf-8
import  uuid
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TEXT,Integer
from flask_login import UserMixin,AnonymousUserMixin

Base = declarative_base()

class User(Base,UserMixin):
    __tablename__ = 'users_test'
    id = Column(Integer, primary_key = True)
    username = Column(String(128), index = True)
    password_hash = Column(String(128))

    def __init__(self, username=None, password = None):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "<[User] username:`{}`, password:`{}`".format(self.username, self.password_hash)


    def generate_token(self, expiration=3600):
        s = Serializer('secret key', expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer('secret key')
        data = s.loads(token)
        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        return True

    @property
    def password(self):
        raise AttributeError('password cannot be read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(Base):
    __tablename__ = 'role_test'
    id = Column(String(32), primary_key=True)
    title = Column(String(128))
    content = Column(TEXT)
    account_id = Column(String(64))
    main_flow_id = Column(String(64))
    create_time = Column(String(19))