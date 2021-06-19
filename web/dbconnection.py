import psycopg2
import os

class DBConnection:

    def __init__(self):
        self.dbname = "testdb"
        self.user = "hack"
        self.password = "hack"
        self.con = None
        self.host = os.environ['SQL_HOST']


    def exec(self, req, args, all=False, fetch=True):
        if self.con is None:
            if self.host is not None:
                self.con = psycopg2.connect(dbname=self.dbname, user=self.user,
                                            password=self.password, host=self.host)
            else:
                self.con = psycopg2.connect(dbname=self.dbname, user=self.user,
                                            password=self.password)
        
        cur = self.con.cursor();
        cur.execute(req, args)

        if not fetch:
            self.con.commit()
            print("not fetch")
            return ()

        if all:
            return cur.fetchall()
        else:
            return cur.fetchone()
