import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "usage" in response.json()


def test_upload_csv_with_numeric_data():
    """Test uploading a CSV file with numeric columns"""
    csv_content = b"""name,age,score
Alice,30,85.5
Bob,25,92.0
Charlie,35,78.5
"""
    
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "filename" in data
    assert data["filename"] == "test.csv"
    assert "total_rows" in data
    assert data["total_rows"] == 3
    assert "numeric_columns" in data
    assert set(data["numeric_columns"]) == {"age", "score"}
    assert "statistics" in data
    
    # Check age statistics
    assert "age" in data["statistics"]
    assert data["statistics"]["age"]["count"] == 3
    assert data["statistics"]["age"]["mean"] == 30.0
    assert data["statistics"]["age"]["min"] == 25
    assert data["statistics"]["age"]["max"] == 35
    
    # Check score statistics
    assert "score" in data["statistics"]
    assert data["statistics"]["score"]["count"] == 3
    assert abs(data["statistics"]["score"]["mean"] - 85.333) < 0.01


def test_upload_csv_no_numeric_columns():
    """Test uploading a CSV file with no numeric columns"""
    csv_content = b"""name,city
Alice,New York
Bob,London
Charlie,Paris
"""
    
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert "No numeric columns found" in data["message"]
    assert data["statistics"] == {}


def test_upload_csv_with_nan_values():
    """Test uploading a CSV file with NaN values"""
    csv_content = b"""name,age,score
Alice,30,85.5
Bob,,92.0
Charlie,35,
"""
    
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    # Age should have 2 valid values
    assert data["statistics"]["age"]["count"] == 2
    assert data["statistics"]["age"]["mean"] == 32.5
    
    # Score should have 2 valid values
    assert data["statistics"]["score"]["count"] == 2


def test_upload_non_csv_file():
    """Test uploading a non-CSV file"""
    txt_content = b"This is not a CSV file"
    
    files = {"file": ("test.txt", io.BytesIO(txt_content), "text/plain")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 400
    assert "must be a CSV file" in response.json()["detail"]


def test_upload_empty_csv():
    """Test uploading an empty CSV file"""
    csv_content = b""
    
    files = {"file": ("empty.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_upload_csv_headers_only():
    """Test uploading a CSV file with only headers"""
    csv_content = b"name,age,score\n"
    
    files = {"file": ("headers.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_upload_csv_with_mixed_types():
    """Test uploading a CSV file with mixed data types"""
    csv_content = b"""product,quantity,price,available
Widget A,100,19.99,yes
Widget B,50,29.99,no
Widget C,75,24.99,yes
"""
    
    files = {"file": ("products.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload-csv", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have quantity and price as numeric columns
    assert "quantity" in data["numeric_columns"]
    assert "price" in data["numeric_columns"]
    
    # available should not be numeric (it's yes/no)
    assert "available" not in data["numeric_columns"]
    
    # Check statistics are computed
    assert "quantity" in data["statistics"]
    assert "price" in data["statistics"]
