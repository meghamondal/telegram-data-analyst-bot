# Telegram Data Analyst Bot

An advanced, AI-powered Telegram bot designed to act as a robust data analyst. This bot can securely ingest public datasets, interpret complex analytical questions, and mathematically compute exact answers by dynamically writing and executing its own Python code.

## Key Features

* **Agentic Code Interpreter:** Instead of guessing or hallucinating math answers, the AI writes dynamic Python scripts using the `pandas` library to calculate mathematically perfect answers directly from the dataset.
* **Intelligent State Management:** Supports multi-turn conversations and dataset caching. The bot smartly recognizes when a task is finished and automatically wipes its memory to prevent context bleeding between independent tasks.
* **Robust File Handling:** Aggressively fetches and parses CSV and Excel files from public URLs, even handling tricky API endpoints that lack standard file extensions.
* **Strict JSON Formatting:** Wraps all final answers in strict JSON formats required by automated grading scripts, automatically stripping markdown or conversational filler.
* **Cloud Ready:** Built with FastAPI and designed for zero-downtime deployment on Render. Includes a `/health` endpoint to support 24/7 uptime monitoring via services like UptimeRobot.

## Architecture & Technologies

* **Framework:** `FastAPI` (for webhooks and log hosting) + `python-telegram-bot` (for Telegram API integration)
* **AI Provider:** `gpt-4o-mini` (via OpenAI-compatible proxy)
* **Data Processing:** `pandas`
* **Deployment:** Render (Web Service)

## Project Structure

* `telegram_bot.py`: Handles Telegram API integration, message parsing, and strict JSON response formatting.
* `agent_runner.py`: The brain of the bot. Manages the LLM prompt, Code Interpreter execution (`exec()`), and intermediate bypass logic.
* `tools.py`: Handles robust downloading and parsing of datasets from the web.
* `memory.py` & `dataset_cache.py`: Manages multi-turn conversation history and dataset caching, including aggressive wipe logic.
* `app.py`: FastAPI application serving the `/run.jsonl` logs and managing the bot lifecycle.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd telegram_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Create a `.env` file in the root directory with the following variables:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   AIPROXY_TOKEN=your_ai_api_token
   BASE_URL=your_render_url
   ```

4. **Run Locally:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 10000
   ```

## Logging

The bot maintains a persistent JSONL log of all incoming questions and outgoing answers, which is publicly accessible via the `/run.jsonl` endpoint for automated evaluation scripts.
