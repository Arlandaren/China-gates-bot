from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from ..models.repository.postgre import DB
from ..models.keyboards.keyboard import to_web_app

r = Router()

@r.callback_query(F.data.startswith("booking_"))
async def booking(cb:CallbackQuery):
    _,user_id = cb.data.split("_")
    user = await DB.get_user(user_id)

    if user["balance"] > 0:
        await cb.answer("Чтобы начать нажмите на кнопку", reply_markup=to_web_app())
    else:
        cb.message.answer("Чтобы продолжить пополните баланс")