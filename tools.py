from pathlib import Path
import requests
import pandas as pd

from config import DATASET_FOLDER


def ensure_dataset_folder():
    Path(DATASET_FOLDER).mkdir(parents=True, exist_ok=True)


def download_file(url: str) -> str:
    """
    Download a file into datasets/.
    Returns the local file path.
    """
    ensure_dataset_folder()

    filename = url.split("/")[-1].split("?")[0]

    filepath = Path(DATASET_FOLDER) / filename

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return str(filepath)


def load_dataframe(filepath: str):
    """
    Load CSV or Excel.
    """

    if filepath.endswith(".xlsx") or filepath.endswith(".xls"):
        return pd.read_excel(filepath)

    # Default to CSV instead of crashing if the URL doesn't have a perfect .csv extension
    try:
        return pd.read_csv(filepath)
    except Exception:
        # If it fails as CSV, try excel just in case
        return pd.read_excel(filepath)


def dataframe_summary(df):
    """
    Summary and full data for the LLM.
    """
    csv_data = df.to_csv(index=False)
    return f"Shape: {df.shape}\nColumns: {list(df.columns)}\nData:\n{csv_data}"