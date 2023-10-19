import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token="1323680830:AAHMuqFWXGsyYuab9rTXtVfjUYEd1iDm2Xc")
dp = Dispatcher(bot)


@dp.callback_query_handler()
async def button_press(callback: CallbackQuery):
    logging.info(f"{callback.message}")


@dp.message_handler(commands=['start'])
async def start(message: Message):
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f"Text", callback_data="text")
    )
    await message.answer("text", reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
