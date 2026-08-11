from config.settings import get_settings
from config.db_connection import DBConnectionHandler

settings = get_settings()

def get_connection_handler() -> DBConnectionHandler:
    return DBConnectionHandler(connection_string=settings.database_url)