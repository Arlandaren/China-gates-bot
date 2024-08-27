from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import WebAppInfo

def to_web_app():
    webAppInfo = WebAppInfo(url="https://arlandaren.github.io/rosgranstroy_front/")

    kb = ReplyKeyboardBuilder()
    kb.button(text="начать", web_app=webAppInfo)

    return kb.as_markup(resize_keyboard=True)

def menu(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Забронировать", callback_data=f"booking_{user_id}")

    return kb.as_markup()