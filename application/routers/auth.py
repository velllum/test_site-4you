import logging
from random import randint
from typing import Optional, Union
from urllib.parse import urlencode

from fastapi import (
    APIRouter,
    Depends,
    Request
)

from db import users as users_db
from misc import redis, session
from misc.redis import (
    Connection as RedisConnection
)
from misc.db import (
    Connection as DbConnection
)
from misc.smtp import (
    send as send_mail,
    SMTP as SMTPConnection
)
from misc.fastapi.depends.db import (
    get as get_db
)
from misc.fastapi.depends.session import (
    get as get_session
)
from misc.fastapi.depends.redis import (
    get as get_cache
)
from misc.fastapi.depends.smtp import (
    get as get_smtp
)
from misc.fastapi.depends.conf import (
    get as get_conf
)
from misc.fastapi.depends.jinja import (
    get as get_jinja
)
from jinja2 import Environment as JinjaEnvironment
from misc.handlers import (
    error_400,
    error_401,
    error_404
)
from misc.password import (
    get_password_hash,
    generate_password
)
from misc.session import (
    Session,
    new_key
)
from models.auth import (
    MeResponse,
    MeSuccessResponse,
    RegisterModel,
    LoginModel,
    ConfirmModel,
    detect_login_type
)
from models.users import (
    UserAccountType
)
from models.base import SuccessResponse

from jinja2 import Template
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


DAY = 86400  # in seconds

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


logger = logging.getLogger(__name__)


@router.get('/me', name='me', response_model=MeSuccessResponse)
async def about_me(
        session: Session = Depends(get_session)
):
    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))


@router.post('/login', name='login', response_model=MeSuccessResponse)
async def login(
        auth: LoginModel,
        conn: DbConnection = Depends(get_db),
        session: Session = Depends(get_session),
        conf: dict = Depends(get_conf)
):
    if session.user.is_authenticated:
        return await error_401()

    data = detect_login_type(auth.login)
    if not data:
        return await error_400()

    user_account_type, login = data

    hashed_password = await get_password_hash(auth.password, conf['salt'])
    user = await users_db.get_user_by_cridentials(conn, user_account_type, login, hashed_password)

    if not user:
        return await error_404()

    session.set_user(user)
    
    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))


@router.post('/logout', name='logout', response_model=MeSuccessResponse)
async def logout(
        session: Session = Depends(get_session),
        cache: RedisConnection = Depends(get_cache)
):
    if not session.user:
        return await error_401()

    session.reset_user()
    
    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))


@router.post('/register', name='register', response_model=SuccessResponse)
async def register(
    req: Request,
    register: RegisterModel,
    conn: DbConnection = Depends(get_db),
    cache: RedisConnection = Depends(get_cache),
    smtp: SMTPConnection = Depends(get_smtp),
    jinja: JinjaEnvironment = Depends(get_jinja),
    conf: dict = Depends(get_conf)
):
    data = detect_login_type(register.login)
    if not data:
        return await error_400()

    user_account_type, login = data

    if await users_db.login_exists(conn, login):
        return await error_400('User already exists')

    code = randint(100000, 999999)
    if user_account_type == UserAccountType.MAIL:
        await send_registration_email(req, smtp, login, code, jinja, conf)
    else:
        raise NotImplementedError('Phone registration disabled')
    
    await redis.setex(
        key=confirm_key(login),
        ttl=DAY,
        value={
            'code': code,
            'login': login
        },
        conn=cache
    )
    return SuccessResponse()


@router.post('/recover', name='recover', response_model=SuccessResponse)
async def recover(
    req: Request,
    register: RegisterModel,
    session: Session = Depends(get_session),
    smtp: SMTPConnection = Depends(get_smtp),
    conn: DbConnection = Depends(get_db),
    cache: RedisConnection = Depends(get_cache),
    jinja: JinjaEnvironment = Depends(get_jinja),
    conf: dict = Depends(get_conf)
):
    data = detect_login_type(register.login)
    if not data:
        return await error_400()

    user_account_type, login = data

    if await users_db.login_exists(conn, login):
        code = randint(100000, 999999)
        if user_account_type == UserAccountType.MAIL:
            await send_recover_email(req, smtp, login, code, jinja, conf)
        else:
            raise NotImplementedError('Phone password restore disabled')

        await redis.setex(
            key=confirm_key(login),
            ttl=DAY,
            value={
                'code': code,
                'login': login
            },
            conn=cache
        )
    return SuccessResponse()


@router.post('/confirm', name='confirm', response_model=MeSuccessResponse)
async def confirm(
        req: Request,
        confirm: ConfirmModel,
        session: Session = Depends(get_session),
        conn: DbConnection = Depends(get_db),
        cache: RedisConnection = Depends(get_cache),
        smtp: SMTPConnection = Depends(get_smtp),
        jinja: JinjaEnvironment = Depends(get_jinja),
        conf: dict = Depends(get_conf)
):
    data = detect_login_type(confirm.login)
    if not data:
        return await error_400()

    user_account_type, login = data
    code = confirm.code

    if session.user.is_authenticated:
        account = session.user.account_by_login(user_account_type, login)
        if not account:
            return await error_401()

    cache_data = await redis.get(
        key=confirm_key(login),
        conn=cache
    )
    
    if not cache_data:
        return await error_401(message='')
        
    if code != cache_data['code']:
        return await error_400('Wrong confirmation code')

    password = await generate_password()
    hashed_password = await get_password_hash(password, conf['salt'])
    if await users_db.login_exists(conn, login):
        await users_db.set_password(conn, login, hashed_password)
    else:
        user = await users_db.create_user(conn, user_account_type, login, hashed_password)
        if not user:
            return await error_400()
    
    if user_account_type == UserAccountType.MAIL:
        await send_password_email(smtp, login, password, jinja, conf)
    else:
        raise NotImplementedError('Phone password restore disabled')

    await redis.del_(
        key=confirm_key(login),
        conn=cache
    )

    if not session.user.is_authenticated:
        user = await users_db.get_user_by_cridentials(conn, user_account_type, login, hashed_password)
        if user:
            session.set_user(user)

    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))


async def send_registration_email(
    req: Request,
    smtp: SMTPConnection, 
    email: str, 
    code: int, 
    jinja: JinjaEnvironment,
    conf: dict
):
    msg = MIMEMultipart()
    msg['To'] = email
    msg['From'] =conf['smtp']['sender']
    msg['Subject'] = 'Регистрация'
    
    part = MIMEText(await generate_register_template(jinja, code=code), 'html')

    msg.attach(part)

    await send_mail(
        smtp, 
        msg
    )


async def send_recover_email(
    req: Request,
    smtp: SMTPConnection, 
    email: str, 
    code: int, 
    jinja: JinjaEnvironment,
    conf: dict
):
    msg = MIMEMultipart()
    msg['To'] = email
    msg['From'] =conf['smtp']['sender']
    msg['Subject'] = 'Восстановление пароля'
    
    part = MIMEText(await generate_recover_template(jinja, code=code), 'html')

    msg.attach(part)

    await send_mail(
        smtp, 
        msg
    )


async def send_password_email(
    smtp: SMTPConnection, 
    email: str,
    password: str,
    jinja: JinjaEnvironment,
    conf: dict
):
    msg = MIMEMultipart()
    msg['To'] = email
    msg['From'] =conf['smtp']['sender']
    msg['Subject'] = 'Пароль для входа'
    
    part = MIMEText(await generate_password_template(jinja, email=email, password=password), 'html')

    msg.attach(part)

    await send_mail(
        smtp, 
        msg
    )


async def generate_register_template(jinja, **data) -> str:
    return await generate_tpl(jinja, "auth/confirm-message.html", **data)


async def generate_recover_template(jinja, **data) -> str:
    return await generate_tpl(jinja, "auth/recover-password.html", **data)


async def generate_password_template(jinja, **data) -> str:
    return await generate_tpl(jinja, "auth/send-password.html", **data)


async def generate_tpl(jinja: JinjaEnvironment, path: str, **data) -> str:
    template = jinja.get_template(path)
    return template.render(**data)


def confirm_key(email: str) -> str:
    return f'confirm_{email}'
