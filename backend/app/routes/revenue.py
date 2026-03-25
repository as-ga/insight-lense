from fastapi import APIRouter, HTTPException
from ..utils.data_loader import load_csv

router = APIRouter(prefix="/api", tags=["Revenue"])


@router.get("/revenue")
def get_revenue():
    """Get monthly revenue trend data."""
    try:
        df = load_csv("monthly_revenue.csv")
        return df.to_dict(orient="records")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
