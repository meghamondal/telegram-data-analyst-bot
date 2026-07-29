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

    if filepath.endswith(".csv"):
        return pd.read_csv(filepath)

    if filepath.endswith(".xlsx"):
        return pd.read_excel(filepath)

    if filepath.endswith(".xls"):
        return pd.read_excel(filepath)

    raise ValueError(f"Unsupported file type: {filepath}")


def dataframe_summary(df):
    """
    Summary and full data for the LLM.
    """
    csv_data = df.to_csv(index=False)
    # truncate if it's too massive, e.g., > 100k chars to be safe for LLM context
    limit = 500000
    if len(csv_data) > limit:
        csv_data = csv_data[:limit] + "\n... (truncated)"


    return f"Shape: {df.shape}\nColumns: {list(df.columns)}\nData:\n{csv_data}"