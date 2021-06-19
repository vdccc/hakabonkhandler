import psycopg2

class DBConnection:

    def __init__(self):
        self.dbname = "testdb"
        self.user = "hack"
        self.password = "hack"
        self.con = None

    def exec(self, req, args, all=False, fetch=True):
        if self.con is None:
            self.con = psycopg2.connect(dbname=self.dbname,
                                        user=self.user,
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
