from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from ai_gpt.enums import Path
from utils import FileManager

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
        request_timeout=10,
    )
    msg_text = await FileManager.read(Path.MESSAGE.value, 'welcome_text')
    await message.answer(
        text=msg_text,
    )

# @command_router.message(F.photo)
# async def catch_photo(message: Message, bot: Bot):
#     photo = message.photo[-1]  # самая большая версия
#     file_info = await bot.get_file(photo.file_id)
#     file_path = file_info.file_path
#     file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_path}"
#     response = requests.get(file_url)
#     photo_image = Image.open(BytesIO(response.content))
#     photo_image.save("user_photo.png")  # временно сохраняем
#     msg_list = GPTMessage('card_prompt')
#     text = await FileManager.read('data', 'simple')
#     msg_list.update(GPTRole.USER, text)
#     response = await ai_client.request(msg_list, bot)
#     print(response)
#     await ai_client.generate_image(response, file_url)
#     await message.answer_photo(
#         photo=FSInputFile(os.path.join('data', 'final_card.png')),
#         caption=text,
#     )
