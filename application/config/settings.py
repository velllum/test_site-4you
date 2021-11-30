import os

from pydantic import BaseSettings


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
