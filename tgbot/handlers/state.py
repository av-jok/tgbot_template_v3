from loguru import logger
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from app.loader import dp, bot
from app.config import *
# from app.middlewares import rate_limit
from app.states.state import PhotoDownload
from typing import Union


# обработчик выхода из машины состояний
@dp.message_handler(filters.IDFilter(user_id=USERS), state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('отменена!')


@dp.message_handler(filters.IDFilter(user_id=USERS), commands="file")
async def command_reg_handler(message: types.Message):
    await message.answer("Введите инвентарный №")
    await PhotoDownload.id.set()


@dp.message_handler(filters.IDFilter(user_id=USERS), state=PhotoDownload.id)
async def get_street(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer("Отлично! Теперь введите адрес.")
    await PhotoDownload.address.set()  # либо же UserState.adress.set()


@dp.message_handler(filters.IDFilter(user_id=USERS), state=PhotoDownload.address)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Отлично! Теперь кидай фото.")
    await PhotoDownload.photo.set()  # либо же UserState.adress.set()


# @dp.message_handler(state=PhotoDownload.photo)
# async def get_address(message: types.Message, state: FSMContext):
#     await state.update_data(address=message.text)
#     data = await state.get_data()
#     await message.answer(f"Инв: {data['id']}\n"
#                          f"Адрес: {data['address']}\n"
#                          f"Фото: {data['photo']}\n"
#                          )
#     await state.finish()


# @rate_limit(5)
@dp.message_handler(filters.IDFilter(user_id=USERS), state=PhotoDownload.photo, content_types=types.ContentType.PHOTO)
async def handle_albums(message: types.Message, state: FSMContext):
    """This handler will receive a complete album of any type."""
    await state.update_data(photo=message.photo[-1].file_unique_id)
    data = await state.get_data()

    filename = data['id'] + '-' + message.photo[-1].file_unique_id + '.jpg'
    text = (f"Инв № - {data['id']}\n"
            f"Файл - {filename}\n"
            f"Адрес: {data['address']}\n"
            f"Отправил - {message.chat.first_name}"
            )
    logger.debug("Downloading photo start")

    downloaded_file = bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id))
    await message.photo[-1].download(destination_file=upload_dir_photo + filename)
    await download_file(downloaded_file, filename, message)
    logger.debug("Downloading photo end")
    await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text)
    # await bot.send_message('252810436', caption=text)
    # await message.forward('252810436')
    await message.answer("Принято " + filename)

    await state.finish()


# @dp.message_handler(filters.IDFilter(user_id=USERS), state=PhotoDownload.photo, content_types=types.ContentType.PHOTO)
# async def handle_albums(message: types.Message, state: FSMContext):
#     logger.debug("Downloading photo")
#     # file_info = await bot.get_file(message.photo[-1].file_id)
#     if message.reply_to_message:
#         if re.match('^\\d{5}$', message.reply_to_message.text):
#             text = re.search('^\\d{5}$', message.reply_to_message.text)
#             text = str(text[0])
#
#             filename = text + '-' + message.photo[-1].file_unique_id + '.jpg'
#             text = (f"Инв № - {text}\n"
#                     f"Файл - {filename}\n"
#                     f"Отправил - {message.reply_to_message.from_user.first_name}"
#                     )
#             logger.debug("Downloading photo start")
#
#             downloaded_file = bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id))
#             # src = '../photos/' + filename
#             # with open(src, 'wb') as new_file:
#             #     new_file.write(downloaded_file)
#             await message.photo[-1].download(destination_file='../photos/' + filename)
#             await download_file(downloaded_file, filename, message)
#             logger.debug("Downloading photo end")
#             await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text)
#             # await bot.send_message('252810436', caption=text)
#             # await message.forward('252810436')
#             await message.answer("Принято " + filename)
#         else:
#             await message.answer("Фотография должна быть ответом на Инв свича")
#     else:
#         await message.answer("Фотография должна быть ответом на Инв свича")
#
#     """This handler will receive a complete album of any type."""
#     await state.update_data(photo=message.photo[0].file_id)
#     data = await state.get_data()
#     media_group = types.MediaGroup()
#
#     for obj in album:
#         if obj.photo:
#             file_id = obj.photo[-1].file_id
#         else:
#             file_id = obj[obj.content_type].file_id
#
#         try:
#             # We can also add a caption to each file by specifying `"caption": "text"`
#             media_group.attach({"media": file_id, "type": obj.content_type})
#         except ValueError:
#             return await message.answer("This type of album is not supported by aiogram.")
#
#     await message.answer(f"Инв: {data['id']}\n"
#                          f"Адрес: {data['address']}\n"
#                          f"Фото: {data['photo']}\n"
#                          )
#     await message.answer_media_group(media_group)
#     await state.finish()

# @dp.message_handler(state=PhotoDownload.photo)
# async def process_photo(message: types.Message, state: FSMContext):
#
#     await state.update_data(photo=message.photo[0].file_id)
#     data = await state.get_data()
#     await message.answer(f"Инв: {data['id']}\n"
#                          f"Адрес: {data['address']}\n"
#                          f"Фото: {data['photo']}\n"
#                          )
#     await state.finish()


async def download_file(file: types.File, name: str, message: types.Message):
    # file_path = file.file_path
    destination = upload_dir_photo + name
    image_id = message.photo[len(message.photo) - 1].file_id
    file_path = (await bot.get_file(image_id)).file_path

    await bot.download_file(file_path, destination)
