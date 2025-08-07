import polars as pl
from fastapi import UploadFile, HTTPException
import os
from core.config import CURRENT_FILE, UPLOAD_DIR


async def save_and_read_csv(file: UploadFile) -> pl.DataFrame:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    contents = await file.read()

    with open(CURRENT_FILE, "wb") as f:
        f.write(contents)
    return pl.read_csv(CURRENT_FILE)


def get_df() -> pl.DataFrame:
    if not os.path.exists(CURRENT_FILE):
        raise HTTPException(
            status_code=400, detail="No file uploaded. Please upload a CSV first."
        )
    return pl.read_csv(CURRENT_FILE)
