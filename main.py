from aiogram import Dispatcher
from pkg import router,bot,bot_commands
import asyncio,logging,os
from pkg.models.repository.postgre import DB


async def main():
    logging.basicConfig(level=logging.INFO)
    await DB.InitDB(os.getenv("DB_CONN"))
    print("DB initialized")
    await bot.set_my_commands(bot_commands)
    dp = Dispatcher()
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())