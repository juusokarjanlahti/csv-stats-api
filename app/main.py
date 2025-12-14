from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import io

from app.services.csv_stats import compute_statistics

app = FastAPI(
    title="CSV Stats API",
    description="A simple API that accepts CSV file uploads and returns basic statistics for numeric columns",
    version="1.0.0",
)


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        statistics = compute_statistics(df)

        if not statistics:
            return {
                "message": "No numeric columns found in the CSV file",
                "statistics": {},
            }

        return {
            "filename": file.filename,
            "total_rows": len(df),
            "statistics": statistics,
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file format")
