import re
import os
from loguru import logger
from requests import request
from aiogram import types, Router, F
from aiogram import filters
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from typing import Optional

from tgbot.config import Config, HEADERS, upload_dir_photo, upload_dir_data
from tgbot.filters.users import UserFilter

# from pprint import pprint

any_router = Router()
any_router.message.filter(UserFilter())


class IdButton(CallbackData, prefix="action"):
    action: str
    value: Optional[int] = None


async def send_photo_by_id(callback: types.CallbackQuery, photos, photos2):

    media = MediaGroupBuilder(caption="Media group caption")

    if photos is not None:
        for iterator in photos:
            img_data = request("GET", iterator['image'], headers=HEADERS, data='').content
            filename = upload_dir_data + str(iterator['object_id']) + "_" + str(iterator['pid']) + ".jpg"
            with open(filename, 'wb') as photo:
                photo.write(img_data)
            media.add(type="photo", media=FSInputFile(filename))

    if photos2 is not None:
        for iterator in photos2:
            filename = upload_dir_photo + str(iterator['name'])
            # pprint(filename)
            media.add(type="photo", media=FSInputFile(filename))

    # await callback.message.reply_media_group(media=media)
    await callback.send_media_group(media=media.build())
    return True


@any_router.callback_query(IdButton.filter())
async def callbacks_num_change_fab(callback: types.CallbackQuery, callback_data: IdButton):

    switch = callback_data.value
    # pprint(switch.images)
    # pprint(switch.images2)
    logger.debug(f"action == {callback_data.action}")

    if callback_data.action == "ping":
        user = callback_data.value
        await callback.message.edit_text(f"Итого: {user}")
    await callback.answer()

    if callback_data.action == 'photo':
        if switch.images or switch.images2:
            await send_photo_by_id(callback, switch.images, switch.images2)
            await callback.answer()
        else:
            await callback.answer(
                text=f'Фотографии не найдены',
                show_alert=True
            )
            await callback.answer()
        return True

    if callback_data.action == 'ping':
        hostname = switch.ip
        host = "is down!"
        response = os.system("ping -c 1 -W 1 " + hostname + "> /dev/null")
        if response == 0:
            host = "is up!"

        await callback.send_message(callback.from_user.id, f"Switch: {switch.name} {host}", reply_to_message_id=callback.message.message_id)
        await callback.answer()
        return True

    await callback.send_message(callback.from_user.id, f"id: {callback_data.value}\naction: {callback_data.action}")
    await callback.answer()


@any_router.message.handlers(F.photo)
async def scan_message(message: Message):
    if message.reply_to_message and re.match('^\\d{5}$', message.reply_to_message.text):
        is_exist = False
        text = re.search('^\\d{5}$', message.reply_to_message.text)
        text = str(text[0])

        filename = text + '-' + message.photo[-1].file_unique_id + '.jpg'
        text_out = (f"Инв № - {text}\n"
                    f"Файл - {filename}\n"
                    f"Отправил - {message.reply_to_message.from_user.first_name}"
                    )
        # logger.debug("Downloading photo start")

        # select_all_rows = f"SELECT * FROM `bot_photo` WHERE tid='{message.photo[-1].file_unique_id}' AND sid='{text}' LIMIT 1"
        # cur = db.query(select_all_rows)
        # row = cur.fetchall()

        # rows = query_select(select_all_rows)

        # if not row:
        #     insert_query = f"INSERT INTO `bot_photo` (sid, name, tid, file_id) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}', '{message.photo[-1].file_id}');"
        #     cur = db.query(insert_query)
        #     cur.commit()
        #     is_exist = True
        #     logger.debug(f"is_exist = {is_exist}")

        # if not rows:
        #     insert_query = f"INSERT INTO `bot_photo` (sid, name, tid, file_id) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}', '{message.photo[-1].file_id}');"
        #     is_exist = query_insert(insert_query)
        #     logger.debug(f"is_exist = {is_exist}")

        # await message.photo[-1].download(destination_file=upload_dir_photo + filename)
        # destination = upload_dir_photo + filename
        # image_id = message.photo[len(message.photo) - 1].file_id
        # file_path = (await bot.get_file(image_id)).file_path
        # await bot.download_file(file_path, destination)

        if is_exist:
            if message.from_user.id != 252810436:
                await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text_out)
            await message.answer("Принято " + filename)
        else:
            await message.answer("Такое фото уже есть в базе")
    else:
        await message.answer("Фотография должна быть ответом на Инв свича")


@any_router.message(F.text)
async def photo_msg(message: Message):
    if len(message.text) < 4:
        await message.answer("Запрос должен быть длиннее")
        return False

    url = Config.misc.netbox_url + "api/dcim/devices/?q=" + message.text
    response = request("GET", url, headers=HEADERS, data='')

    json = response.json()

    if json['count'] > 0:
        for iterator in json['results']:
            switch = sw(iterator['id'])

            match switch.status:
                case 'Active':
                    status = '🟢'
                case 'Offline':
                    status = '🔴'
                case 'Inventory':
                    status = '📦'
                case 'Decommissioning':
                    status = '⚰️'
                case _:
                    status = switch.status

            msg = (
                f"Адрес: {switch.address}\n"
                f"{switch.rack}\n\n"
                f"Имя: {switch.name} {status}\n"
                f"Инв № : {switch.id}\n"
                f"{switch.device_type}\n"
                f"{switch.ip}\n\n"    
                f"{switch.comments}"
            )
            builder = InlineKeyboardBuilder()
            builder.button(
                text="Device", callback_data=IdButton(
                    url=switch.url
                )
            )
            builder.button(
                text="Ping", callback_data=IdButton(
                    action="ping",
                    value=switch.nid
                )
            )
            builder.button(
                text="Фото", callback_data=IdButton(
                    action="photo",
                    value=switch.nid
                )
            )
            builder.adjust(3)
            logger.debug(f"{switch.nid}")

            await message.answer(msg, reply_markup=builder.as_markup())
    else:
        await message.answer("Ничего не найдено")
