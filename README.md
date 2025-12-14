# csv-stats-api

A small HTTP API that accepts a CSV file upload, computes basic statistics for numeric columns, and returns the result as JSON.

## Features

- ✅ Accepts CSV file uploads via POST endpoint
- ✅ Automatically identifies numeric columns
- ✅ Computes basic statistics: count, mean, median, standard deviation, min, max
- ✅ Returns results as JSON
- ✅ Built with FastAPI for automatic API documentation

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### GET `/`
Returns API information.

```bash
curl http://localhost:8000/
```

#### GET `/health`
Check system health status.

```bash
curl http://localhost:8000/health
```

#### POST `/upload-csv`
Upload a CSV file and get statistics for numeric columns.

```bash
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@your_file.csv"
```

### Example

Sample CSV file (`data.csv`):
```csv
name,age,salary,score
Alice,30,50000,85.5
Bob,25,45000,92.0
Charlie,35,60000,78.5
```

Request:
```bash
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@data.csv"
```

Response:
```json
{
  "filename": "data.csv",
  "total_rows": 3,
  "numeric_columns": ["age", "salary", "score"],
  "statistics": {
    "age": {
      "count": 3,
      "mean": 30.0,
      "median": 30.0,
      "std": 5.0,
      "min": 25.0,
      "max": 35.0
    },
    "salary": {
      "count": 3,
      "mean": 51666.67,
      "median": 50000.0,
      "std": 7637.63,
      "min": 45000.0,
      "max": 60000.0
    },
    "score": {
      "count": 3,
      "mean": 85.33,
      "median": 85.5,
      "std": 6.76,
      "min": 78.5,
      "max": 92.0
    }
  }
}
```

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`

## Running Tests

```bash
pytest test_main.py -v
```

## Error Handling

The API handles various error cases:

- **Invalid file format**: Returns 400 if file is not a CSV
- **Empty CSV**: Returns 400 if CSV file is empty
- **No numeric columns**: Returns 200 with empty statistics
- **Parse errors**: Returns 400 if CSV format is invalid

## Out of Scope

The following features are explicitly out of scope:

- Authentication
- Database
- Frontend
- Streaming
- Async optimization
- Large file handling

## Technology Stack

- **FastAPI**: Modern web framework for building APIs
- **Pandas**: Data manipulation and statistics computation
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework

## Code style and formatting

- **Black**: Python Code formatter