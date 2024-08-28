from aiogram.types import Message,ReplyKeyboardRemove,CallbackQuery
from aiogram import Router,F
from aiogram.filters import CommandStart
from ..models.keyboards.keyboard import menu
from..models.repository.postgre import DB
from typing import Union
from aiogram.filters import StateFilter
r = Router()

@r.message(CommandStart() or F.text == "/menu")
async def start(msg:Message):
    user = await DB.get_user(msg.from_user.id)
    if user == None:
        await DB.create_user(msg.from_user.id,msg.from_user.username)
        start(msg)
    else:
        await msg.answer(f"Добро пожаловать, {msg.from_user.first_name} {msg.from_user.last_name}", reply_markup=ReplyKeyboardRemove())
        await msg.answer(f"баланс :{user["balance"]}", reply_markup=menu(msg.from_user.id))

@r.callback_query(F.data=="cancel")
@r.message(F.text == "/cancel")
async def cancel_handler(query_or_message: Union[CallbackQuery, Message]): 
    
    # current_state = await state.get_state()
    # if current_state is None:
    #     await query_or_message.answer("🕐На данный момент не выполняются какие-либо действия🕑",reply_markup=to_menu())
    #     return
    if isinstance(query_or_message, CallbackQuery):
        await query_or_message.message.delete()
        await query_or_message.message.answer("❌Действие отмененно❗", reply_markup=ReplyKeyboardRemove())
        await start(query_or_message.message)
    elif isinstance(query_or_message, Message):

        await query_or_message.answer("❌Действие отмененно❗", reply_markup=ReplyKeyboardRemove())
        await start(query_or_message)