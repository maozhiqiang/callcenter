# -*- encoding: utf-8 -*-
import orm
from callapi.common.utils import to_json
from dbconn import session_scope
from sqlalchemy import or_

'''
eg:各种查询条件
1、等值过滤器 session.query(Account).filter(Account.user_name == 'Jacky')
2、不等过滤器 session.query(Account).filter(Account.user_name != 'Jacky')
   (!=  ,< ,>, <=, >=)
3、模糊查询 like
    session.query(Account).filter(Account.user_name.like('%i%'))
4、包括过滤器 in_
    查询id 不为1.3.5的记录
    session.query(Account).filter(~Account.id.in_([1.3.5]))
5、判断是否为空 is NULL 、is not NULL 
    session.query(Account).filter(Account.salary == None)
    session.query(Account).filter(Account.salary.is_(None) )
    
    session.query(Account).filter(Account.salary != None)
    session.query(Account).filter(Account.salary.isnot(None) )
6、与逻辑 and_
    session.query(Account).filter(Account.title == 'Engineer',Account.salary == 3000)
    session.query(Account).filter(and_(Account.title == 'Engineer',Account.salary == 3000))
    session.query(Account).filter(Account.title == 'Engineer').filter(Account.salary == 3000)

7、 或逻辑(or_)
    查询title是Engneer 或者salary为3000的记录
    session.query(Account).filter(or_(Account.title == 'Engineer',Account.salary == 3000))

'''

#添加操作
def InsertAccount(user,password,title,salary):
    with session_scope() as session:
        account = orm.Account(user_name = user,password = password,title = title,salary = salary)
        session.add(account)
#查询操作
def GetAccount(id = None,user_name = None):
    with session_scope() as session:
        return session.query(orm.Account).filter(or_(orm.Account.id == id,orm.Account.user_name == user_name)).first()
#删除操作
def DeleteAccount(user_name):
    with session_scope() as session:
        account = GetAccount(user_name = user_name)
        if account:
            session.delete(account)
#更新操作
def UpdateAccount(id,user_name,password,title,salary):
    with session_scope() as session :
        account = session.query(orm.Account).filter(or_(orm.Account.id == id)).first()
        if not account: return
        account.user_name = user_name
        account.password = password
        account.title = title
        account.salary = salary



if __name__ == '__main__':
    print 'start.....'
    #InsertAccount('Arvin','123456','System Manager',3000)
    #InsertAccount('Bellee', '123456', 'System Manager', 3000)
    account = GetAccount(2)
    print account
    dct = to_json(account)
    print dct
    # print account.__str__()
    # print account.__repr__()

    # UpdateAccount(1,'admin',"none","System Admin",2000)