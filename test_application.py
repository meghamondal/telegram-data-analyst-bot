import asyncio
from telegram.ext import Application

from config import BOT_TOKEN


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    print("Initializing...")
    await app.initialize()
    print("Initialized!")

    await app.shutdown()
    print("Shutdown complete.")


asyncio.run(main())