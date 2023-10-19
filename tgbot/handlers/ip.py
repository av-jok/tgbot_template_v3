from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.markdown import hcode
from app.loader import dp
from app.middlewares import rate_limit

from sys import argv
import telnetlib


@rate_limit(5, "ip")
@dp.message_handler(commands="ip")
async def command_reg_handler(msg: types.Message):
    await msg.answer(main())


# edge - 10.0.18.33
# cisco - 10.0.24.164
# snr - 10.0.20.3

if not argv[1:]:
    exit("Не указан IP!")

HOST = argv[1]
user = "a.deripasko"
password = "Mrj0keer155"

tn = telnetlib.Telnet(HOST)
tn.set_debuglevel(0)


def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def main():
    try:
        type_msg, m, output = tn.expect([b"\*\*\*\*\*$", b"Username:", b"login:"], timeout=3)
        # print(output)
        tn.write(user.encode('ascii') + b"\n")
        tn.read_until(b"Password:")
        tn.write(password.encode('ascii') + b"\n")
        index, m, output = tn.expect([b">", b"#"])
        if index == 0:
            tn.write(b"enable\n")
            tn.read_until(b"Password")
            tn.write("swindler".encode('ascii') + b"\n")
            tn.read_until(b"#", timeout=5)

        if type_msg == 0:
            tn.write(to_bytes("terminal length 0"))
            tn.write(to_bytes("sh int br"))
            tn.write(to_bytes("sh ver"))
        elif type_msg == 1:
            tn.write(to_bytes("terminal length 0"))
            tn.write(to_bytes("sh int status"))
            tn.write(to_bytes("sh inv"))
            tn.write(to_bytes("sh ver"))
        elif type_msg == 2:
            tn.write(to_bytes("sh int eth status"))
            tn.write(to_bytes("sh ver"))

        tn.write(to_bytes("exit"))
        tn.interact()
        return tn.read_all().decode('ascii')
    except:
        return 'Ошибка'
