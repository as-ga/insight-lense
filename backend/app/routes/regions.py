from fastapi import APIRouter, HTTPException
from ..utils.data_loader import load_csv

router = APIRouter(prefix="/api", tags=["Regions"])


@router.get("/regions")
def get_regions():
    """Get regional analysis data."""
    try:
        df = load_csv("regional_analysis.csv")
        return df.to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
