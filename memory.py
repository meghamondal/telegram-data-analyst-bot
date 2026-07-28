from collections import defaultdict

# Stores conversation history per Telegram chat
_chat_history = defaultdict(list)


def add_message(chat_id: int, role: str, content: str):
    """
    role = "user" or "assistant"
    """
    _chat_history[chat_id].append(
        {
            "role": role,
            "content": content,
        }
    )

    # Keep only the latest 10 messages
    _chat_history[chat_id] = _chat_history[chat_id][-10:]


def get_history(chat_id: int):
    return _chat_history[chat_id]


def clear_history(chat_id: int):
    _chat_history.pop(chat_id, None)