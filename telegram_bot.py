import asyncio
import json
import logging
import traceback
from telegram.error import NetworkError

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

from config import BOT_TOKEN, BASE_URL
from logger import log_event
from agent_runner import run_agent

# Configure HTTP client
request = HTTPXRequest(
    connection_pool_size=1,
    connect_timeout=30,
    read_timeout=30,
    write_timeout=30,
    pool_timeout=30,
)

# ----------------------------
# /start command
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your Data Analyst Bot."
    )


# ----------------------------
# Handle user messages
# ----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    question = update.message.text


    log_event(
        "question",
        {
            "chat_id": chat_id,
            "question": question,
        },
    )

    try:
        answer = await asyncio.to_thread(
            run_agent,
            chat_id,
            question,
        )

        # The instructor confirmed we must always include log_url!
        response = {
            "answer": answer,
            "log_url": f"{BASE_URL}/run.jsonl",
        }


        log_event(
            "answer",
            response,
        )

        for attempt in range(3):
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=json.dumps(response),
                )
                print("Telegram reply sent successfully.")
                break

            except NetworkError as e:
                print(f"Telegram network error (attempt {attempt + 1}/3): {e}")

                if attempt == 2:
                    traceback.print_exc()
                else:
                    await asyncio.sleep(2)

            except Exception as e:
                print("\n" + "=" * 60)
                print("FAILED TO SEND TELEGRAM MESSAGE")
                print("TYPE:", type(e))
                print("ERROR:", repr(e))
                traceback.print_exc()
                print("=" * 60 + "\n")
                break
    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR INSIDE handle_message()")
        print("TYPE:", type(e))
        print("ERROR:", repr(e))

        if e.__cause__:
            print("CAUSE:", repr(e.__cause__))

        if e.__context__:
            print("CONTEXT:", repr(e.__context__))

        traceback.print_exc()
        print("=" * 60 + "\n")

        try:
            await update.message.reply_text(
                json.dumps(
                    {
                        "answer": "Internal server error.",
                        "log_url": f"{BASE_URL}/run.jsonl",
                    }
                )
            )
        except Exception:
            traceback.print_exc()


# ----------------------------
# Build application
# ----------------------------
application = (
    Application.builder()
    .token(BOT_TOKEN)
    .request(request)
    .build()
)

application.add_handler(
    CommandHandler(
        "start",
        start,
    )
)

application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message,
    )
)