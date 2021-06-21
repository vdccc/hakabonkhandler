from dbconnection import SQLConnection

class SQLRequest():

    def __init__(self):
        self.con = None
        self.body = None

    def _abstract_run(self, args, single=True, all=False, fetch=True):
        result = None

        try:
            result = self.con.exec(self.body, args, all=all, fetch=fetch)
        except:
            print("Failed to run a request: ", self.con.mogrify(self.body, args))
            print("Body: ", self.body)
            print("Args: ", args)

        if result is None:
            return result

        return result[0] if single else result


class SQLRequestGetMisses(SQLRequest):

    def __init__(self, con=SQLConnection()):
        self.con = con
        self.body = """
        SELECT misses FROM prices WHERE id = %s;
        """

    def run(self, price_tag_id):
        return self._abstract_run((price_tag_id,))

class SQLRequsetUpdateMisses(SQLRequest):

    def __init__(self, con=SQLConnection()):
        self.con = con
        self.body = """
        UPDATE prices SET misses = %s WHERE id = %s;
        """

    def run(self, price_tag_id, misses):
        return self._abstract_run((misses, price_tag_id), fetch=False)

class SQLRequestGetNewestTagDate(SQLRequest):

    def __init__(self, con=SQLConnection()):
        self.con = con
        self.body = """
        SELECT date FROM prices WHERE item_id = %s ORDER BY date DESC;
        """

    def run(self, item_id):
        return self._abstract_run((item_id,))

class SQLRequsetGetTagDate(SQLRequest):

    def __init__(self, con=SQLConnection()):
        self.con = con
        self.body = """
        SELECT date FROM prices WHERE id = %s;
        """

    def run(self, price_tag_id):
        return self._abstract_run((price_tag_id,))

class SQLInsertNewTag(SQLRequest):

    def __init__(self, con=SQLConnection()):
        self.con = con
        self.body = """
        INSERT INTO prices(date, item_id, misses) VALUES (%s, %s, %s) RETURNING id;
        """

    def run(self, date, item_id, misses=0):
        return self._abstract_run((date, item_id, misses), fetch=False)
