import asyncio
import logging
import src.tg_bot.bot as bot

logging.basicConfig(level=logging.INFO)
asyncio.run(bot.main())
