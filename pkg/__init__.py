from aiogram import Router,Bot
import os
from .handlers.common import r as common_router
from .handlers.commands import r as command_router
from .handlers.webapp import r as webapp_router
from .handlers.booking import r as booking_router
router = Router()
bot = Bot(os.getenv("BOT_TOKEN"))
router.include_routers(command_router,webapp_router,booking_router)
router.include_router(common_router)