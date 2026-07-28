import os
from dotenv import load_dotenv


load_dotenv(override=True)
BOT_TOKEN = os.getenv("BOT_TOKEN")
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")

DATASET_FOLDER = "datasets"
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "run.jsonl")
