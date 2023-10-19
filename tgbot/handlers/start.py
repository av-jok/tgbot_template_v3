from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hcode
from tgbot.config import commands


start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(msg: Message):
    await msg.answer(
        f'Привет, {msg.from_user.full_name}!\n Пройди регистрацию /reg\n Если не знаешь для чего она - 🖕',
        reply_markup=ReplyKeyboardRemove()
    )


@start_router.message(Command("id"))
async def command_reg_handler(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")


@start_router.message(Command("help"))
async def command_help_handler(message: Message):
    # Generates a list
    answer = ["Available commands: "]
    for command, description in commands:
        answer.append(hcode(f"/{command}") + f" — {description}")

    await message.answer("\n".join(answer))
