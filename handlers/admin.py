import os

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from middleware import Admin
from utils import FileManager
from utils.enums import Path

admin_router = Router()
admin_router.message.middleware(Admin())


@admin_router.message(Command('set'))
async def admin_set(message: Message, command: CommandObject):
    file_list = [file.rsplit('.', 1)[0] for file in os.listdir(Path.PROMPT.value)]
    msg_text = '\n'.join(file_list)
    if command.args:
        file_name, prompt = command.args.split(' ', 1)
        if file_name in file_list:
            await FileManager.write(Path.PROMPT.value, file_name, data=prompt)
            msg_text = 'Done!'
    await message.answer(
        text=msg_text,
    )


@admin_router.message(Command('get'))
async def admin_get(message: Message, command: CommandObject):
    file_list = [file.rsplit('.', 1)[0] for file in os.listdir(Path.PROMPT.value)]
    msg_text = '\n'.join(file_list)
    if command.args:
        file_name = command.args.strip()
        if file_name in file_list:
            msg_text = await FileManager.read(Path.PROMPT.value, file_name, with_kwargs=False)
    await message.answer(
        text=msg_text,
    )
