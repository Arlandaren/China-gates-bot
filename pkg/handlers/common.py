from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

r = Router()

@r.message(StateFilter(None))
async def warning(msg:Message,):
    await msg.answer("👋Привет \nЧтобы начать напиши /start⭐")