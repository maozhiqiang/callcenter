# coding=utf-8
import  uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TEXT,Integer

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_test'
    id = Column(Integer, primary_key = True)
    username = Column(String(128), index = True)
    password_hash = Column(String(128))

    def __init__(self, username=None, password = None):
        self.username = username
        self.password_hash = password
        print 'username is ',self.username

    def __repr__(self):
        return "<[User] username:`{}`, password:`{}`".format(self.username, self.password_hash)

class Role(Base):
    __tablename__ = 'role_test'
    id = Column(String(32), primary_key=True)
    title = Column(String(128))
    content = Column(TEXT)
    account_id = Column(String(64))
    main_flow_id = Column(String(64))
    create_time = Column(String(19))