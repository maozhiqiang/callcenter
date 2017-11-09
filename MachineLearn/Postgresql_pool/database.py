#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import redis
from psycopg2 import connect
from psycopg2.pool import SimpleConnectionPool
import config

config_conn = dict(config.PostgresqlDbConfig)
del config_conn['minconn']
del config_conn['maxconn']


class Redis(redis.Redis):
    def __init__(self, cnf):
        pool = redis.ConnectionPool(**cnf)
        super(redis.Redis, self).__init__(connection_pool=pool)

    def getn(self, name):
        try:
            return self.get(name).decode()
        except:
            return None


class PSQL(object):

    def __init__(self):
        self.pool = None
        self.conn = None
        self.cursor = None
        self.need_update = None

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
            if self.need_update:
                self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __getCursor(self):
        if self.cursor is None:
            self.cursor = self.conn.cursor()
        return self.cursor

    def get_conn(self, key=None):
        if key:
            if not self.pool:
                self.pool = SimpleConnectionPool(**config.PostgresqlDbConfig)
            self.conn = self.pool.getconn(key)
        else:
            self.conn = connect(**config_conn)
        self.conn.autocommit = False

    def put_conn(self, key, close=False):
        self.pool.putconn(self.conn, key, close)

    def insert(self, data={}, table=None):
        keys, vals = [], []
        for k, v in data.items():
            keys.append(k)
            vals.append(v)
        val_str = ','.join(['%s'] * len(vals))
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, ','.join(keys), val_str)
        self.cursor = self.__getCursor()
        self.cursor.execute(sql, tuple(vals))
        self.need_update = 1

    def findBySql(self, sql='', args=None):
        self.cursor = self.__getCursor()
        self.cursor.execute(sql, tuple(args))
        return self.cursor.fetchall()

    def group_location(self, locate={}):
        cond = dict(locate)
        args = []
        sql = ' WHERE '
        if 'union' in cond:
            union = ' %s ' % cond['union']
            del cond['union']
        else:
            union = ' AND '
        for k in cond:
            v = cond[k]
            if isinstance(v, str):
                if v.startswith('%') or v.endswith('%'):
                    sql += "%s LIKE %%s" % k
                else:
                    sql += "%s=%%s" % k
                args.append(v)
            elif isinstance(v, int) or isinstance(v, float):
                sql += "%s=%%s" % k
                args.append(v)
            elif isinstance(v, list):
                sql += '%s in (%s)' % (k, ','.join(['%s'] * len(v)))
                args.extend(v)
            sql += union
        return sql[:-5], tuple(args)

    def query(self, table=None, columns=None, locate={}, order_by='', limit=0):
        if not columns:
            columns = getattr(config, 'column_%s' % table)
            _query = ','.join(columns)
        elif isinstance(columns, str):
            _query = columns
        elif isinstance(columns, list):
            _query = ','.join(columns)
        else:
            raise BaseException
        sql = "SELECT %s FROM %s " % (_query, table,)

        args = ()
        if locate:
            sql_cond, args = self.group_location(locate)
            sql += sql_cond
        if order_by:
            sql += ' ORDER BY %s' % order_by
            # args += (order_by, )
        if limit:
            sql += ' LIMIT %s' % limit
            # args += (limit, )

        self.cursor = self.__getCursor()
        # print(sql, '--sql')
        self.cursor.execute(sql, args)
        res = self.cursor.fetchall()
        if isinstance(columns, str):
            return res[0][0]
        if not res:
            return res

        if limit == 1:
            data = dict([(column.split(' as ')[-1], res[0][idx])
                         for idx, column in enumerate(columns)])
        else:
            data = [dict([(column.split(' as ')[-1], item[idx])
                          for idx, column in enumerate(columns)]
                         ) for item in res]
        return data

    def update(self, table=None, data={}, locate={}):
        sql = 'UPDATE %s SET ' % table
        args = []
        for k in data:
            if k[-1] in '+-':
                sql += '%s=%s%s%%s,' % (k[:-1], k[:-1], k[-1],)
                args.append(str(data[k]))
            else:
                sql += "%s=$$%s$$," % (k, str(data[k]))
        sql = sql[:-1]
        if locate:
            sql_cond, _args = self.group_location(locate)
            sql += sql_cond
            args.extend(_args)

        self.cursor = self.__getCursor()
        self.cursor.execute(sql, tuple(args))
        self.need_update = 1

    def delete(self, table=None, locate={}, delete_all=False):
        sql = 'DELETE FROM %s ' % table
        args = ()
        if locate:
            sql_cond, args = self.group_location(locate)
            sql += sql_cond
        # 防止情况
        elif not locate and not delete_all:
            print("can't delete all")
            raise Exception
        self.cursor = self.__getCursor()
        # print(sql)
        self.cursor.execute(sql, args)
        self.need_update = 1


