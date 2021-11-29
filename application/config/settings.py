from pydantic import BaseSettings


class Settings(BaseSettings):
    """- Реализация конфигарациооных настроек"""
    host: str = '127.0.0.1'
    port: int = 8000

    # из файла application/config/.env
    db: str


# получить объект настроек
settings = Settings(
    _env_file='application/config/.env',
    _env_file_encoding='utf-8',
)
