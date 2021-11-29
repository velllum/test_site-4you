from pydantic import BaseSettings


class Settings(BaseSettings):
    """- Реализация конфигурационных настроек
    из файла application/config/.env"""
    host: str
    port: int
    db: str


# получить объект настроек
settings = Settings(
    _env_file='application/.env',
    _env_file_encoding='utf-8',
)
