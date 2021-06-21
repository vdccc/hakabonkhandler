import psycopg2

from config import SQLConfig

class SQLConnection:

    def __init__(self):
        self.dbname = SQLConfig.dbname
        self.user = SQLConfig.user
        self.password = SQLConfig.password
        self.host = SQLConfig.host

        self.con = None

    def connect(self):
        self.con = psycopg2.connect(dbname=self.dbname, user=self.user,
                                    password=self.password, host=self.host)

    def close(self):
        if self.con is not None:
            self.con.close()
            self.con = None

    def exec(self, req, args, all=False, fetch=True):

        if self.con is None:
            self.connect()

        cur = self.con.cursor();
        cur.execute(req, args)

        if not fetch:
            self.con.commit()

        if all:
            return cur.fetchall()
        else:
            return cur.fetchone()

    def mogrify(self, req, args):
        self.connect()
        result = self.con.cursor().mogrify(req, args)
        self.close()
        return result
