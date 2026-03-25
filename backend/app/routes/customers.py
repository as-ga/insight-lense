from fastapi import APIRouter, HTTPException
from ..utils.data_loader import load_csv

router = APIRouter(prefix="/api", tags=["Customers"])


@router.get("/top-customers")
def get_top_customers():
    """Get top 10 customers by total spend."""
    try:
        df = load_csv("top_customers.csv")
        # Convert boolean columns properly
        if "churned" in df.columns:
            df["churned"] = df["churned"].astype(bool)
        return df.to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
