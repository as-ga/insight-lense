from pathlib import Path
import pandas as pd
from fastapi import HTTPException

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "../data" / "processed"


def load_csv(filename: str) -> pd.DataFrame:
    """Load CSV file from processed data directory."""
    print(f"Loading data from: {DATA_DIR / filename}")
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"Data file not found: {filename}")
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
