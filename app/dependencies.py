from config.settings import get_settings
from config.db_connection import DBConnectionHandler

settings = get_settings()

connection_handler = DBConnectionHandler(
    connection_string=settings.database_url
)
