import os
import sqlite3
from sqlite3 import Error
import json


class Datastore:
    def __init__(self):
        self.conn = None
        self.db = None

    def setup(self, db=None):
        if db is None:
            curpath = os.path.dirname(os.path.realpath(__file__))
            dbpath = os.path.join(curpath, "persisted.db")
            if os.path.isfile(dbpath):
                db = dbpath
            else:
                db = Datastore.migrate()
        try:
            self.conn = sqlite3.connect(db)
            self.db = self.conn.cursor()
        except Error as e:
            print(e)

        return self

    def close(self):
        try:
            self.conn.close()
        except Error as e:
            print(e)

    def persist(self, data):
        persist_data_sql = "INSERT INTO persisted (data) VALUES (?);"
        try:
            self.db.execute(persist_data_sql, (data,))
            self.conn.commit()
        except Error as e:
            print(e)

    def fetch_all(self):
        fetch_all_sql = "SELECT data from persisted;"
        try:
            self.db.execute(fetch_all_sql)
            data = self.db.fetchall()
            return data
        except Error as e:
            print(e)

    def fetch_some(self, limit, offset):
        fetch_some_sql = "SELECT data from persisted LIMIT ? OFFSET ?"
        try:
            self.db.execute(fetch_some_sql, (limit, offset))
            data = self.db.fetchall()
            return data
        except Error as e:
            print(e)

    def pop(self):
        pop_sql = "DELETE FROM persisted WHERE id = (SELECT MAX(id) FROM persisted);"
        try:
            self.db.execute(pop_sql)
            self.conn.commit()
        except Error as e:
            print(e)

    @classmethod
    def migrate(cls):
        conn = None
        create_tables_sql = """ CREATE TABLE IF NOT EXISTS persisted
                        (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data TEXT,
                            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        ); """

        try:
            conn = sqlite3.connect("persisted.db")
            c = conn.cursor()
            c.execute(create_tables_sql)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

        curpath = os.path.dirname(os.path.realpath(__file__))
        dbpath = os.path.join(curpath, "persisted.db")
        return dbpath
