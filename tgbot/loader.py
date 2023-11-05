from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from tgbot.config import config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from infrastructure.database.setup import create_engine, create_session_pool
import logging
from typing import List
import betterlogging as bl


def register_global_middlewares(dp: Dispatcher, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging(ignored: List[str] = ""):
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.DEBUG
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # for ignore in ignored:
    #     logger.disable(ignore)
    # logger.info('Logging is successfully configured')

    logger.info("Starting bot")


def get_storage(conf):
    """
    Return storage based on the provided configuration.

    Args:
        conf (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if conf.tg_bot.use_redis:
        return RedisStorage.from_url(
            conf.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


setup_logging()
storage = get_storage(config)
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
dp = Dispatcher(storage=storage)
engine = create_engine(config.db, echo=True)
session_pool = create_session_pool(engine)

dp.include_routers(*routers_list)
register_global_middlewares(dp, session_pool)


__all__ = (
    "bot",
    "storage",
    "dp",
    "session_pool",
    "engine",
    setup_logging()
)
