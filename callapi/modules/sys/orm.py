# -*- encoding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,Integer,String

Base = declarative_base()

class Account(Base):
    __tablename__ = u'account'

    id = Column(Integer,primary_key=True)
    user_name = Column(String(50),nullable=False)
    password = Column(String(200),nullable=False)
    title = Column(String(50))
    salary = Column(Integer)

    def __str__(self):
        return "account.id=%s,account.name=%s"%(self.id,self.user_name)

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)

    def is_active(self):
        #假设所有用户都是活跃用户
        return True

    def get_id(self):
        #返回账号Id，用方法返回属性值提高了表的封装性
        return True

    def is_authenticated(self):
        #假设已经通过验证
        return True

    def is_anoymous(self):
        #具有登录名和密码的账号不是匿名用户
        return False

#========================================================
from sqlalchemy import table,Column,Integer,ForeignKey,String
from sqlalchemy.orm import relationship,backref
#from sqlalchemy.ext.declarative import declarative_base

class Class(Base):
    __tablename__ = 'class'
    class_id = Column(Integer,primary_key=True)
    name = Column(String(50))
    level = Column(Integer)
    address = Column(String(200))

    class_teacher = relationship("ClassTeacher",backref="class",cascade='all')
    students = relationship("Student",backref="class")

class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer,primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    address = Column(String(200))
    class_id = Column(Integer,ForeignKey('class.class_id'))

class Teacher(Base):
    __tablename__ = 'teacher'
    teacher_id = Column(Integer,primary_key=True)
    name = Column(String(50))
    gender = Column(String(10))
    telephone = Column(String(50))
    address = Column(String(200))
    class_teachers = relationship("ClassTeacher",backref="teacher")

class ClassTeacher(Base):
    __tablename__ = 'class_teacher'
    teacher_id = Column(Integer,ForeignKey('teacher.teacher_id'),primary_key=True)
    class_id = Column(Integer,ForeignKey('class.class_id'),primary_key=True)
















