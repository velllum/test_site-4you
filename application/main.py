import logging
from fastapi import FastAPI
import asyncio
import functools
from misc.session import Session
from misc.handlers import register_exception_handler
from misc.mqtt import mqtt
from misc.mqtt import queue
from models.base import ErrorResponse


logger = logging.getLogger(__name__)


def factory():
    app = ctrl.main_with_parser(None, main)
    if not app:
        raise RuntimeError
    return app


def main(args, config):
    """- точка входа"""
    root_path = config.get('root_path', None)
    app = FastAPI(
        title="CraftRadio HTTP REST API",
        debug=config.get('debug', False),
        root_path=root_path,
        responses=responses(),
        exception_handlers=responses()
    )

    app.state.args = args
    app.state.config = config
    register_exception_handler(app)

    init(app)

    logger.info(f"REST API app allocated")
    return app


def init(app):
    register_startup(app)
    register_shutdown(app)

    register_routers(app)


def register_startup(app):
    """- запускается в начале работы"""
    @app.on_event("startup")
    async def hander():
        logger.info('Startup called')
        try:
            await startup(app)
            logger.info(f"REST API app startup executed")
        except:
            logger.exception('Startup crashed')


def register_shutdown(app):
    """- запускается в конце"""
    @app.on_event("shutdown")
    async def hander():
        logger.info('Shutdown called')
        try:
            await shutdown(app)
            logger.info(f"REST API app shutdown executed")
        except:
            logger.exception('Shutdown crashed')


def register_routers(app):
    """- добавляем роуты"""
    from . import routers
    return routers.register_routers(app)


async def startup(app):
    app.state.loop = asyncio.get_event_loop()
    app.state.mqtt = await mqtt.init(
        app.state.config["mqtt"],
        "fast_api",
        on_connect=queue.on_connect(app),
        on_message=queue.on_message(app),
        on_disconnect=queue.on_disconnect(app),
        on_subscribe=queue.on_subscribe(app)
    )
    app.state.db_pool = await db.init(app.state.config['db'])
    app.state.redis_pool = await redis.init(app.state.config['redis'])
    app.state.smtp = await smtp.init(app.state.config['smtp'])
    await storage.init(app.state.config['storage'])
    app = await startup_jinja(app)
    return app    


async def startup_jinja(app):
    from jinja2 import (
        Environment, 
        ChoiceLoader,
        PackageLoader, 
        FileSystemLoader, 
        select_autoescape
    )

    env = Environment(
        loader=ChoiceLoader([
            FileSystemLoader('templates')
        ]),
        autoescape=select_autoescape()
    )
    app.state.jinja = env
    return app


async def shutdown(app):
    if app.state.db_pool:
        await db.close(app.state.db_pool)
    if app.state.redis_pool:
        await redis.close(app.state.redis_pool)
    if app.state.mqtt:
        await mqtt.close(app.state.mqtt)


def responses():
    return {
        400: {
            "model": ErrorResponse
        },
        401: {
            "model": ErrorResponse
        },
        404: {
            "model": ErrorResponse
        },
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    }
