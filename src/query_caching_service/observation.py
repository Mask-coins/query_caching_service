import datetime

from .access import Access, URLAccess


class Observation(Access):
    @property
    def select(self):
        return 'SELECT response FROM observation WHERE query = ? order by timestamp desc ;'

    @property
    def insert_query(self):
        return """INSERT INTO observation VALUES(?, ?, ?)"""

    @property
    def primary_query(self):
        return """
                CREATE TABLE IF NOT EXISTS observation (
                query    TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                response TEXT NOT NULL,
                PRIMARY KEY (query, timestamp)
                );
            """

    def insert(self, query, response):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(self.insert_query, (self.query2str(query), datetime.datetime.now(), self.response2str(response)))
        conn.commit()
        cur.close()
        conn.close()

    def load_db(self):
        conn = self.conn
        cur = conn.cursor()
        cur.execute('SELECT * FROM observation ;')
        res = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return res

    def run(self, query):
        response = self.access(query)
        old_response = self.fetch_temp(query)
        if response != old_response:
            self.add_temp(query, response)
        old_response = self.fetch_db(query)
        if response != old_response:
            self.insert(query, response)
        return response


class URLObservation(Observation, URLAccess):
    pass
