import asyncio
from tgbot.loader import dp, bot
from tgbot.services import broadcaster
from tgbot.config import config


async def on_startup(admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот запущен")


async def on_shutdown(admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот выключается")


async def main():

    await on_startup(config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Exit')
