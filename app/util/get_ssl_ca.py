from pathlib import Path

from config.settings import get_settings


def get_mysql_ssl_ca_path() -> str:
    settings = get_settings()
    certificate = settings.mysql_ssl_ca

    if not certificate:
        raise RuntimeError("MYSQL_SSL_CA is not configured")

    path = Path("/tmp/mysql-ca.pem")
    path.write_text(certificate)

    return str(path)