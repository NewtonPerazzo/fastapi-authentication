from app.util import get_ssl_ca
from config.settings import get_settings
from config.db_connection import DBConnectionHandler

settings = get_settings()

def get_connection_handler() -> DBConnectionHandler:
    return DBConnectionHandler(
        connection_string=settings.database_url,
        ssl_ca=get_ssl_ca(),
    )