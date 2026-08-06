from config.settings import get_settings
from config.db_connection import DBConnectionHandler

settings = get_settings()


def get_connection_handler() -> DBConnectionHandler:
    print(settings.database_url)
    return DBConnectionHandler(connection_string=settings.database_url)
