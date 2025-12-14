from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict, Any
import pandas as pd
import io

app = FastAPI(
    title="CSV Stats API",
    description="A simple API that accepts CSV file uploads and returns basic statistics for numeric columns",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CSV Stats API",
        "usage": "POST /upload-csv with a CSV file to get statistics"
    }


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a CSV file and get basic statistics for numeric columns.
    
    Args:
        file: CSV file to process
        
    Returns:
        JSON object containing statistics for each numeric column
    """
    # Validate file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    try:
        # Read the uploaded file content
        contents = await file.read()
        
        # Parse CSV using pandas
        df = pd.read_csv(io.BytesIO(contents))
        
        # Check if dataframe is empty
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Select only numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            return {
                "message": "No numeric columns found in the CSV file",
                "statistics": {}
            }
        
        # Compute statistics for numeric columns
        statistics = {}
        for column in numeric_columns:
            column_data = df[column].dropna()  # Remove NaN values for accurate statistics
            
            if len(column_data) > 0:
                statistics[column] = {
                    "count": int(column_data.count()),
                    "mean": float(column_data.mean()),
                    "median": float(column_data.median()),
                    "std": float(column_data.std()),
                    "min": float(column_data.min()),
                    "max": float(column_data.max())
                }
        
        return {
            "filename": file.filename,
            "total_rows": len(df),
            "numeric_columns": numeric_columns,
            "statistics": statistics
        }
        
    except HTTPException:
        raise
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
