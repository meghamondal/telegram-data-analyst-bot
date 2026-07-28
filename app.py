from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from config import LOG_FILE
from telegram_bot import application


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start Telegram bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("Telegram bot started.")

    yield

    # Stop Telegram bot
    await application.updater.stop()
    await application.stop()
    await application.shutdown()

    print("Telegram bot stopped.")


app = FastAPI(
    title="Telegram Data Analyst Bot",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "message": "Telegram Data Analyst Bot is running."
    }


@app.get("/health")
def health():
    return {
        "ok": True
    }


@app.get("/run.jsonl")
def run_log():

    log_path = Path(LOG_FILE)

    if not log_path.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch()

    return FileResponse(
        path=log_path,
        media_type="application/json",
        filename="run.jsonl",
    )