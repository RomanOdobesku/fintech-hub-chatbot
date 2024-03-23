import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from common.bot_cmds_list import private
from handlers.user_private import user_private_router
from bot_database.engine import session_maker
from middlewares.db import DataBaseSession


bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage(),
                fsm_strategy=FSMStrategy.USER_IN_CHAT)
dp.include_router(user_private_router)


async def main() -> None:
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
