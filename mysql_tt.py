#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-11-24 下午3:18
# @Author  : Arvin
# @Site    : 
# @File    : mysql_tt.py
# @Software: PyCharm

import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("10.9.111.12","root","Aicyber201415926","survey" )
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT * from robot_question")
# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()
print "Database version : %s " % data
# 关闭数据库连接
db.close()
