from fastapi import APIRouter, HTTPException
from ..utils.data_loader import load_csv

router = APIRouter(prefix="/api", tags=["Categories"])


@router.get("/categories")
def get_categories():
    """Get category performance data."""
    try:
        df = load_csv("category_performance.csv")
        return df.to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
