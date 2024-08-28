from aiogram import Router,F
from aiogram.types import Message,CallbackQuery,ReplyKeyboardRemove
from ..models.repository.postgre import DB
from ..models.keyboards.keyboard import profile_menu, booking_button
from ..utils import order_analytic

r = Router()

@r.callback_query(F.data == "profile_menu")
async def profile(cb:CallbackQuery):
    user = await DB.get_user(cb.from_user.id)
    await cb.message.answer("Профиль:", reply_markup=ReplyKeyboardRemove())
    if user != None:
        await cb.message.answer(f"Баланс: {user["balance"]}\nДата регистрации: {user["joined_at"].strftime("%Y-%m-%d %H:%M:%S")}", reply_markup=profile_menu())
    else:
        await cb.message.answer(f"Внозникли проблемы с загрузкой вашего профиля")

@r.callback_query(F.data == "orders_menu")
async def booking_menu(cb: CallbackQuery):
    orders = await DB.get_orders(cb.from_user.id)
    if orders != None:
        stat = await order_analytic.analyse_order(orders)
        await cb.message.answer(f"Общее количество ващих заказов: {len(orders)}\nВыполненных заказов: {stat["finished"]}\nЗаказы ожидающие исполнения: {stat["pending"]}\nЗаказы в исполнении: {stat["active"]}")
    else:
        await cb.message.answer("К сожалению вы еще не совершали заказов\nЧтобы начать нажмите на кнопку", reply_markup=booking_button())
