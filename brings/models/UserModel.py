# coding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TEXT

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_test'
    id = Column(String(32), primary_key = True)
    username = Column(String(128), index = True)
    password_hash = Column(String(128))