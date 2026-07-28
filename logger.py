import json
from datetime import datetime
from pathlib import Path

from config import LOG_FILE


def log_event(event_type: str, data: dict):
    """
    Append one JSON object to the log file.
    Each line in the file is a separate JSON object.
    """

    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "data": data
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")