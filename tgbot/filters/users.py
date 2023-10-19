from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class UserFilter(BaseFilter):
    is_user: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.user_ids) == self.is_user
