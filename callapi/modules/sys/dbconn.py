# -*- encoding: utf-8 -*-
import orm
from orm import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

#配置链接mysql数据库
db_connect_string = "mysql://root:mysql@localhost:3306/mytest?charset=utf8"
engine = create_engine(db_connect_string,encoding='utf8', max_overflow=5,pool_size=10)
SessionType = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))

orm.Base.metadata.create_all(engine)
'''
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([User(name=username) for username in ('xiaoming', 'wanglang', 'lilei')])
session.commit()
'''

def GetSession():
    return SessionType

from contextlib import contextmanager
@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield  session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == '__main__':
    print 'start....'