from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from tgbot.config import config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from infrastructure.database.setup import create_engine, create_session_pool


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
    "engine"
)
