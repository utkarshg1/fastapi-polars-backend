import polars as pl
from typing import Literal
from fastapi import HTTPException
from services.file_processing import get_df
from schemas.eda import ColumnSummary, SummaryResponse


def get_summary() -> SummaryResponse:
    df = get_df()
    assert type(df) == pl.DataFrame
    num_rows = df.height
    num_columns = df.width

    summaries = []
    for col in df.columns:
        summaries.append(
            ColumnSummary(
                column=col,
                dtype=str(df[col].dtype),
                missing=df[col].null_count(),
                unique=df[col].n_unique(),
            )
        )

    return SummaryResponse(
        num_rows=num_rows, num_columns=num_columns, columns=summaries
    )


def aggregate_by_column(
    cat_col: str,
    con_col: str,
    agg_func: Literal[
        "sum", "mean", "min", "max", "count", "n_unique", "len", "median", "std"
    ],
):
    df = get_df(lazy=True)  # LazyFrame
    if not isinstance(df, pl.LazyFrame):
        raise HTTPException(status_code=500, detail="Expected a LazyFrame.")

    schema = df.collect_schema()  # {col: dtype}

    # Column existence check
    if cat_col not in schema:
        raise HTTPException(
            status_code=400, detail=f"Categorical column '{cat_col}' not found."
        )
    if con_col not in schema:
        raise HTTPException(
            status_code=400, detail=f"Continuous column '{con_col}' not found."
        )

    # Type checks
    if schema[cat_col] not in (pl.Utf8, pl.Categorical):
        raise HTTPException(
            status_code=400,
            detail=f"Column '{cat_col}' must be string or categorical for grouping.",
        )

    if schema[con_col] not in (
        pl.Float64,
        pl.Float32,
        pl.Int64,
        pl.Int32,
        pl.Int16,
        pl.Int8,
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Column '{con_col}' must be numeric for aggregation.",
        )

    # Supported aggregations
    supported_aggs = {
        "sum": pl.sum,
        "mean": pl.mean,
        "min": pl.min,
        "max": pl.max,
        "count": pl.count,
        "n_unique": pl.n_unique,
        "median": pl.median,
        "std": pl.std,
    }

    agg_col_name = f"{con_col}_{agg_func}"

    result = (
        df.group_by(cat_col)
        .agg([supported_aggs[agg_func](con_col).alias(agg_col_name)])
        .with_columns(pl.col(agg_col_name).round(2))
        .sort(agg_col_name, descending=True)
        .collect()  # 🚀 Execute lazy pipeline
    )

    return {
        "group_by": cat_col,
        "aggregate": {con_col: agg_func},
        "data": result.to_dict(as_series=False),
    }
