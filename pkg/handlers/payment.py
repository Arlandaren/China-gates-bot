from aiogram.types import CallbackQuery
from aiogram import Router,F,types,Bot
from ..models.keyboards.keyboard import catalogue
from ..models.repository.postgre import DB
import os
from .commands import start
r = Router()
bot = Bot(os.getenv("BOT_TOKEN"))

@r.callback_query(F.data == "payment_menu")
async def payment_menu(cb:CallbackQuery):
    await cb.message.answer("прайс", reply_markup=catalogue())


@r.callback_query(F.data == "buy_oneBooking")
async def buy_oneBooking(cb:types.CallbackQuery):
    await bot.send_invoice(chat_id=cb.message.chat.id,
                           title="Пополнение баланса",
                           description="1 бронирование",
                           provider_token=os.getenv("PAYMENT_TOKEN"),
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           prices=[
                                types.LabeledPrice(label="Товар", amount=10000),
                            ],
                           is_flexible=False,
                           start_parameter="one-month-subscription",
                           payload="invoice-payload")
    

@r.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@r.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer('Оплата прошла успешно, счет пополнен!')
    await DB.increase_balance_user(1,message.from_user.id)
    await start(message)
