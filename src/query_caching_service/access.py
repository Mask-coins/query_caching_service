import sqlite3
import urllib
from typing import Any
import chardet
from urllib import request

dir_path = ""


class Access(object):
    _temp_dict: dict[str,[dict]] = dict()

    def __init__(self):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(self.primary_query)
        conn.commit()
        conn.close()

    @classmethod
    def add_temp(cls, key, value):
        if cls.__name__ not in cls._temp_dict:
            cls._temp_dict[cls.__name__] = dict()
        cls._temp_dict[cls.__name__][cls.query2str(key)] = cls.response2str(value)

    @classmethod
    def fetch_temp(cls, query):
        query_str = cls.query2str(query)
        if cls.__name__ not in cls._temp_dict:
            return None
        if query_str not in cls._temp_dict[cls.__name__]:
            return None
        response_str = cls._temp_dict[cls.__name__][query_str]
        return cls.str2response(response_str)

    @classmethod
    def query2str(cls, key:Any) -> str:
        return key

    @classmethod
    def str2query(cls, key:str) -> Any:
        return key

    @classmethod
    def response2str(cls, value:Any) -> str:
        return value

    @classmethod
    def str2response(cls, value:str) -> Any:
        return value

    @property
    def db_name(self):
        if dir_path == "":
            return self.__class__.__name__ + ".db"
        return dir_path + "/" + self.__class__.__name__ + ".db"

    @property
    def conn(self):
        return sqlite3.connect(self.db_name)

    @property
    def primary_query(self):
        return """
                CREATE TABLE IF NOT EXISTS queries (
                query    TEXT NOT NULL,
                response TEXT NOT NULL,
                PRIMARY KEY (query)
                );
            """

    @property
    def insert_query(self):
        return """INSERT INTO queries VALUES(?, ?)"""

    def insert(self, query, response):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(self.insert_query, (self.query2str(query), self.response2str(response)))
        conn.commit()
        cur.close()
        conn.close()

    def insert_many(self, query=None, data=None, query_data_dict=None):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(self.insert_query, data)
        conn.commit()
        cur.close()
        conn.close()

    @property
    def select(self):
        return 'SELECT response FROM queries WHERE query = ?;'

    def fetch_db(self, query):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(self.select,(self.query2str(query),))
        res = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if res is None:
            return None
        return self.str2response(res[0])

    def access(self,query):
        response = query
        return response

    def run(self, query):
        response = self.fetch_temp(query)
        if response is not None:
            return response
        response = self.fetch_db(query)
        if response is not None:
            return response
        response = self.access(query)
        self.insert(query, response)
        self.add_temp(query, response)
        return response


class URLAccess(Access):
    def access(self,query, encoding=None):
        with request.urlopen(query) as fp:
            if encoding:
                return fp.read().decode(encoding)
            res = fp.read()
            enc = chardet.detect(res)
            response = res.decode(enc['encoding'])
            return response


if __name__=="__main__":
    a = URLAccess()
    print(a.run("https://blog.dblp.org/feed/"))


