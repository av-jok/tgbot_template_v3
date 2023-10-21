import asyncio
import logging
from typing import List

import betterlogging as bl
from tgbot.loader import dp, bot
from tgbot.services import broadcaster
from tgbot.config import config


async def on_startup(admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот запущен")


async def on_shutdown(admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот выключается")


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


async def main():

    setup_logging()

    await on_startup(config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был выключен!")
