from fastapi import APIRouter, Query, HTTPException
from typing import Literal
from services.eda import aggregate_by_column

router = APIRouter()


@router.get("/")
def aggregate(
    cat_col: str = Query(...),
    con_col: str = Query(...),
    agg_func: Literal[
        "sum", "mean", "min", "max", "count", "n_unique", "median", "std"
    ] = Query(...),
):
    try:
        return aggregate_by_column(cat_col, con_col, agg_func)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
