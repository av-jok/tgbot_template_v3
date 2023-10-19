from typing import Union
from aiogram import types
from aiogram.dispatcher.filters import Command
from app.loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    # markup = await categories_keyboard()
    pass
