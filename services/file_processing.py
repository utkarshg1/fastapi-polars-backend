import polars as pl
from fastapi import UploadFile
import os

CURRENT_FILE = "temp_uploads/current.csv"


async def save_and_read_csv(file: UploadFile) -> pl.DataFrame:
    contents = await file.read()
    with open(CURRENT_FILE, "wb") as f:
        f.write(contents)
    return pl.read_csv(CURRENT_FILE)


def get_df() -> pl.DataFrame:
    if not os.path.exists(CURRENT_FILE):
        raise RuntimeError("No file uploaded.")
    return pl.read_csv(CURRENT_FILE)
