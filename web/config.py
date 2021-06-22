import os

def env_or(env_var_name, alternative=None):
    try:
        return os.environ[env_var_name]
    except KeyError:
        print(f"No env var {env_var_name}")
        return alternative

class SQLConfig(object):
    dbname = os.environ["WEB_DB"]
    user = os.environ["WEB_DB_USER"]
    password = os.environ["WEB_DB_PASSWORD"]
    host = env_or("WEB_DB_HOST")

class TgConfig(object):
   api_url = env_or("TG_API", "https://api.telegram.org/")
   bot_method = env_or("TG_BOT")
   chat_id = env_or("TG_CHAT_ID")
