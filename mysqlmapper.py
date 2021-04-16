# -- coding: utf-8 --

import pymysql


class MysqlMapper(object):
    def __init__(self, host, port, user, password):
        self.conn = pymysql.connect(host=host, port=int(port), user=user, password=password)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def show_databases(self):
        self.cursor.execute("show databases")
        return self.cursor.fetchall()

    def show_tables(self, database):
        self.cursor.execute("use `%s`" % database)
        self.cursor.execute("show tables")
        return self.cursor.fetchall()

    def show_table_status(self, table):
        self.cursor.execute("show table status where name = '%s'" % table)
        return self.cursor.fetchall()

    def show_field(self, table):
        self.cursor.execute("SHOW FULL COLUMNS FROM  `%s`" % table)
        return self.cursor.fetchall()

    def insert_data(self, param, value, table):
        sql = "insert into %s %s values %s" % (table, param, value)
        self.cursor.execute(sql)


def dict_factory(cursor, row):
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data
