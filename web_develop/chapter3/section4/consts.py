# coding=utf-8
HOSTNAME = 'localhost'
DATABASE = 'mytest'
USERNAME = 'root'
PASSWORD = 'mysql'
DB_URI = 'mysql://{}:{}@{}/{}'.format(
    USERNAME, PASSWORD, HOSTNAME, DATABASE)
