from telegram import Bot
from config import BOT_TOKEN
import asyncio


async def main():
    bot = Bot(BOT_TOKEN)

    me = await bot.get_me()

    print(me)


asyncio.run(main())