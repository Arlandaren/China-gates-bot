from aiogram import Router,F
from aiogram.types import Message,ReplyKeyboardRemove,WebAppData
from aiogram.enums.content_type import ContentType
from..models.repository.postgre import DB
from .commands import start
import json
r = Router()

@r.message(F.web_app_data)
async def handle_web_app_data(msg:Message):
    try:
        data = json.loads(msg.web_app_data.data)
    except json.JSONDecodeError:
        await msg.answer("Ошибка при обработке данных. Проверьте правильность ввода.", reply_markup=ReplyKeyboardRemove())
        await start(msg)
        return

    login = data.get("login")
    password = data.get("password")
    truck_grnz = data.get("truck_grnz")
    trunk_grnz = data.get("trunk_grnz")
    driver_email = data.get("driver_email")
    driver_phone = data.get("driver_phone")

    if await DB.create_order(
        msg.from_user.id,
        login,
        password,
        truck_grnz,
        trunk_grnz,
        driver_email,
        driver_phone
    ):
        await DB.decrease_balance_user(1,msg.from_user.id)
        await msg.answer("Заказ успешно принят, вы можете отслеживать статус в профиле", reply_markup=ReplyKeyboardRemove())

        await start(msg)
    else:
        await msg.answer("Ошибка с обработкой заказа, попробуйте снова и проверьте правильность введенных данных", reply_markup=ReplyKeyboardRemove())
        await start(msg)

