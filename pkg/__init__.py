from aiogram import Router,Bot
import os
from aiogram.types import BotCommand
from .handlers.common import r as common_router
from .handlers.commands import r as command_router
from .handlers.webapp import r as webapp_router
from .handlers.booking import r as booking_router
from .handlers.payment import r as payment_router
from .handlers.profile import r as profile_router

bot_commands = [
    BotCommand(command="start", description="Начать работу с ботом"),
    BotCommand(command="menu", description="Вернуться в меню"),
    BotCommand(command="cancel", description="Отменить действие")
]

router = Router()
bot = Bot(os.getenv("BOT_TOKEN"))
router.include_routers(command_router,webapp_router,booking_router,payment_router,profile_router)
router.include_router(common_router)