import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from src.tg_bot.common.bot_cmds_list import commands_for_private_channels
from src.tg_bot.handlers.user_private import user_private_router
from src.tg_bot.bot_database.engine import session_maker
from src.tg_bot.middlewares.db import DataBaseSession


bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage(),
                fsm_strategy=FSMStrategy.USER_IN_CHAT)


async def main() -> None:
    dp.include_router(user_private_router)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=commands_for_private_channels,
                              scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
