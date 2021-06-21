import os

class SQLConfig(object):
    dbname = os.environ["WEB_DB"]
    user = os.environ["WEB_DB_USER"]
    password = os.environ["WEB_DB_PASSWORD"]

    host = None
    try:
        host = os.environ["WEB_DB_HOST"]
    except KeyError:
        host = None
