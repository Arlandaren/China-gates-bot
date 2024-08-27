from aiogram import Router,F
from aiogram.types import Message
from aiogram.enums.content_type import ContentType
r = Router()

@r.message(F.web_app_data)
async def handle_web_app_data(msg: Message):
    web_app_data = msg.web_app_data
    print(web_app_data.data)
    await msg.answer(f"Received data: {web_app_data.data}")
