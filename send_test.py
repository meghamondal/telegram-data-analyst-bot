import asyncio
from telegram import Bot
from config import BOT_TOKEN

CHAT_ID = 1125866093 

async def main():
    bot = Bot(BOT_TOKEN)

    print("Sending first...")
    await bot.send_message(chat_id=CHAT_ID, text="First")

    await asyncio.sleep(2)

    print("Sending second...")
    await bot.send_message(chat_id=CHAT_ID, text="Second")

    print("Done")

asyncio.run(main())