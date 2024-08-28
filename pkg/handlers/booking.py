from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from ..models.repository.postgre import DB
from ..models.keyboards.keyboard import to_web_app,to_payment

r = Router()

@r.callback_query(F.data == "booking")
async def booking(cb:CallbackQuery):
    user_balance = await DB.get_balance_user(cb.from_user.id)

    if user_balance > 0:
        await cb.message.answer("Чтобы начать нажмите на кнопку", reply_markup=to_web_app())
    else:
        await cb.message.answer("Чтобы продолжить - пополните баланс", reply_markup=to_payment())

