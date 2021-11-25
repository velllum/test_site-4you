from typing import Optional, Tuple, Match
import re

from pydantic import BaseModel, constr, Field

from .base import SuccessResponse
from .users import UserAccountType, User


class MeResponse(BaseModel):
    token: str
    me: User


class MeSuccessResponse(SuccessResponse):
    data: MeResponse


class RegisterModel(BaseModel):
    login: constr(to_lower=True, strip_whitespace=True)


class AuthConfirmModel(BaseModel):
    email: constr(to_lower=True, strip_whitespace=True)
    code: int


class LoginModel(BaseModel):
    login: constr(to_lower=True, strip_whitespace=True)
    password: constr(strip_whitespace=True)


class ConfirmModel(BaseModel):
    login: constr(to_lower=True, strip_whitespace=True)
    code: int


def detect_login_type(login: str) -> Optional[Tuple[UserAccountType, str]]:
    if is_valid_email(clean_email(login)):
        return UserAccountType.MAIL, clean_email(login)
    
    if is_valid_phone(clean_phone(login)):
        return UserAccountType.PHONE, clean_phone(login)
    
    return None


EMAIL_REGEX = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
PHONE_REGEX = r'[0-9]{4,}'


def is_valid_email(data: str) -> Optional[Match[str]]:
    return re.match(EMAIL_REGEX, data)


def is_valid_phone(data: str) -> Optional[Match[str]]:
    return re.match(PHONE_REGEX, data)


def clean_email(data: str) -> str:
    return data.strip()


def clean_phone(data: str) -> str:
    return data \
        .replace(' ', '') \
        .replace('+', '') \
        .replace('-', '') \
        .replace('(', '') \
        .replace(')', '') \
        .strip()
