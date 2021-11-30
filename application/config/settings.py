import os

from pydantic import BaseSettings

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(os.getcwd(), 'application/database/data/db.sqlite3')}"

# получить полный путь до корневой директории с файлом .env
env_dir = os.path.join(os.getcwd(), '.env')


class Settings(BaseSettings):
    """- Реализация конфигурационных настроек
    из файла application/config/.env"""
    host: str
    port: int
    db: str


# получить объект настроек
settings = Settings(
    _env_file=env_dir,
    _env_file_encoding='utf-8',
)

# @lru_cache()
# def get_settings():
#     return {
#         "host": settings.host,
#         "port": settings.port,
#         "db": settings.db,
#     }

