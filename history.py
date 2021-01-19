# -- coding: utf-8 --

import sqlite3
import json


class History(object):
    def __init__(self):
        self.conn = sqlite3.connect("history.db")
        self.cursor = self.conn.cursor()
        self.conn.row_factory = dict_factory
        self.create_database()

    def create_database(self):
        self.cursor.execute("create table if not exists `history` (id varchar(255) primary key, name text)")
        self.conn.commit()

    def update_history(self, key, value):
        if len(self.select_history(key)) == 0:
            self.insert_history(key, value)
        else:
            self.cursor.execute("update `history` set name = '%s' where id = '%s'" % (value, key))
            self.conn.commit()

    def insert_history(self, key, value):
        self.cursor.execute("insert into `history` values (?, ?)", (key, value))
        self.conn.commit()

    def list_history(self):
        self.cursor.execute("select * from `history`")
        return self.cursor.fetchall()

    def select_history(self, key):
        self.cursor.execute("select * from `history` where id = '%s'" % key)
        return self.cursor.fetchall()


def dict_factory(cursor, row):
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data
