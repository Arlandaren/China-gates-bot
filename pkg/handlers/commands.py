from aiogram.types import Message,ReplyKeyboardRemove
from aiogram import Router
from aiogram.filters import CommandStart
from ..models.keyboards.keyboard import to_web_app,menu
from..models.repository.postgre import DB
r = Router()

@r.message(CommandStart())
async def start(msg:Message):
    user = await DB.get_user(msg.from_user.id)
    if user == None:
        await DB.create_user(msg.from_user.id,msg.from_user.username)
        start(msg)
    else:
        await msg.answer(f"Добро пожаловать, {msg.from_user.first_name} {msg.from_user.last_name}", reply_markup=ReplyKeyboardRemove())
        await msg.answer(f"баланс:{user["balance"]}", reply_markup=menu(msg.from_user.id))
