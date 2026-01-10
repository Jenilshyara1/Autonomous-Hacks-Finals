import sys
import os

# Add the project root directory to sys.path so we can import 'backend'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import engine
from sqlalchemy import text

client = TestClient(app)

def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful.")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Please check your DATABASE_URL in .env and ensure Postgres is running.")
        return False

def test_analyze_email():
    print("\n--- Sending Live Request to /api/v1/analyze ---")
    payload = {
        "text": """
Date: 2024-03-10
From: ceo@client.com
To: counsel@lawfirm.com
Subject: Potential Lawsuit

Hi, we screwed up the contract logic. Will we get sued?
        """
    }
    try:
        response = client.post("/api/v1/analyze", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            import json
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error Response:")
            print(response.text)
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    if check_db_connection():
        test_analyze_email()
