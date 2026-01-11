# Privilege Logging Pipeline Backend

This project implements an AI-powered pipeline to automate the creation of "Privilege Logs" for legal discovery. It mimics a human lawyer's workflow to extract metadata, classify privilege status, generate safe descriptions, and identify redactions using Large Language Models (LLMs).

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (v2.0)
- **Migrations**: Alembic
- **AI/LLM**: LangChain + Google Gemini (`gemini-3-flash-preview`)
- **Language**: Python 3.x

## Prerequisites

- Python 3.8+
- PostgreSQL installed and running
- Google AI Studio API Key

## Setup

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd <repository-folder>/backend
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        # Windows Powershell: Copy-Item .env.example .env
        ```
    - Edit `.env` and provide your credentials:
        ```ini
        # Your Google API Key
        GOOGLE_API_KEY=your_google_api_key_here
        
        # PostgreSQL Connection String
        DATABASE_URL=postgresql://user:password@localhost/dbname
        ```

5.  **Database Setup**:
    - Ensure your PostgreSQL database exists.
    - Run migrations to create tables:
        ```bash
        alembic upgrade head
        ```

## Authentication

All API endpoints (except documentation) are protected and require a valid JWT token.

**Header:** `Authorization: Bearer <your_token>`

## Docker Support

You can run the backend in a Docker container.

1.  **Build the image:**
    ```bash
    docker build -t privilege-backend .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 8000:8000 --env-file .env privilege-backend
    ```

## Usage

### Running the API Server

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### API Documentation

Interactive API docs (Swagger UI) are available at:
`http://127.0.0.1:8000/docs`

### Key Endpoint: Analyze Email

**POST** `/api/v1/analyze`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Request Body:**
```json
{
  "text": "Subject: Privileged Info\n\nDear Counsel, please advise on the liability..."
}
```

**Response:**
```json
{
  "metadata": {
    "Subject": "Privileged Info",
    ...
  },
  "privilege_analysis": {
    "is_privileged": true,
    "privilege_type": "Attorney-Client",
    "description": "Confidential communication regarding liability...",
    "reasoning": "...",
    "redaction_indices": [...]
  }
}
```


## Testing

To run the verification script (mocks external services):

```bash
python test_pipeline.py
```
