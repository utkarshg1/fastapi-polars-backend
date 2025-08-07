# main.py
from fastapi import FastAPI
from api import upload, summary, aggregation

app = FastAPI(title="EDA App")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(summary.router, prefix="/summary", tags=["Summary"])
app.include_router(aggregation.router, prefix="/aggregate", tags=["Aggregation"])
