from fastapi import HTTPException
from starlette import status


class MessageService:
    """- Сервис сообщений"""

    @classmethod
    def error_404(cls, message: str) -> HTTPException:
        """- вывод ошибки 404"""
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
