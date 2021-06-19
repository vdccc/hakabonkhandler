import psycopg2

class DBConnection:

    def __init__(self):
        self.dbname = "testdb"
        self.user = "hack"
        self.password = "hack"
        self.con = None

    def exec(self, req, item_id, all=False):
        if self.con is None:
            self.con = psycopg2.connect(dbname=self.dbname,
                                        user=self.user,
                                        password=self.password)
        cur = self.con.cursor();
        cur.execute(req, (item_id,))

        if all:
            return cur.fetchall()
        else:
            return cur.fetchone()
