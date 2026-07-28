from typing import Dict
import pandas as pd

_cache: Dict[int, pd.DataFrame] = {}


def save_dataframe(chat_id: int, df: pd.DataFrame):
    _cache[chat_id] = df


def get_dataframe(chat_id: int):
    return _cache.get(chat_id)


def clear_dataframe(chat_id: int):
    _cache.pop(chat_id, None)