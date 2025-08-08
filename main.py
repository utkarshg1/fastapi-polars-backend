import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api import upload, summary, aggregation

# Detect environment (default to "development")
ENV = os.getenv("ENV", "development").lower()

app = FastAPI(title="EDA App")

# Read allowed origins from env and split into list
allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root route
@app.get("/", include_in_schema=False)
def root():
    if ENV == "development":
        return {
            "message": "EDA App Backend is running 🚀",
            "environment": ENV,
            "version": "1.0.0",
            "routes": ["/upload", "/summary", "/aggregate", "/docs"],
        }
    else:
        # Minimal health check response for production
        return {"status": "ok"}


# Include routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(summary.router, prefix="/summary", tags=["Summary"])
app.include_router(aggregation.router, prefix="/aggregate", tags=["Aggregation"])
