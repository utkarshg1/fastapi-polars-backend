# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import upload, summary, aggregation

app = FastAPI(title="EDA App")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(summary.router, prefix="/summary", tags=["Summary"])
app.include_router(aggregation.router, prefix="/aggregate", tags=["Aggregation"])
